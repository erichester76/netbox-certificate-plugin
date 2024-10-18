from rest_framework import serializers
from ..models import Certificate, CertificateAuthority, Hostname

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'name', 'type', 'common_name', 'san', 'wildcard', 'certificate_authority', 'issue_date', 'expiration_date', 'serial_number', 'fingerprint', 'tenant', 'tags']

class CertificateAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateAuthority
        fields = ['id', 'name', 'managed_by', 'url', 'contact_email', 'phone_number', 'renewal_url', 'auto_renew', 'acme_endpoint', 'acme_account', 'notes']

class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostname
        fields = ['id', 'name', 'tenant']
