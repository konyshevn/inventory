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
        formset = DocIncomeTableUnitFormSet(request.POST, queryset=DocIncomeTableUnit.objects.filter(doc=doc))
        print('form: ' + str(form.is_valid()))
        print('formset: ' + str(formset.is_valid()))
        print(formset.errors)

        if form.is_valid() & formset.is_valid():
            form_cd = form.cleaned_data
            formset_cd = formset.cleaned_data
            doc_num = form_cd['doc_num']
            doc_date = form_cd['doc_date']
            department = form_cd['department']
            stock = form_cd['stock']

            tableunit_recs = []
            for rec in formset_cd:
                tableunit_recs.append(DocIncomeTableUnit(
                    doc=doc,
                    device=rec['device'],
                    person=rec['person'],
                    qty=rec['qty'],
                    comment=rec['comment']))
                
            DocIncomeTableUnit.objects.filter(doc=doc).delete()
            DocIncomeTableUnit.objects.bulk_create(tableunit_recs)
    else:
        form = DocIncomeForm(instance=doc)
        formset = DocIncomeTableUnitFormSet(queryset=DocIncomeTableUnit.objects.filter(doc=doc))

    return render(request, template_name, {'form': form, 'formset': formset})
