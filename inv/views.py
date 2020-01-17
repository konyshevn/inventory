from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Sum, F
from django.db import models
from django.contrib.contenttypes.models import ContentType
import time, datetime
from inv.config import *
import csv


from inv.models import *
from inv.forms import *
import json
from django.core.cache import caches
from django.core import signing
import operator
from django.db.models import Q

# DRF
from rest_framework import viewsets, status, mixins
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView


DOCUMENT = {
    'income': {'model': DocIncome, 'table_unit': DocIncomeTableUnit, 'form': DocIncomeForm, 'formset': DocIncomeTableUnitFormSet},
    'writeoff': {'model': DocWriteoff, 'table_unit': DocWriteoffTableUnit, 'form': DocWriteoffForm, 'formset': DocWriteoffTableUnitFormSet},
    'move': {'model': DocMove, 'table_unit': DocMoveTableUnit, 'form': DocMoveForm, 'formset': DocMoveTableUnitFormSet},
    'inventory': {'model': DocInventory, 'table_unit': DocInventoryTableUnit, 'form': DocInventoryForm, 'formset': DocInventoryTableUnitFormSet},
    'docincome': {'model': DocIncome, 'table_unit': DocIncomeTableUnit, 'form': DocIncomeForm, 'formset': DocIncomeTableUnitFormSet},
    'docwriteoff': {'model': DocWriteoff, 'table_unit': DocWriteoffTableUnit, 'form': DocWriteoffForm, 'formset': DocWriteoffTableUnitFormSet},
    'docmove': {'model': DocMove, 'table_unit': DocMoveTableUnit, 'form': DocMoveForm, 'formset': DocMoveTableUnitFormSet},
    'docinventory': {'model': DocInventory, 'table_unit': DocInventoryTableUnit, 'form': DocInventoryForm, 'formset': DocInventoryTableUnitFormSet},
}

CATALOG = {
    'device': {'model': Device, 'form': DeviceForm, 'order_by': 'nomenclature'},
    'devicetype': {'model': DeviceType, 'form': DeviceTypeForm, 'order_by': 'label'},
    'nomenclature': {'model': Nomenclature, 'form': NomenclatureForm, 'order_by': 'label'},
    'person': {'model': Person, 'form': PersonForm, 'order_by': 'surname'},
    'department': {'model': Department, 'form': DepartmentForm, 'order_by': 'label'},
    'stock': {'model': Stock, 'form': StockForm, 'order_by': 'label'},
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


class DocumentViewSet(viewsets.ViewSet):
    def destroy(self, request, pk, format=None):
        doc = self.get_object()
        dd = doc.doc_delete()
        if dd['success']:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(dd['data'], status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='next_doc_num')
    def next_doc_num(self, request, pk=None):
        doc_num = self.serializer_class.Meta.model.objects.get_doc_num()
        doc_num_json = json.dumps({'doc_num': doc_num})
        return HttpResponse(doc_num_json)

    @action(detail=False, url_path='get_labels')
    def get_labels(self, *args):
        labels = {}

        for field in self.serializer_class.Meta.model._meta.get_fields():
            if field.name in self.serializer_class.Meta.model._meta.fields:
                labels[field.name] = field.verbose_name

        labels['_model'] = {
            'singular': self.serializer_class.Meta.model._meta.verbose_name.title(),
            'plural': self.serializer_class.Meta.model._meta.verbose_name_plural.title(),
        }
        labels_json = json.dumps(labels)
        return HttpResponse(labels_json)

    @action(detail=True, url_path='get_follower')
    def get_follower(self, request, pk=None):
        doc_leader = self.serializer_class.Meta.model.objects.get(id=pk)
        followers = doc_leader.get_follower
        followers_id = []
        for doc in followers:
            doc_contenttype = ContentType.objects.get_for_model(doc._meta.model)
            followers_id.append({'docId': doc.id, 'docType': doc_contenttype.model})
        return HttpResponse(json.dumps(followers_id))

    @action(detail=True, url_path='get_leader')
    def get_leader(self, request, pk=None):
        doc_current = self.serializer_class.Meta.model.objects.get(id=pk)
        doc_leader = doc_current.get_leader
        doc_leader_contenttype = ContentType.objects.get_for_model(doc_leader._meta.model)
        leader_id = {'docId': doc_leader.id, 'docType': doc_leader_contenttype.model}
        return HttpResponse(json.dumps(leader_id))

    @action(detail=True, url_path='create_follower')
    def create_follower(self, request, pk=None):
        doc_follower_id = []
        doc_current = self.serializer_class.Meta.model.objects.get(id=pk)
        follower_type = self.request.query_params.get('follower_type', None)
        if follower_type is not None:
            follower_model = get_doc_type(follower_type)['model']
            if follower_model:
                doc_follower_id = doc_current.follower_create(model_follower=follower_model)
        return HttpResponse(json.dumps(doc_follower_id))


class CatalogViewSet(viewsets.ViewSet):
    def destroy(self, request, pk, format=None):
        catlg = self.get_object()
        cd = catlg.catlg_delete()
        if cd['success']:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(cd['data'], status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        # Get URL parameter as a string, if exists
        ids = self.request.query_params.get('ids', None)
        query = self.request.query_params.get('query', None)
        fields = self.request.query_params.get('fields', None)

        # Get snippets for ids if they exist
        if ids is not None:
            # Convert parameter string to list of integers
            ids = [int(x) for x in ids.split(',')]
            # Get objects for all parameter ids
            queryset = self.serializer_class.Meta.model.objects.filter(pk__in=ids)

        elif (query is not None) and (fields is not None):
            fields = [str(x) for x in fields.split(',')]
            filter_vals = {}
            for field in fields:
                field_label = '%s__icontains' % field
                filter_vals.update([(field_label, query)])

            list_of_Q = [Q(**{key: val}) for key, val in filter_vals.items()]
            query_filter = reduce(operator.or_, list_of_Q)
            queryset = self.serializer_class.Meta.model.objects.filter(query_filter)

        else:
            # Else no parameters, return all objects
            queryset = self.serializer_class.Meta.model.objects.all()

        return queryset


class RepCurrentLocation(viewsets.ViewSet):
    filter_options = {
        'device': {'type': {'catlg': 'device'}, 'list': True, 'period': False},
        'date_to': {'type': 'date', 'list': False, 'period': True},
        'department': {'type': {'catlg': 'department'}, 'list': True, 'period': False},
        'stock': {'type': {'catlg': 'stock'}, 'list': True, 'period': False},
        'person': {'type': {'catlg': 'person'}, 'list': True, 'period': False},
    }

    def list(self, request):
        filter_vals = request.query_params.get('filter_vals', None)
        filter_vals_j = json.loads(filter_vals)
        return Response([{'report': 'RepCurrentLocation', 'filter_vals': filter_vals_j}])


class DocIncomeViewSet(DocumentViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DocIncomeSerializer
    queryset = DocIncome.objects.all()


class DocWriteoffViewSet(DocumentViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DocWriteoffSerializer
    queryset = DocWriteoff.objects.all()


class DocMoveViewSet(DocumentViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DocMoveSerializer
    queryset = DocMove.objects.all()


class DocInventoryViewSet(DocumentViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DocInventorySerializer
    queryset = DocInventory.objects.all()


class RegDeviceStockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegDeviceStockSerializer
    queryset = RegDeviceStock.objects.all()


class DeviceViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DeviceSerializer
    queryset = Device.objects.all()


class DepartmentViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    queryset = Department.objects.all()


class StockViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.StockSerializer
    queryset = Stock.objects.all()


class PersonViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = Person.objects.all()


class NomenclatureViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.NomenclatureSerializer
    queryset = Nomenclature.objects.all()


class DeviceTypeViewSet(CatalogViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.DeviceTypeSerializer
    queryset = DeviceType.objects.all()


def home(request):
    return render(request, 'index.html')


def selectize_ajax_query(request):
    cache = caches['selectize']
    if 'q' in request.GET:
        q = request.GET['q']
        if 'field_id' not in request.GET:
            raise Http404('No "field_id" provided.')
        field_id = request.GET['field_id']
        try:
            widget_id = signing.loads(field_id)
        except BadSignature:
            raise Http404('Invalid "field_id".')
        widget_attrs = cache.get('selectize_widget_%s' % widget_id)
        if widget_attrs is None:
                raise Http404('field_id not found')
        widget = widget_attrs['cls'](**widget_attrs)

        search_result = widget.filter_queryset(q)
        response_dict = [{'text': str(item), 'value': item.id} for item in search_result]
        json_dict = json.dumps(response_dict)
        return HttpResponse(json_dict)


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
    if request.method == 'POST':
        if 'delete' in request.POST:
            print(dict(request.POST))
            delete_doc_id = [k[7:] for k, v in dict(request.POST).items() if k[0:7] == 'doc_id_']
            print(delete_doc_id)

            doc_exist_follower = []
            for doc_id in delete_doc_id:
                doc = model.objects.get(id=doc_id)
                dd = doc.doc_delete()
                if not dd['success']:
                    doc_exist_follower.append({'id': doc.id, 'name': str(doc)})
            if doc_exist_follower:
                print(doc_exist_follower)
                request.session['doc_delete_errors'] = doc_exist_follower
                doc_delete_status_url = '/doc/%s/status/doc_delete/0' % (doc_name, )
                return HttpResponseRedirect(doc_delete_status_url)

    doc_list = model.objects.all().order_by('-doc_date', '-doc_num')
    template_name = 'doc/%s/%s_list.html' % (doc_name, model.__name__.lower())
    return render(request, template_name, {'doc_list': doc_list})


def doc_delete_status(request, status, doc_name):
    template_name = 'delete_fail.html'
    return render(request, template_name, {'doc_name': doc_name, 'doc_delete_errors': request.session['doc_delete_errors']})


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

        print('form.is_valid() - %s' % form.is_valid())
        print('formset.is_valid() - %s' % formset.is_valid())
        if form.is_valid() & formset.is_valid():

            form_cd = form.cleaned_data
            formset_cd = formset.cleaned_data
            if 'reg_write' in request.POST:
                dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                rd = doc.reg_delete()
                rw = doc.reg_write()
                print(rw)
                if dw['success'] & rd['success'] & rw['success']:
                    print('-' * 50)
                    print('PERIOD total: ' + str(time.time() - start))
                    status_url = '/doc/%s/%s/status/reg_write/1' % (doc_name, doc.id)
                else:
                    request.session['status_errors'] = (dw['data'], rd['data'], rw['data'])
                    status_url = '/doc/%s/%s/status/reg_write/0' % (doc_name, doc.id)

            elif 'reg_delete' in request.POST:
                rd = doc.reg_delete()
                if rd['success']:
                    status_url = '/doc/%s/%s/status/reg_delete/1' % (doc_name, doc.id)
                else:
                    request.session['status_errors'] = (rd['data'],)
                    status_url = '/doc/%s/%s/status/reg_delete/0' % (doc_name, doc.id)

            elif 'doc_write' in request.POST:
                if doc.active:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    rd = doc.reg_delete()
                    rw = doc.reg_write()

                    if dw['success'] & rd['success'] & rw['success']:
                        status_url = '/doc/%s/%s/status/doc_write/1' % (doc_name, doc.id)
                    else:
                        request.session['status_errors'] = (dw['data'], rd['data'], rw['data'])
                        status_url = '/doc/%s/%s/status/doc_write/0' % (doc_name, doc.id)
                else:
                    dw = doc.doc_write(doc_attr=form_cd, table_unit=formset_cd)
                    if dw['success']:
                        status_url = '/doc/%s/%s/status/doc_write/1' % (doc_name, doc.id)
                    else:
                        request.session['status_errors'] = (dw['data'],)
                        status_url = '/doc/%s/%s/status/doc_write/0' % (doc_name, doc.id)
            elif 'doc_inventory_fill_saldo' in request.POST:
                print('doc_inventory_fill_saldo')
                form = form_class(instance=doc)
                fromset_init_data = doc.doc_inventory_fill_saldo(form_cd['department'], form_cd['stock'])
                formset = formset_class(queryset=model.objects.none(), initial=fromset_init_data)
                formset.extra += len(fromset_init_data)
                return render(request, template_name, {'form': form, 'formset': formset, 'active': doc.active})

            elif 'doc_delete' in request.POST:
                dd = doc.doc_delete()
                doc_exist_follower = []
                if not dd['success']:
                    doc_exist_follower.append({'id': doc.id, 'name': str(doc)})
                    request.session['doc_delete_errors'] = doc_exist_follower
                    status_url = '/doc/%s/status/doc_delete/0' % (doc_name, )
                else:
                    status_url = '/doc/%s' % doc_name
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


def follower_manager(request, doc_leader_name, doc_leader_id, doc_follower_name):
    doc_leader_type = get_doc_type(doc_leader_name)
    model_leader = doc_leader_type['model']
    doc_leader = model_leader.objects.get(id=doc_leader_id)
    doc_follower_type = get_doc_type(doc_follower_name)
    model_follower = doc_follower_type['model']
    template_name = 'doc/%s/doc%s_followers_new_list.html' % (doc_leader_name, doc_leader_name)

    doc_follower_id = doc_leader.follower_create(doc_follower_name=doc_follower_name, model_follower=model_follower)
    return render(request, template_name, {'doc_leader': str(doc_leader), 'doc_follower_name': doc_follower_name, 'doc_follower_id': doc_follower_id})


def follower_hierarchy(request, doc_leader_name, doc_leader_id):
    doc_leader_type = get_doc_type(doc_leader_name)
    model_leader = doc_leader_type['model']
    doc_leader = model_leader.objects.get(id=doc_leader_id)
    template_name = 'doc/follower_hierarchy.html'
    #print(doc_leader.get_leader)
    return render(request, template_name, {'doc_leader': doc_leader, 'doc_up_leader': doc_leader.get_leader})


# форма списка справочника
def catlg_list(request, catlg_name):
    catlg_type = get_catlg_type(catlg_name)
    if not catlg_type:
        return HttpResponseRedirect('/catlg_type_error/')
    model = catlg_type['model']

    if request.method == 'POST':
        if 'delete' in request.POST:
            print(dict(request.POST))
            delete_catlg_id = [k[9:] for k, v in dict(request.POST).items() if k[0:9] == 'catlg_id_']
            print(delete_catlg_id)

            catlg_exist_ref = []
            for catlg_id in delete_catlg_id:
                catlg = model.objects.get(id=catlg_id)
                cd = catlg.catlg_delete()
                if cd['success']:
                    catlg_exist_ref.append({'id': catlg.id, 'name': str(catlg)})
            if catlg_exist_ref:
                print(catlg_exist_ref)
                request.session['catlg_delete_errors'] = catlg_exist_ref
                catlg_delete_status_url = '/catlg/%s/status/catlg_delete/0' % (catlg_name, )
                return HttpResponseRedirect(catlg_delete_status_url)

    catlg_list = model.objects.all().order_by(catlg_type['order_by'])
    template_name = 'catlg/%s/%s_list.html' % (catlg_name, model.__name__.lower())
    return render(request, template_name, {'catlg_list': catlg_list, 'model': model})


def catlg_delete_status(request, status, catlg_name):
    template_name = 'catlg_delete_fail.html'
    return render(request, template_name, {'catlg_name': catlg_name, 'catlg_delete_errors': request.session['catlg_delete_errors']})


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
                if cw['success']:
                    status_url = '/catlg/%s/%s/status/catlg_write/1' % (catlg_name, catlg.id)
                else:
                    request.session['status_errors'] = cw['data']
                    status_url = '/catlg/%s/%s/status/catlg_write/0' % (catlg_name, catlg.id)
            elif 'catlg_delete' in request.POST:

                cd = catlg.catlg_delete()
                catlg_exist_ref = []
                if cd['success']:
                    catlg_exist_ref.append({'id': catlg.id, 'name': str(catlg)})
                    request.session['catlg_delete_errors'] = catlg_exist_ref
                    status_url = '/catlg/%s/status/catlg_delete/0' % (catlg_name, )
                else:
                    status_url = '/catlg/%s' % catlg_name
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


def report_current_location(request):
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
                filter_vals['department'] = Department.objects.get(id=cd['department'])

            if not cd['stock'] == '' and not cd['stock'] is None:
                filter_vals['stock'] = Stock.objects.get(id=cd['stock'])

            if not cd['person'] == '' and not cd['person'] is None:
                filter_vals['person'] = Person.objects.get(id=cd['person'])

            for device in devices:
                location_rec = RegDeviceStock.objects.current_location(device=device, date=date_to)
                filter_diff = DictDiffer(location_rec, filter_vals)
                if len(filter_diff.changed()) == 0:
                    location_rec['department'] = str(location_rec['department'])

                    if location_rec['stock'] is None:
                        location_rec['stock'] = ''
                    else:
                        location_rec['stock'] = str(location_rec['stock'])

                    if location_rec['person'] is None:
                        location_rec['person'] = ''
                    else:
                        location_rec['person'] = str(location_rec['person'])
                    location_rec['device'] = str(device)
                    location.append(location_rec)
    else:
        form = ReportCurrentLocationForm()

    template_name = 'report/current_location.html'
    return render(request, template_name, {'location': location, 'form': form})


def report_statement_docs(request):
    location = []
    filter_vals = {}
    if request.method == 'POST':
        form = ReportStatementDocsForm(request.POST)
        #print(form)
        if form.is_valid():
            cd = form.cleaned_data
            if not cd['device'] == '' and not cd['device'] is None:
                filter_vals['device'] = Device.objects.get(id=cd['device'])
                print(form['device'])
                print(cd['device'])
                

            if not cd['date_to'] == '' and not cd['date_to'] is None:
                filter_vals['reg_date__lte'] = cd['date_to'] + datetime.timedelta(days=1)
            if not cd['date_from'] == '' and not cd['date_from'] is None:
                filter_vals['reg_date__gte'] = cd['date_from']

            reg_recs = RegDeviceStock.objects.filter(**filter_vals).order_by('-reg_date')

            for row in reg_recs:
                location_rec = {}
                doc_multi_operation = row.base_doc._REG_CONST_ATTR_MAP['RegDeviceStock']['_MULTI']

                if row.operation_type == '+':
                    location_rec['base_doc'] = str(row.base_doc)
                    location_rec['base_doc_id'] = row.base_doc.id
                    location_rec['base_doc_type'] = row.base_doc._meta.model_name[3:]
                    location_rec['qty'] = RegDeviceStock.objects.saldo(device=row.device, date_to=row.reg_date)
                    location_rec['department'] = str(row.department)

                    if row.stock is None:
                        location_rec['stock'] = ''
                    else:
                        location_rec['stock'] = str(row.stock)

                    if row.person is None:
                        location_rec['person'] = ''
                    else:
                        location_rec['person'] = str(row.person)
                    location_rec['date'] = row.reg_date
                elif not doc_multi_operation:
                    location_rec['base_doc'] = str(row.base_doc)
                    location_rec['base_doc_id'] = row.base_doc.id
                    location_rec['base_doc_type'] = row.base_doc._meta.model_name[3:]
                    location_rec['qty'] = RegDeviceStock.objects.saldo(device=row.device, date_to=row.reg_date)
                    location_rec['department'] = ''
                    location_rec['stock'] = ''
                    location_rec['person'] = ''
                    location_rec['date'] = row.reg_date
                else:
                    continue
                location.append(location_rec)

    else:
        form = ReportStatementDocsForm()

    template_name = 'report/statement_docs.html'
    return render(request, template_name, {'location': location, 'form': form})


def upload_file_success(request):
    return render_to_response('upload_file/upload_success.html',)


def upload_file_fail(request):
    return render_to_response('upload_file/upload_fail.html',)


def handle_uploaded_file(f):
    try:
        file_path = file_dir + f.name
        destination = open(file_path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as err:
        return (False, str(err))
    else:
        return (True, file_path)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            huf = handle_uploaded_file(request.FILES['file'])
            cd = form.cleaned_data
            doc_date = cd['date']

            if huf[0]:
                doc_income_attr = {}
                doc_num = DocIncome.objects.get_doc_num() - 1
                with open(huf[1], newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for line in reader:
                        doc_attr = {}
                        department = Department.objects.filter(name=line['Department_name'])
                        if department:
                            department = department[0]
                        elif line['Department_name'] != '':
                            department = Department(name=line['Department_name'])
                            department.save()
                        else:
                            return HttpResponseRedirect('/upload_file/fail')

                        if not str(department) in doc_income_attr:
                            doc_num = doc_num + 1
                            doc_attr['doc_num'] = doc_num
                            doc_attr['doc_date'] = doc_date
                            doc_attr['department'] = department
                            doc_income_attr[str(department)] = {'doc_attr': doc_attr, 'table_unit': []}

                        person = Person.objects.filter(surname=line['Person_surname'], name=line['Person_name'])
                        if person:
                            person = person[0]
                        elif (line['Person_name'] != '') & (line['Person_surname'] != ''):
                            person = Person(name=line['Person_name'], surname=line['Person_surname'], department=department)
                            person.save()
                        else:
                            return HttpResponseRedirect('/upload_file/fail')

                        deviceType = DeviceType.objects.filter(name=line['Device_deviceType'])
                        if deviceType:
                            deviceType = deviceType[0]
                        elif (line['Device_deviceType'] != ''):
                            deviceType = DeviceType(name=line['Device_deviceType'])
                            deviceType.save()
                        else:
                            return HttpResponseRedirect('/upload_file/fail')

                        nomenclature = Nomenclature.objects.filter(name=line['Device_name'])
                        if nomenclature:
                            nomenclature = nomenclature[0]
                        elif (line['Device_name'] != ''):
                            nomenclature = Nomenclature(name=line['Device_name'])
                            nomenclature.save()
                        else:
                            return HttpResponseRedirect('/upload_file/fail')

                        device = Device.objects.filter(serial_num=line['Device_serial_num'], inv_num=line['Device_inv_num'])
                        if device:
                            device = device[0]
                        else:
                            device = Device(serial_num=line['Device_serial_num'], inv_num=line['Device_inv_num'], name=nomenclature, deviceType=deviceType, comment=line['Device_comment'])
                            device.save()
                        
                        table_unit_rec = {}
                        table_unit_rec['id'] = None
                        table_unit_rec['device'] = device
                        table_unit_rec['person'] = person
                        table_unit_rec['qty'] = 1
                        doc_income_attr[str(department)]['table_unit'].append(table_unit_rec)

                for dep, attr in doc_income_attr.items():
                    doc_income = DocIncome()
                    doc_income.doc_write(doc_attr=attr['doc_attr'], table_unit=attr['table_unit'])
                return HttpResponseRedirect('/upload_file/success')
            else:
                print('huf - False')
                return HttpResponseRedirect('/upload_file/fail')
    else:
        form = UploadFileForm()
    template_name = 'upload_file/upload_form.html'
    return render(request, template_name, {'form': form})


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