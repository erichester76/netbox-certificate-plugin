import django_tables2 as tables
from netbox.tables import NetBoxTable
from django.utils.html import format_html
from .models import Certificate, CertificateAuthority, Hostname

class CertificateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    certificate_authority = tables.Column(linkify=True)
    common_name = tables.Column()
    expiration_date = tables.DateColumn()

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ('name', 'type', 'common_name', 'certificate_authority', 'expiration_date', 'fingerprint', 'tags')
        order_by = ('expiration_date',)  # Default sort by expiration date
        
    def render_expiration_date(self, value):
        # Highlight certificates expiring within 30 days
        if value and (value - now().date()).days <= 30:
            return format_html('<span class="text-danger">{}</span>', value)
        return value

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ('common_name', 'expiration_date', 'certificate_type')
        default_columns = ('common_name', 'expiration_date', 'certificate_type')
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
