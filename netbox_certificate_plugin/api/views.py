from rest_framework.viewsets import ModelViewSet
from ..models import Certificate, CertificateAuthority, Hostname
from .serializers import CertificateSerializer, CertificateAuthoritySerializer, HostnameSerializer

class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class CertificateAuthorityViewSet(ModelViewSet):
    queryset = CertificateAuthority.objects.all()
    serializer_class = CertificateAuthoritySerializer

class HostnameViewSet(ModelViewSet):
    queryset = Hostname.objects.all()
    serializer_class = HostnameSerializer
