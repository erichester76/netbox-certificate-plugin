from django.db import models
from netbox.models import NetBoxModel
from tenancy.models import Tenant
from django.core.exceptions import ValidationError  # Import ValidationError
from django.urls import reverse  # Import reverse

class Hostname(NetBoxModel):
    name = models.CharField(max_length=255, unique=True)  # Hostname or FQDN
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name="hostnames")
    prerequisite_models = (
        'Certificate'
    )
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_certificate_plugin:hostname', kwargs={'pk': self.pk})

class CertificateAuthority(NetBoxModel):
    name = models.CharField(max_length=255, unique=True, help_text="The name of the Certificate Authority")
    managed_by = models.CharField(
        max_length=10,
        choices=[
            ('manual', 'Manual'),
            ('acme', 'ACME'),
        ],
        default='manual',
        help_text="Indicates whether the Certificate Authority is managed manually or via ACME"
    )
    url = models.URLField(null=True, blank=True, help_text="URL of the Certificate Authority")
    contact_email = models.EmailField(null=True, blank=True, help_text="Contact email for the Certificate Authority")
    phone_number = models.CharField(max_length=20, null=True, blank=True, help_text="Support phone number for the CA")
    renewal_url = models.URLField(null=True, blank=True, help_text="URL for certificate renewal (if applicable)")
    auto_renew = models.BooleanField(default=False, help_text="Indicates if certificates are automatically renewed")
    acme_endpoint = models.URLField(null=True, blank=True, help_text="ACME API endpoint (for ACME-managed authorities)")
    acme_account = models.CharField(max_length=255, null=True, blank=True, help_text="ACME account ID")
    notes = models.TextField(null=True, blank=True, help_text="Additional notes about the Certificate Authority")

    class Meta:
        ordering = ['name']
        verbose_name_plural = ('Certificate Authorities')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_certificate_plugin:certificateauthority', kwargs={'pk': self.pk})
    

class Certificate(NetBoxModel):
    # General fields
    type = models.CharField(
        max_length=30,
        choices=[
            ('single', 'Single Domain'),
            ('wildcard', 'Wildcard'),
            ('multi-domain', 'Multi-Domain (SAN)'),
            ('ev', 'Extended Validation (EV)'),
            ('ov', 'Organization Validation (OV)'),
            ('self-signed', 'Self-Signed'),
            ('code-signing', 'Code Signing'),
            ('email', 'Email (S/MIME)'),
            ('root', 'Root Certificate'),
            ('intermediate', 'Intermediate Certificate'),
            ('client', 'Client Certificate'),
        ]
    )
    
    prerequisite_models = (
        'CertificateAuthority',
    )
    
    common_name = models.CharField(max_length=255, help_text="Common Name (CN)")
    san = models.TextField(null=True, blank=True, help_text="Comma-separated SANs")
    wildcard = models.BooleanField(default=False, help_text="Indicates if this is a wildcard certificate")
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField()

    # Identification and metadata fields
    serial_number = models.CharField(max_length=255, unique=True)
    certificate_authority = models.ForeignKey(
        'CertificateAuthority',
        on_delete=models.CASCADE,
        related_name="certificates",
        help_text="The Certificate Authority that issued the certificate"
    )    
    fingerprint = models.CharField(max_length=255, help_text="Certificate Fingerprint")

    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name="certificates")

    class Meta:
        ordering = ['expiration_date', 'common_name']

    def __str__(self):
        return f"{self.common_name} - {self.type}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_certificate_plugin:certificate', kwargs={'pk': self.pk})

    def san_list(self):
        """ Returns the SANs as a list for easy comparison """
        return [san.strip() for san in self.san.split(",")] if self.san else []
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

class CertificateHostnameRelationship(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name="hostname_relationships")
    hostname = models.ForeignKey(Hostname, on_delete=models.CASCADE, related_name="certificate_relationships")

    class Meta:
        unique_together = ('certificate', 'hostname')

    def clean(self):
        """
        Custom validation to ensure that the hostname matches the common name, SANs, or wildcard pattern.
        """
        # Check if the certificate is a wildcard and the hostname matches the wildcard pattern
        if self.certificate.wildcard:
            wildcard_domain = self.certificate.common_name.replace('*.', '')
            if not self.hostname.name.endswith(wildcard_domain):
                raise ValidationError(f"Hostname {self.hostname.name} does not match the wildcard domain {wildcard_domain}")

        # Check if the hostname matches the common name
        elif self.hostname.name == self.certificate.common_name:
            return

        # Check if the hostname matches any SANs
        elif self.hostname.name in self.certificate.san_list():
            return

        else:
            raise ValidationError(f"Hostname {self.hostname.name} does not match the certificate's common name, SANs, or wildcard pattern.")
