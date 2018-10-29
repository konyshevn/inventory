from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Sum, F

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


def main(request):
    return render_to_response('base.html',)


def doc_type_error(request):
    return render_to_response('doc_type_error.html',)


def doc_list(request, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    doc_list = model.objects.all().order_by('doc_date')
    template_name = '%s_list.html' % model.__name__.lower()
    return render(request, template_name, {'doc_list': doc_list})


def doc_form(request, doc_id, doc_name):
    doc_type = get_doc_type(doc_name)
    if not doc_type:
        return HttpResponseRedirect('/doc_type_error/')
    model = doc_type['model']
    form_class = doc_type['form']
    formset_class = doc_type['formset']

    doc = model.objects.get(id=doc_id)
    template_name = '%s_form.html' % model.__name__.lower()

    if request.method == 'POST':
        start = time.time()
        form = form_class(request.POST, instance=doc)
        formset = formset_class(request.POST, queryset=doc.get_table_unit())

        if form.is_valid() & formset.is_valid():
            form_cd = form.cleaned_data
            formset_cd = formset.cleaned_data
            if 'reg_write' in request.POST:
                start_dw = time.time()
                dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                print('-' * 50)
                print('PERIOD doc_write: ' + str(time.time() - start_dw))

                start_rd = time.time()
                rd = doc.reg_delete()
                print('-' * 50)
                print('PERIOD reg_delete: ' + str(time.time() - start_rd))

                start_rw = time.time()
                rw = doc.reg_write()
                print('-' * 50)
                print('PERIOD reg_write: ' + str(time.time() - start_rw))

                if (not dw) & (not rd) & (rw[0]):
                    print('-' * 50)
                    print('PERIOD total: ' + str(time.time() - start))
                    return HttpResponseRedirect('status/reg_write/1')
                else:
                    request.session['status_errors'] = (dw, rd, rw[1])
                    return HttpResponseRedirect('status/reg_write/0')

            elif 'reg_delete' in request.POST:
                rd = doc.reg_delete()
                if not rd:
                    return HttpResponseRedirect('status/reg_delete/1')
                else:
                    request.session['status_errors'] = (rd,)
                    return HttpResponseRedirect('status/reg_delete/0')

            elif 'doc_write' in request.POST:
                if doc.active:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    rd = doc.reg_delete()
                    rw = doc.reg_write()

                    if (not dw) & (not rd) & (rw[0]):
                        return HttpResponseRedirect('status/doc_write/1')
                    else:
                        request.session['status_errors'] = (dw, rd, rw[1])
                        return HttpResponseRedirect('status/doc_write/0')
                else:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    if not dw:
                        return HttpResponseRedirect('status/doc_write/1')
                    else:
                        request.session['status_errors'] = (dw,)
                        return HttpResponseRedirect('status/doc_write/0')

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
        template_name = 'operation_success.html'
        return render(request, template_name, {'doc': doc, 'doc_name': doc_name, 'operation': OPERATION_DESCR[operation]})
    else:
        template_name = 'operation_fail.html'
        return render(request, template_name, {'doc': doc, 'doc_name': doc_name, 'status_errors': request.session['status_errors'], 'operation': OPERATION_DESCR[operation]})
