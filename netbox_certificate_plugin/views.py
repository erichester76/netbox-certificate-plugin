from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


class certificateView(generic.ObjectView):
    queryset = models.certificate.objects.all()


class certificateListView(generic.ObjectListView):
    queryset = models.certificate.objects.all()
    table = tables.certificateTable


class certificateEditView(generic.ObjectEditView):
    queryset = models.certificate.objects.all()
    form = forms.certificateForm


class certificateDeleteView(generic.ObjectDeleteView):
    queryset = models.certificate.objects.all()
