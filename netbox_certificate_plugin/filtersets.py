from netbox.filtersets import NetBoxModelFilterSet
from .models import certificate


# class certificateFilterSet(NetBoxModelFilterSet):
#
#     class Meta:
#         model = certificate
#         fields = ['name', ]
#
#     def search(self, queryset, name, value):
#         return queryset.filter(description__icontains=value)
