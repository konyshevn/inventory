"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
import inv.views
import inv.models
import inv.forms
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve


from rest_framework import routers
router = routers.DefaultRouter()
router.register('docincome', inv.views.DocIncomeViewSet)
router.register('docwriteoff', inv.views.DocWriteoffViewSet)
router.register('docmove', inv.views.DocMoveViewSet)
router.register('docinventory', inv.views.DocInventoryViewSet)
router.register('regdevicestock', inv.views.RegDeviceStockViewSet)
router.register('device', inv.views.DeviceViewSet)
router.register('department', inv.views.DepartmentViewSet)
router.register('stock', inv.views.StockViewSet)
router.register('person', inv.views.PersonViewSet)
router.register('deviceType', inv.views.DeviceTypeViewSet)
router.register('nomenclature', inv.views.NomenclatureViewSet)
router.register('report/RepCurrentLocation', inv.views.RepCurrentLocation, base_name='RepCurrentLocation')
router.register('report/RepStatementDocs', inv.views.RepStatementDocs, base_name='RepStatementDocs')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('main/', inv.views.main),
    # re_path('selectize_ajax_query/', inv.views.selectize_ajax_query, name='selectize_ajax_query'),
    # path('doc_type_error/', inv.views.doc_type_error),
    # path('catlg_type_error/', inv.views.catlg_type_error),
    # path('reg_type_error/', inv.views.reg_type_error),
    # path('upload_file/', inv.views.upload_file),
    # path('upload_file/success', inv.views.upload_file_success),
    # path('upload_file/fail', inv.views.upload_file_fail),
    # re_path('doc/(?P<doc_name>\w+)/$', inv.views.doc_list),
    # re_path('doc/(?P<doc_name>\w+)/(?P<doc_id>\w+)/$', inv.views.doc_form),
    # re_path('(?P<obj_type_name>\w+)/(?P<obj_name>\w+)/(?P<obj_id>\w+)/status/(?P<operation>\w+)/(?P<status>\d)/$', inv.views.operation_status),
    # re_path('doc/(?P<doc_name>\w+)/status/doc_delete/(?P<status>\d)$', inv.views.doc_delete_status),
    # re_path('catlg/(?P<catlg_name>\w+)/status/catlg_delete/(?P<status>\d)$', inv.views.catlg_delete_status),
    # re_path('catlg/(?P<catlg_name>\w+)/$', inv.views.catlg_list),
    # re_path('catlg/(?P<catlg_name>\w+)/(?P<catlg_id>\w+)/$', inv.views.catlg_form),
    # re_path('doc/(?P<doc_name>\w+)/(?P<doc_id>\w+)/reg/$', inv.views.doc_reg_recs),
    # re_path('^report/current_location/$', inv.views.report_current_location),
    # re_path('^report/statement_docs/$', inv.views.report_statement_docs),
    # re_path('doc/(?P<doc_leader_name>\w+)/(?P<doc_leader_id>\w+)/follower/new/(?P<doc_follower_name>\w+)/$', inv.views.follower_manager),
    # re_path('doc/(?P<doc_leader_name>\w+)/(?P<doc_leader_id>\w+)/follower/hierarchy/$', inv.views.follower_hierarchy),
    path('api/', include(router.urls)),
    re_path('^.*$', TemplateView.as_view(template_name="index.html"), name="home"),
]
