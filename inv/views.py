from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Sum, F
from django.db import models

import time


#from inv.forms import *
from inv.models import *
from inv.forms import *
# Create your views here.
DOCUMENT = {
    'income': {'model': DocIncome, 'form': DocIncomeForm, 'formset': DocIncomeTableUnitFormSet},
    'writeoff': {'model': DocWriteoff, 'form': DocWriteoffForm, 'formset': DocWriteoffTableUnitFormSet},
    'move': {'model': DocMove, 'form': DocMoveForm, 'formset': DocMoveTableUnitFormSet},
}

CATALOG = {
    'device': {'model': Device, 'form': DeviceForm, 'order_by': 'name'},
    'devicetype': {'model': DeviceType, 'form': DeviceTypeForm, 'order_by': 'name'},
    'nomenclature': {'model': Nomenclature, 'form': NomenclatureForm, 'order_by': 'name'},
    'person': {'model': Person, 'form': PersonForm, 'order_by': 'surname'},
    'department': {'model': Department, 'form': DepartmentForm, 'order_by': 'name'},
    'stock': {'model': Stock, 'form': StockForm, 'order_by': 'name'},
}

OPERATION_DESCR = {
    'reg_write': 'проведение',
    'reg_delete': 'отмена проведения',
    'doc_write': 'запись'
}


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


def main(request):
    return render_to_response('base.html',)


def doc_type_error(request):
    return render_to_response('doc/doc_type_error.html',)


def catlg_type_error(request):
    return render_to_response('catlg/catlg_type_error.html',)


def doc_list(request, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    doc_list = model.objects.all().order_by('doc_date')
    template_name = 'doc/%s/%s_list.html' % (doc_name, model.__name__.lower())
    return render(request, template_name, {'doc_list': doc_list})


def doc_form(request, doc_id, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    template_name = 'doc/%s/%s_form.html' % (doc_name, model.__name__.lower())
    form_class = doc_type['form']
    formset_class = doc_type['formset']

    if doc_id == 'new':
        doc = model(active=False)
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
        if doc_id == 'new':
            form = form_class()
            formset = formset_class(queryset=model.objects.none())
        else:
            form = form_class(instance=doc)
            formset = formset_class(queryset=doc.get_table_unit())

    return render(request, template_name, {'form': form, 'formset': formset, 'active': doc.active})


def operation_status(request, doc_id, doc_name, status, operation):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    doc = model.objects.get(id=doc_id)
    if int(status):
        template_name = 'doc/operation_success.html'
        return render(request, template_name, {'doc': doc, 'doc_name': doc_name, 'operation': OPERATION_DESCR[operation]})
    else:
        template_name = 'doc/operation_fail.html'
        return render(request, template_name, {'doc': doc, 'doc_name': doc_name, 'status_errors': request.session['status_errors'], 'operation': OPERATION_DESCR[operation]})


def catlg_list(request, catlg_name):
    catlg_type = get_catlg_type(catlg_name)
    if not catlg_type:
        return HttpResponseRedirect('/catlg_type_error/')
    model = catlg_type['model']
    catlg_list = model.objects.all().order_by(catlg_type['order_by'])
    template_name = 'catlg/%s/%s_list.html' % (catlg_name, model.__name__.lower())
    return render(request, template_name, {'catlg_list': catlg_list})
