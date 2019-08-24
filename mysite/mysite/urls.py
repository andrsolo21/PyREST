"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from django.conf.urls import url

from shop import views

#from . import views

#from ..shop import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    #url(r'^$', views.hello),
    #url(r'^qwe/', views.hello2),
    path('imports/', views.importsR),
    path('imports', views.importsR),
    #url(r'^import/([0-9]+)', views.patchImp),
    path('imports/<int:imp>/citizens/<int:cit>', views.patchImpR),
    path('imports/<int:imp>/citizens/<int:cit>/', views.patchImpR),
    path('imports/<int:imp>/citizens', views.getImportR),
    path('imports/<int:imp>/citizens/', views.getImportR),
    path('imports/<int:imp>/citizens/birthdays', views.birthdayR),
    path('imports/<int:imp>/citizens/birthdays/', views.birthdayR),
    path('imports/<int:imp>/towns/stat/percentile/age', views.townBirthdayR),
    path('imports/<int:imp>/towns/stat/percentile/age/', views.townBirthdayR),
    #url(r'^imports/<int:imp>/citizens/5', views.patchImp)
    #url(r'^post/', views.post)
]