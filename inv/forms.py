from django import forms
from django.forms import ModelForm, modelformset_factory
from inv.models import *


class DocIncomeForm(ModelForm):
    class Meta:
        model = DocIncome
        fields = ['doc_date', 'doc_num', 'department', 'stock']


DocIncomeTableUnitFormSetBase = modelformset_factory(DocIncomeTableUnit, form=DocIncomeForm, fields=['device', 'person', 'comment'], can_delete=True)




#class DocIncomeTableUnitFormSet(DocIncomeTableUnitFormSetBase):
