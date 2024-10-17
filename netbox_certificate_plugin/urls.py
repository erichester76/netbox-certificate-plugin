from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views


urlpatterns = (
    path("certificates/", views.certificateListView.as_view(), name="certificate_list"),
    path("certificates/add/", views.certificateEditView.as_view(), name="certificate_add"),
    path("certificates/<int:pk>/", views.certificateView.as_view(), name="certificate"),
    path("certificates/<int:pk>/edit/", views.certificateEditView.as_view(), name="certificate_edit"),
    path("certificates/<int:pk>/delete/", views.certificateDeleteView.as_view(), name="certificate_delete"),
    path(
        "certificates/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="certificate_changelog",
        kwargs={"model": models.certificate},
    ),
)
