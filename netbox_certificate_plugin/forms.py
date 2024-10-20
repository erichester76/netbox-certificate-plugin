from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from django.core.exceptions import ValidationError  # Import ValidationError
from . import models


class CertificateForm(forms.ModelForm):
    
    common_name = forms.CharField(
        label='Common Name',
        max_length=255,
        help_text='The fully qualified domain name (FQDN) for the certificate.'
    )
    san = forms.ModelMultipleChoiceField(
        queryset=models.Hostname.objects.all(),
        required=False,
        label='Subject Alternative Names (SAN)',
        help_text='The Subject Alternative Names (SAN) for this certificate.',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    certificate_authority = forms.ModelChoiceField(
        queryset=models.CertificateAuthority.objects.all(),
        label='Certificate Authority',
        help_text='The certificate authority that issued the certificate.',
        widget=forms.Select()
    )
    serial_number = forms.CharField(
        label='Serial Number',
        max_length=100,
        required=False,
        help_text='The serial number of the certificate.'
    )
    issue_date = forms.DateField(
        label='Issue Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='The date when the certificate was issued.'
    )
    expiration_date = forms.DateField(
        label='Expiration Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='The expiration date of the certificate.'
    )

    class Meta:
        model = models.Certificate
        fields = ['common_name', 'type', 'san', 'certificate_authority', 'tenant', 'issue_date', 'expiration_date', 'serial_number', 'fingerprint'] 

    def clean(self):
        cleaned_data = super().clean()
        common_name = cleaned_data.get('common_name')
        expiration_date = cleaned_data.get('expiration_date')
        issue_date = cleaned_data.get('issue_date')

        # Ensure the expiration date is after the issue date
        if expiration_date and issue_date and expiration_date <= issue_date:
            raise ValidationError("Expiration date must be after the issue date.")

        return cleaned_data
    
class CertificateAuthorityForm(NetBoxModelForm):
   
    class Meta:
        model = models.CertificateAuthority
        fields = ['name', 'managed_by', 'url', 'contact_email', 'phone_number', 'renewal_url', 'auto_renew', 'acme_endpoint', 'acme_account', 'notes']

class HostnameForm(forms.ModelForm):
   
    certificate = forms.ModelChoiceField(
        queryset=models.Certificate.objects.all(),  # Single select dropdown for certificates
        required=False,
        label='Associated Certificate',
        help_text='Select the certificate associated with this hostname.',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.Hostname
        fields = ['name', 'tenant', 'certificate']  # Added 'certificate' field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Print/log to verify that certificates are being fetched
        certificate_queryset = models.Certificate.objects.all()
        print(f"Certificate queryset: {certificate_queryset}")  # For debugging purposes

        # Ensure that all certificates are available in the dropdown
        self.fields['certificate'].queryset = certificate_queryset

        # If editing an existing hostname, prepopulate certificate based on relationship
        if self.instance and self.instance.pk:
            relationship = models.CertificateHostnameRelationship.objects.filter(hostname=self.instance).first()
            if relationship:
                self.fields['certificate'].initial = relationship.certificate

    def save(self, commit=True):
        """
        Override save to handle the certificate-hostname relationship.
        """
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self.save_certificate(instance)

        return instance

    def save_certificate(self, instance):
        # Clear existing relationship
        models.CertificateHostnameRelationship.objects.filter(hostname=instance).delete()

        # Create new relationship if a certificate is selected
        certificate = self.cleaned_data.get('certificate')
        if certificate:
            relationship = models.CertificateHostnameRelationship(certificate=certificate, hostname=instance)
            relationship.full_clean()  # Ensure validation is applied
            relationship.save()
    
class CertificateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Certificate
        fields = ['type', 'common_name', 'san', 'certificate_authority', 'issue_date', 'expiration_date']

class CertificateAuthorityImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.CertificateAuthority
        fields = ['name', 'managed_by', 'url', 'contact_email']

class HostnameImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Hostname
        fields = ['name', 'tenant']
