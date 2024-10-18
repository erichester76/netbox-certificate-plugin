from django.urls import path
from . import views
from netbox.views.generic import ObjectChangeLogView


urlpatterns = [
    # Ajax certificate details fetch
    path('fetch-certificate/', views.fetch_certificate, name='fetch_certificate'),

    # Certificate URLs
    path('certificates/', views.CertificateListView.as_view(), name='certificate_list'),
    path('certificates/add/', views.CertificateCreateView.as_view(), name='certificate_add'),
    path('certificates/import/', views.CertificateImportView.as_view(), name='certificate_import'),
    path('certificates/<int:pk>/', views.CertificateView.as_view(), name='certificate'),
    path('certificates/<int:pk>/edit/', views.CertificateEditView.as_view(), name='certificate_edit'),
    path('certificates/<int:pk>/delete/', views.CertificateDeleteView.as_view(), name='certificate_delete'),
    path('certificates/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='certificate_changelog'),

    # Certificate Authority URLs
    path('certificate-authorities/', views.CertificateAuthorityListView.as_view(), name='certificateauthority_list'),
    path('certificate-authorities/add/', views.CertificateAuthorityCreateView.as_view(), name='certificateauthority_add'),
    path('certificate-authorities/import/', views.CertificateAuthorityImportView.as_view(), name='certificateauthority_import'),
    path('certificate-authorities/<int:pk>/', views.CertificateAuthorityView.as_view(), name='certificateauthority'),
    path('certificate-authorities/<int:pk>/edit/', views.CertificateAuthorityEditView.as_view(), name='certificateauthority_edit'),
    path('certificate-authorities/<int:pk>/delete/', views.CertificateAuthorityDeleteView.as_view(), name='certificateauthority_delete'),
    path('certificate-authorities/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='certificateauthority_changelog'),

    # Hostname URLs
    path('hostnames/', views.HostnameListView.as_view(), name='hostname_list'),
    path('hostnames/add/', views.HostnameCreateView.as_view(), name='hostname_add'),
    path('hostnames/import/', views.HostnameImportView.as_view(), name='hostname_import'),
    path('hostnames/<int:pk>/', views.HostnameView.as_view(), name='hostname'),
    path('hostnames/<int:pk>/edit/', views.HostnameEditView.as_view(), name='hostname_edit'),
    path('hostnames/<int:pk>/delete/', views.HostnameDeleteView.as_view(), name='hostname_delete'),
    path('hostnames/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='hostname_changelog'),
]
