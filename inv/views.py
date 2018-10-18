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
    form = DocIncomeForm(instance=doc)
    formset = DocIncomeTableUnitFormSet(queryset=DocIncomeTableUnit.objects.filter(doc=doc))
    return render(request, template_name, {'form': form, 'formset': formset})
