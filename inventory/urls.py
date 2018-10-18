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
from django.urls import path, re_path
import inv.views
import inv.models

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', inv.views.main),
    re_path('doc/income/$', inv.views.doc_list, {'model': inv.models.DocIncome}),
    re_path('doc/move/$', inv.views.doc_list, {'model': inv.models.DocMove}),
    re_path('doc/writeoff/$', inv.views.doc_list, {'model': inv.models.DocWriteoff}),
    re_path('doc/income/(?P<doc_id>\d+)/$', inv.views.doc_form, {'model': inv.models.DocIncome}),
]
