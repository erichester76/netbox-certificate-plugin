from netbox.views import generic
from . import forms, models, tables
from extras.views import ObjectBulkImportView, ObjectChangeLogView

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

class CertificateDeleteView(generic.ObjectDeleteView):
    queryset = models.Certificate.objects.all()

class CertificateImportView(ObjectBulkImportView):
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

class CertificateAuthorityImportView(ObjectBulkImportView):
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

class HostnameImportView(ObjectBulkImportView):
    queryset = models.Hostname.objects.all()
    model_form = forms.HostnameImportForm

