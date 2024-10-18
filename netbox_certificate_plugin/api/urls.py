from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('certificates', views.CertificateViewSet)
router.register('certificate-authorities', views.CertificateAuthorityViewSet)
router.register('hostnames', views.HostnameViewSet)

urlpatterns = router.urls
