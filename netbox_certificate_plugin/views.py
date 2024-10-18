from netbox.views import generic
from . import forms, models, tables
from django.http import JsonResponse
import ssl
import socket
from datetime import datetime
from OpenSSL import crypto  # To process certificates
from django.db.models import ManyToOneRel

def get_related_models(model, ordered=True):
    """
    Return a list of all models which have a ForeignKey to the given model and the name of the field. For example,
    `get_related_models(Tenant)` will return all models which have a ForeignKey relationship to Tenant.
    """
    related_models = [
        (field.related_model, field.remote_field.name)
        for field in model._meta.related_objects
        if type(field) is ManyToOneRel
    ]

    if ordered:
        return sorted(related_models, key=lambda x: x[0]._meta.verbose_name.lower())

    return related_models

def fetch_certificate(request):
    """
    This view fetches certificate data from the given common name.
    """
    common_name = request.GET.get('common_name')

    if not common_name:
        return JsonResponse({'error': 'Common Name is required'}, status=400)

    try:
        cert_data = ssl.get_server_certificate((common_name, 443))  
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        
        # Extract data from the certificate
        issued_to = x509.get_subject().CN  # Common Name
        issued_by = x509.get_issuer().CN  # Issuer CN
        serial_number = x509.get_serial_number()  # Serial Number
        expiration_date = x509.get_notAfter().decode('utf-8')  # Expiration date in bytes
        issue_date = x509.get_notBefore().decode('utf-8')  # Issue date in bytes
        fingerprint = x509.digest('sha256').decode('utf-8')  # Fingerprint using SHA-256
        # Extract SANs (Subject Alternative Names) if present
        san_names = []
        for i in range(x509.get_extension_count()):
            ext = x509.get_extension(i)
            if ext.get_short_name().decode('utf-8') == 'subjectAltName':
                san_extension = ext
                san_names = [name[4:] for name in str(san_extension).split(", ") if name.startswith('DNS:')]
                break

        # Determine the certificate type
        wildcard = False
        cert_type = 'standard'  # Default to 'standard'
        
        # Check for wildcards in both issued_to and SANs
        if '*' in issued_to:
            wildcard = True
            cert_type = 'wildcard'
        elif any('*' in san for san in san_names):
            wildcard = True
            issued_to = next(san for san in san_names if '*' in san)  # Set issued_to to the wildcard from SANs
            cert_type = 'wildcard'
        elif len(san_names) > 1:
            cert_type = 'multi-domain'
            
        # Format the expiration date to a readable format
        expiration_date = f"{expiration_date[:4]}-{expiration_date[4:6]}-{expiration_date[6:8]}"
        issue_date = f"{issue_date[:4]}-{issue_date[4:6]}-{issue_date[6:8]}"

        # Return the extracted data as a JSON response
        return JsonResponse({
            'issued_to': issued_to,
            'issued_by': issued_by,
            'serial_number': serial_number,
            'expiration_date': expiration_date,
            'issue_date': issue_date,
            'wildcard': wildcard,
            'type': cert_type,
            'san_names': san_names,
            'fingerprint': fingerprint,  # Return the fingerprint
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class CertificateListView(generic.ObjectListView):
    queryset =models.Certificate.objects.all().order_by('expiration_date')  # Sort by expiration date
    table = tables.CertificateTable

class CertificateView(generic.ObjectView):
    queryset = models.Certificate.objects.all()
    
    def get_extra_context(self, request, instance):

        return {
            'related_models': get_related_models(request,instance),
        }

class CertificateCreateView(generic.ObjectEditView):
    queryset = models.Certificate.objects.all()
    form = forms.CertificateForm
    template_name = 'netbox_certificate_plugin/certificate_form.html'

class CertificateEditView(generic.ObjectEditView):
    queryset = models.Certificate.objects.all()
    form = forms.CertificateForm
    template_name = 'netbox_certificate_plugin/certificate_form.html'


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
    
    def get_extra_context(self, request, instance):
 
        return {
            'related_models': get_related_models(request,instance),
        }

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

    def get_extra_context(self, request, instance):
        related_certificates = models.CertificateHostnameRelationship.objects.filter(hostname=instance).select_related('certificate')

        return {
            'related_models': get_related_models(request,instance),
            'related_certificates': related_certificates,
        }

class HostnameCreateView(generic.ObjectEditView):
    queryset = models.Hostname.objects.all()
    form = forms.HostnameForm
    template_name = 'netbox_certificate_plugin/hostname_form.html'

class HostnameEditView(generic.ObjectEditView):
    queryset = models.Hostname.objects.all()
    form = forms.HostnameForm
    template_name = 'netbox_certificate_plugin/hostname_form.html'

    def get_extra_context(self, request, instance):
        """
        Pass extra context for certificates related to the hostname.
        """
        # Fetch existing certificates related to this hostname via the relationship table
        related_certificates = instance.certificate_relationships.all().values_list('certificate__id', flat=True)
        return {
            'related_certificates': related_certificates
        }

    def post(self, request, *args, **kwargs):
        """
        Handle saving the certificate relationships upon form submission.
        """
        instance = self.get_object()
        form = self.get_form()

        if form.is_valid():
            # Save the hostname and the certificate relationships
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class HostnameDeleteView(generic.ObjectDeleteView):
    queryset = models.Hostname.objects.all()

class HostnameImportView(generic.BulkImportView):
    queryset = models.Hostname.objects.all()
    model_form = forms.HostnameImportForm

