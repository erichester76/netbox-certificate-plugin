from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from django.core.exceptions import ValidationError  # Import ValidationError
from . import models


class CertificateForm(forms.ModelForm):
    class Meta:
        model = models.Certificate
        fields = ['common_name', 'certificate_authority', 'serial_number', 'san', 'issue_date', 'expiration_date']

    common_name = forms.CharField(
        label='Common Name',
        max_length=255,
        help_text='The fully qualified domain name (FQDN) for the certificate.'
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

    san = forms.ModelMultipleChoiceField(
        queryset=models.Hostname.objects.all(),
        required=False,
        label='Subject Alternative Names (SAN)',
        help_text='The Subject Alternative Names (SAN) for this certificate.',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
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

class HostnameForm(NetBoxModelForm):
    class Meta:
        model = models.Hostname
        fields = ['name', 'tenant']
        
class CertificateImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Certificate
        fields = ['name', 'type', 'common_name', 'san', 'certificate_authority', 'issue_date', 'expiration_date']

class CertificateAuthorityImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.CertificateAuthority
        fields = ['name', 'managed_by', 'url', 'contact_email']

class HostnameImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Hostname
        fields = ['name', 'tenant']
