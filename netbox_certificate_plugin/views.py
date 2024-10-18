from netbox.views import generic
from . import forms, models, tables
from extras.views import ObjectBulkImportView, ObjectChangeLogView
from django.http import JsonResponse
import ssl
import socket
from datetime import datetime

def fetch_certificate(request):
    common_name = request.GET.get('common_name')
    
    if not common_name:
        return JsonResponse({"error": "Common name is required"}, status=400)

    try:
        # Fetch the certificate for the domain
        context = ssl.create_default_context()
        with socket.create_connection((common_name, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=common_name) as ssock:
                cert = ssock.getpeercert()

        # Parse the certificate fields
        issued_to = dict(x[0] for x in cert['subject'])['commonName']
        issued_by = dict(x[0] for x in cert['issuer'])['commonName']
        serial_number = cert['serialNumber']
        expiration_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y GMT')

        return JsonResponse({
            "issued_to": issued_to,
            "issued_by": issued_by,
            "serial_number": serial_number,
            "expiration_date": expiration_date,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class CertificateListView(generic.ObjectListView):
    queryset = models.Certificate.objects.all()
    table = tables.CertificateTable

class CertificateView(generic.ObjectView):
    queryset = models.Certificate.objects.all()

class CertificateCreateView(generic.ObjectEditView):
    queryset = models.Certificate.objects.all()
    form = forms.CertificateForm

class CertificateEditView(generic.ObjectEditView):
    queryset = models.Certificate.objects.all()
    form = forms.CertificateForm
    template_name = 'netbox_certificate_plugin/certificate-form.html'


class CertificateDeleteView(generic.ObjectDeleteView):
    queryset = models.Certificate.objects.all()

class CertificateImportView(generic.BulkImportView):
    queryset = models.Certificate.objects.all()
    model_form = forms.CertificateImportForm


# Certificate Authority Views
class CertificateAuthorityListView(generic.ObjectListView):
    queryset = models.CertificateAuthority.objects.all()
    table = tables.CertificateAuthorityTable

class CertificateAuthorityView(generic.ObjectView):
    queryset = models.CertificateAuthority.objects.all()

class CertificateAuthorityCreateView(generic.ObjectEditView):
    queryset = models.CertificateAuthority.objects.all()
    form = forms.CertificateAuthorityForm

class CertificateAuthorityEditView(generic.ObjectEditView):
    queryset = models.CertificateAuthority.objects.all()
    form = forms.CertificateAuthorityForm

class CertificateAuthorityDeleteView(generic.ObjectDeleteView):
    queryset = models.CertificateAuthority.objects.all()

class CertificateAuthorityImportView(generic.BulkImportView):
    queryset = models.CertificateAuthority.objects.all()
    model_form = forms.CertificateAuthorityImportForm


# Hostname Views
class HostnameListView(generic.ObjectListView):
    queryset = models.Hostname.objects.all()
    table = tables.HostnameTable

class HostnameView(generic.ObjectView):
    queryset = models.Hostname.objects.all()

class HostnameCreateView(generic.ObjectEditView):
    queryset = models.Hostname.objects.all()
    form = forms.HostnameForm

class HostnameEditView(generic.ObjectEditView):
    queryset = models.Hostname.objects.all()
    form = forms.HostnameForm

class HostnameDeleteView(generic.ObjectDeleteView):
    queryset = models.Hostname.objects.all()

class HostnameImportView(generic.BulkImportView):
    queryset = models.Hostname.objects.all()
    model_form = forms.HostnameImportForm

