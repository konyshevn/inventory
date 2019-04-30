from django.contrib import admin

# Register your models here.


from inv.models import Nomenclature, DeviceType, Device
from inv.models import DocIncome, DocIncomeTableUnit, Person, Department, Stock, DocMove, DocMoveTableUnit, DocWriteoff, DocWriteoffTableUnit
from inv.models import DocInventory, DocInventoryTableUnit
from inv.models import RegDeviceStock


class DocIncomeTableUnitInline(admin.TabularInline):
    model = DocIncomeTableUnit
    extra = 1


class DocMoveTableUnitInline(admin.TabularInline):
    model = DocMoveTableUnit
    extra = 1


class DocWriteoffTableUnitInline(admin.TabularInline):
    model = DocWriteoffTableUnit
    extra = 1


class DocInventoryTableUnitInline(admin.TabularInline):
    model = DocInventoryTableUnit
    extra = 1


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)


class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('label',)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('deviceType', 'nomenclature', 'serial_num', 'inv_num', 'comment')


class DocIncomeAdmin(admin.ModelAdmin):
    list_display = ('doc_date', 'doc_num', 'active', 'department', 'stock')
    inlines = (DocIncomeTableUnitInline,)


class DocIncomeTableUnitAdmin(admin.ModelAdmin):
    list_display = ('doc', 'device', 'person', 'qty', 'comment')
#    inlines = (IncomeTableUnitInline,)


class DocMoveAdmin(admin.ModelAdmin):
    list_display = ('doc_date', 'doc_num', 'active', 'department_from', 'department_to', 'stock_from', 'stock_to')
    inlines = (DocMoveTableUnitInline,)


class DocMoveTableUnitAdmin(admin.ModelAdmin):
    list_display = ('doc', 'device', 'person_from', 'person_to', 'qty', 'comment')


class DocWriteoffAdmin(admin.ModelAdmin):
    list_display = ('doc_date', 'doc_num', 'active', 'department', 'stock')
    inlines = (DocWriteoffTableUnitInline,)


class DocWriteoffTableUnitAdmin(admin.ModelAdmin):
    list_display = ('doc', 'device', 'person', 'qty', 'comment')
#    inlines = (IncomeTableUnitInline,)


class DocInventoryAdmin(admin.ModelAdmin):
    list_display = ('doc_date', 'doc_num', 'active', 'department', 'stock')
    inlines = (DocInventoryTableUnitInline,)


class DocInventoryTableUnitAdmin(admin.ModelAdmin):
    list_display = ('doc', 'device', 'person_accountg', 'qty_accountg', 'person_fact', 'stock_fact', 'qty_fact', 'comment')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'department')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('label',)


class StockAdmin(admin.ModelAdmin):
    list_display = ('label',)


class RegDeviceStockAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'reg_date', 'base_doc_type', 'base_doc_id', 'base_doc', 'department', 'stock', 'device', 'person', 'qty')
    readonly_fields = ('base_doc',)
    search_fields = ('department', )

#    model = RegDeviceStock


#class RegDeviceStockAdmin(admin.ModelAdmin):

admin.site.register(Nomenclature, NomenclatureAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DocIncome, DocIncomeAdmin)
admin.site.register(DocIncomeTableUnit, DocIncomeTableUnitAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(RegDeviceStock, RegDeviceStockAdmin)
admin.site.register(DocMove, DocMoveAdmin)
admin.site.register(DocMoveTableUnit, DocMoveTableUnitAdmin)
admin.site.register(DocWriteoff, DocWriteoffAdmin)
admin.site.register(DocWriteoffTableUnit, DocWriteoffTableUnitAdmin)
admin.site.register(DocInventory, DocInventoryAdmin)
admin.site.register(DocInventoryTableUnit, DocInventoryTableUnitAdmin)
