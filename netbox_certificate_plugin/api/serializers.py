from rest_framework import serializers
from .. import models

class HostnameSerializer(serializers.ModelSerializer):
    # Display certificates associated with this hostname
    certificates = serializers.SerializerMethodField()

    class Meta:
        model = models.Hostname
        fields = ['id', 'name', 'tenant', 'certificates']

    def get_certificates(self, obj):
        # Fetch related certificates from the CertificateHostnameRelationship table
        relationships = models.CertificateHostnameRelationship.objects.filter(hostname=obj)
        return [CertificateSerializer(relationship.certificate).data for relationship in relationships]


class CertificateSerializer(serializers.ModelSerializer):
    # Display hostnames associated with this certificate
    hostnames = serializers.SerializerMethodField()

    class Meta:
        model = models.Certificate
        fields = ['id', 'common_name', 'expiration_date', 'type', 'hostnames']

    def get_hostnames(self, obj):
        # Fetch related hostnames from the CertificateHostnameRelationship table
        relationships = models.CertificateHostnameRelationship.objects.filter(certificate=obj)
        return [HostnameSerializer(relationship.hostname).data for relationship in relationships]

class CertificateAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CertificateAuthority
        fields = ['id', 'name', 'managed_by', 'url', 'contact_email', 'phone_number', 'renewal_url', 'auto_renew', 'acme_endpoint', 'acme_account', 'notes']

