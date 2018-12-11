# app_name/lookup.py
from ajax_select import register, LookupChannel
from inv.models import *


@register('departments')
class DepartmentLookup(LookupChannel):

    model = Department

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def format_item_display(self, item):
        return "<span class='department'>%s</span>" % item.name
