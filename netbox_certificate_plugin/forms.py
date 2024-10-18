from django import forms
from utilities.forms import BootstrapMixin
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from . import models

class CertificateForm(NetBoxModelForm):
    class Meta:
        model = models.Certificate
        fields = ['name', 'type', 'common_name', 'san', 'wildcard', 'certificate_authority', 'issue_date', 'expiration_date', 'serial_number', 'fingerprint', 'tenant', 'tags']

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
