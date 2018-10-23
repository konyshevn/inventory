from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Sum, F

#from inv.forms import *
from inv.models import *
from inv.forms import *
# Create your views here.


def main(request):
    return render_to_response('base.html',)


def doc_list(request, model):
    doc_list = model.objects.all()
    template_name = '%s_list.html' % model.__name__.lower()
    return render(request, template_name, {'doc_list': doc_list})


def doc_form(request, doc_id, model):
    doc = model.objects.get(id=doc_id)
    template_name = '%s_form.html' % model.__name__.lower()

    if request.method == 'POST':
        print('-' * 50)
        form = DocIncomeForm(request.POST, instance=doc)
        formset = DocIncomeTableUnitFormSet(request.POST, queryset=doc.get_table_unit())
        print('form: ' + str(form.is_valid()))
        print('formset: ' + str(formset.is_valid()))
        print('formset errors: %s' % formset.errors)
        print('request.POST: %s' % request.POST)

        if form.is_valid() & formset.is_valid():
            form_cd = form.cleaned_data
            formset_cd = formset.cleaned_data
            doc_num = form_cd['doc_num']
            doc_date = form_cd['doc_date']
            department = form_cd['department']
            stock = form_cd['stock']
            dw = doc.doc_write(doc_num=doc_num, doc_date=doc_date, department=department, stock=stock, table_unit=formset_cd)
            rd = doc.reg_delete()
            rw = doc.reg_write()
            if (not dw) & (not rd) & (not rw):
                return HttpResponseRedirect('success')
            else:
                return HttpResponseRedirect('fail')
    else:
        form = DocIncomeForm(instance=doc)
        formset = DocIncomeTableUnitFormSet(queryset=doc.get_table_unit())

    return render(request, template_name, {'form': form, 'formset': formset})
