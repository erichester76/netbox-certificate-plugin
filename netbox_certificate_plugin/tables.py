import django_tables2 as tables
from netbox.tables import NetBoxTable
from django.utils.html import format_html
from .models import Certificate, CertificateAuthority, Hostname
from django.utils.timezone import now
from django.template.defaultfilters import date as date_filter

class CertificateTable(NetBoxTable):
    certificate_authority = tables.Column(linkify=True)
    common_name = tables.Column(linkify=True)
    expiration_date = tables.DateColumn()

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ('common_name', 'type', 'certificate_authority', 'expiration_date', 'fingerprint', 'tags')
        order_by = ('expiration_date',)  # Default sort by expiration date
        
    def render_expiration_date(self, value):
        formatted_date = date_filter(value, "F d, Y")  # e.g., "October 10, 2024"
        
        # Highlight certificates expiring within 30 days
        if value and (value - now().date()).days <= 90:
            return format_html('<span class="text-danger">{}</span>', formatted_date)
        
        return formatted_date

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ('common_name', 'expiration_date', 'type')
        default_columns = ('common_name', 'type', 'expiration_date')
        order_by = ('expiration_date',)  # Default sort by expiration date


class CertificateAuthorityTable(NetBoxTable):
    name = tables.Column(linkify=True)
    managed_by = tables.Column()
    url = tables.URLColumn()

    class Meta(NetBoxTable.Meta):
        model = CertificateAuthority
        fields = ('name', 'managed_by', 'url', 'contact_email')

class HostnameTable(NetBoxTable):
    name = tables.Column(linkify=True)
    tenant = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = Hostname
        fields = ('name', 'tenant')
