from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Sum, F
from django.db import models
from django.contrib.contenttypes.models import ContentType
import time, datetime


from inv.models import *
from inv.forms import *

DOCUMENT = {
    'income': {'model': DocIncome, 'table_unit': DocIncomeTableUnit, 'form': DocIncomeForm, 'formset': DocIncomeTableUnitFormSet},
    'writeoff': {'model': DocWriteoff, 'table_unit': DocWriteoffTableUnit, 'form': DocWriteoffForm, 'formset': DocWriteoffTableUnitFormSet},
    'move': {'model': DocMove, 'table_unit': DocMoveTableUnit, 'form': DocMoveForm, 'formset': DocMoveTableUnitFormSet},
}

CATALOG = {
    'device': {'model': Device, 'form': DeviceForm, 'order_by': 'name'},
    'devicetype': {'model': DeviceType, 'form': DeviceTypeForm, 'order_by': 'name'},
    'nomenclature': {'model': Nomenclature, 'form': NomenclatureForm, 'order_by': 'name'},
    'person': {'model': Person, 'form': PersonForm, 'order_by': 'surname'},
    'department': {'model': Department, 'form': DepartmentForm, 'order_by': 'name'},
    'stock': {'model': Stock, 'form': StockForm, 'order_by': 'name'},
}

REGISTRY = {
    'devicestock': {'model': RegDeviceStock, 'form': RegDeviceStockForm},
}

OPERATION_DESCR = {
    'reg_write': 'Проведение документа',
    'reg_delete': 'Отмена проведения документа',
    'doc_write': 'Запись документа',
    'catlg_write': 'Запись',
}


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def get_doc_type(doc_name):
    if doc_name in DOCUMENT:
        return DOCUMENT[doc_name]
    else:
        return False


def get_catlg_type(catlg_name):
    if catlg_name in CATALOG:
        return CATALOG[catlg_name]
    else:
        return False


def get_reg_type(reg_name):
    if reg_name in REGISTRY:
        return REGISTRY[reg_name]
    else:
        return False


def main(request):
    return render_to_response('base.html',)


def doc_type_error(request):
    return render_to_response('doc/doc_type_error.html',)


def catlg_type_error(request):
    return render_to_response('catlg/catlg_type_error.html',)


def reg_type_error(request):
    return render_to_response('reg/reg_type_error.html',)


# Форма списка документов
def doc_list(request, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    doc_list = model.objects.all().order_by('doc_date')
    template_name = 'doc/%s/%s_list.html' % (doc_name, model.__name__.lower())
    return render(request, template_name, {'doc_list': doc_list})


# Форма документа
def doc_form(request, doc_id, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    form_class = doc_type['form']
    formset_class = doc_type['formset']
    template_name = 'doc/%s/%s_form.html' % (doc_name, model.__name__.lower())
    if doc_id == 'new':
        doc_num = model.objects.get_doc_num()
        doc = model(doc_num=doc_num, doc_date=datetime.datetime.now(), active=False)
    else:
        doc = model.objects.get(id=doc_id)

    if request.method == 'POST':
        start = time.time()
        form = form_class(request.POST, instance=doc)
        formset = formset_class(request.POST, queryset=doc.get_table_unit())

        if form.is_valid() & formset.is_valid():
            form_cd = form.cleaned_data
            formset_cd = formset.cleaned_data
            if 'reg_write' in request.POST:
                dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                rd = doc.reg_delete()
                rw = doc.reg_write()
                if (not dw) & (not rd) & (rw[0]):
                    print('-' * 50)
                    print('PERIOD total: ' + str(time.time() - start))
                    status_url = '/doc/%s/%s/status/reg_write/1' % (doc_name, doc.id)
                else:
                    request.session['status_errors'] = (dw, rd, rw[1])
                    status_url = '/doc/%s/%s/status/reg_write/0' % (doc_name, doc.id)

            elif 'reg_delete' in request.POST:
                rd = doc.reg_delete()
                if not rd:
                    status_url = '/doc/%s/%s/status/reg_delete/1' % (doc_name, doc.id)
                else:
                    request.session['status_errors'] = (rd,)
                    status_url = '/doc/%s/%s/status/reg_delete/0' % (doc_name, doc.id)

            elif 'doc_write' in request.POST:
                if doc.active:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    rd = doc.reg_delete()
                    rw = doc.reg_write()

                    if (not dw) & (not rd) & (rw[0]):
                        status_url = '/doc/%s/%s/status/doc_write/1' % (doc_name, doc.id)
                    else:
                        request.session['status_errors'] = (dw, rd, rw[1])
                        status_url = '/doc/%s/%s/status/doc_write/0' % (doc_name, doc.id)
                else:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    if not dw:
                        status_url = '/doc/%s/%s/status/doc_write/1' % (doc_name, doc.id)
                    else:
                        request.session['status_errors'] = (dw,)
                        status_url = '/doc/%s/%s/status/doc_write/0' % (doc_name, doc.id)
            return HttpResponseRedirect(status_url)
    else:
        form = form_class(instance=doc)
        if doc_id == 'new':
            formset = formset_class(queryset=model.objects.none())
        else:
            formset = formset_class(queryset=doc.get_table_unit())

    return render(request, template_name, {'form': form, 'formset': formset, 'active': doc.active})


def operation_status(request, obj_type_name, obj_id, obj_name, status, operation):
    if obj_type_name == 'doc':
        obj_type = get_doc_type(obj_name)
        if not obj_type:
            return HttpResponseRedirect('/doc_type_error/')
    elif obj_type_name == 'catlg':
        obj_type = get_catlg_type(obj_name)
        if not obj_type:
            return HttpResponseRedirect('/catlg_type_error/')
    model = obj_type['model']
    obj = model.objects.get(id=obj_id)
    if int(status):
        template_name = 'operation_success.html'
        return render(request, template_name, {'obj': obj, 'obj_name': obj_name, 'obj_type_name': obj_type_name, 'operation': OPERATION_DESCR[operation]})
    else:
        template_name = 'operation_fail.html'
        return render(request, template_name, {'obj': obj, 'obj_name': obj_name, 'obj_type_name': obj_type_name, 'status_errors': request.session['status_errors'], 'operation': OPERATION_DESCR[operation]})


# форма списка справочника
def catlg_list(request, catlg_name):
    catlg_type = get_catlg_type(catlg_name)
    if not catlg_type:
        return HttpResponseRedirect('/catlg_type_error/')
    model = catlg_type['model']
    catlg_list = model.objects.all().order_by(catlg_type['order_by'])
    template_name = 'catlg/%s/%s_list.html' % (catlg_name, model.__name__.lower())
    return render(request, template_name, {'catlg_list': catlg_list})


# форма справочника
def catlg_form(request, catlg_id, catlg_name):
    catlg_type = get_catlg_type(catlg_name)
    if not catlg_type:
        return HttpResponseRedirect('/catlg_type_error/')
    model = catlg_type['model']
    template_name = 'catlg/%s/%s_form.html' % (catlg_name, model.__name__.lower())
    form_class = catlg_type['form']

    if catlg_id == 'new':
        catlg = model()
    else:
        catlg = model.objects.get(id=catlg_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=catlg)

        if form.is_valid():
            form_cd = form.cleaned_data
            if 'catlg_write' in request.POST:
                cw = catlg.catlg_write(catlg_attr=form_cd)
                if (not cw):
                    status_url = '/catlg/%s/%s/status/catlg_write/1' % (catlg_name, catlg.id)
                else:
                    request.session['status_errors'] = (cw, )
                    status_url = '/catlg/%s/%s/status/catlg_write/0' % (catlg_name, catlg.id)
            return HttpResponseRedirect(status_url)
    else:
        if catlg_id == 'new':
            form = form_class()
        else:
            form = form_class(instance=catlg)

    return render(request, template_name, {'form': form, })


# Вывод записей регистров по документу
def doc_reg_recs(request, doc_name, doc_id):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    doc_model = doc_type['model']
    base_doc_type = ContentType.objects.get_for_model(doc_model)
    reg_recs = {}
    doc = doc_model.objects.get(id=doc_id)

    for reg in doc._REG_LIST:
        reg_model = getattr(sys.modules[__name__], reg)
        reg_recs.update([(reg, reg_model.objects.filter(base_doc_type=base_doc_type, base_doc_id=doc_id))])

    template_name = 'reg/doc_reg_recs.html'
    print(reg_recs)
    return render(request, template_name, {'reg_recs': reg_recs, 'doc': doc})


def report_current_location(request, dev_id, date_to):
    location = []
    filter_vals = {}
    if request.method == 'POST':
        form = ReportCurrentLocationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not cd['device'] == '' and not cd['device'] is None:
                devices = Device.objects.filter(id=cd['device'])
            else:
                devices = Device.objects.all()

            if not cd['date_to'] == '' and not cd['date_to'] is None:
                date_to = cd['date_to'] + datetime.timedelta(days=1)

            if not cd['department'] == '' and not cd['department'] is None:
                filter_vals['department'] = cd['department']

            if not cd['stock'] == '' and not cd['stock'] is None:
                filter_vals['stock'] = cd['stock']

            if not cd['person'] == '' and not cd['person'] is None:
                filter_vals['person'] = cd['person']

            for device in devices:
                location_rec = {'device': device, 'department': '', 'stock': '', 'person': '', 'qty': None}
                qty = RegDeviceStock.objects.saldo(device=device, date_to=date_to)
                if qty == 1:
                    reg_rec = RegDeviceStock.objects.filter(device=device, operation_type='+', reg_date__lte=date_to).order_by('-reg_date')

                    if reg_rec[0].department is None:
                        location_rec['department'] = ''
                    else:
                        location_rec['department'] = str(reg_rec[0].department)

                    if reg_rec[0].stock is None:
                        location_rec['stock'] = ''
                    else:
                        location_rec['stock'] = str(reg_rec[0].stock)

                    if reg_rec[0].person is None:
                        location_rec['person'] = ''
                    else:
                        location_rec['person'] = str(reg_rec[0].person)

                location_rec['qty'] = qty
                filter_diff = DictDiffer(location_rec, filter_vals)
                if len(filter_diff.changed()) == 0:
                    location.append(location_rec)

    else:
        form = ReportCurrentLocationForm()

    template_name = 'report/current_location.html'
    return render(request, template_name, {'location': location, 'form': form})


#--------------------------DONT USE NOW--------------------------------
def reg_search(request, reg_name, base_doc_id=None, doc_name=None):
    reg_type = get_reg_type(reg_name)
    if not reg_type:
        return HttpResponseRedirect('/reg_type_error/')
    reg_model = reg_type['model']
    template_name = 'reg/reg_search.html'
    form_class = reg_type['form']

    if doc_name:
        doc_type = get_doc_type(doc_name)
        if not doc_type:
            return HttpResponseRedirect('/doc_type_error/')
        base_doc_type = ContentType.objects.get_for_model(doc_type['model'])
        if base_doc_id:
            reg_recs = reg_model.objects.filter(base_doc_type=base_doc_type, base_doc_id=base_doc_id)
        else:
            reg_recs = reg_model.objects.filter(base_doc_type=base_doc_type)
    else:
        reg_recs = reg_model.objects.all()

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            form_cd = form.cleaned_data
            if 'reg_search' in request.POST:

                cw = catlg.catlg_write(catlg_attr=form_cd)
                if (not cw):
                    status_url = '/catlg/%s/%s/status/catlg_write/1' % (catlg_name, catlg.id)
                else:
                    request.session['status_errors'] = (cw, )
                    status_url = '/catlg/%s/%s/status/catlg_write/0' % (catlg_name, catlg.id)
            return HttpResponseRedirect(status_url)
    else:
        form = form_class()
    print(reg_recs)

    return render(request, template_name, {'form': form, 'reg_recs': reg_recs})
#----------------------------------------------------------------------