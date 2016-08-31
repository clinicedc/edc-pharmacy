"""edc_pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from edc_base.views import LoginView, LogoutView
from edc_pharma.views import HomeView
from edc_pharma.admin_site import edc_pharma_admin

urlpatterns = [
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^admin/', edc_pharma_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^edc_label/', include('edc_label.urls', namespace='edc-label')),
    url(r'^edc/', include('edc_base.urls', namespace='edc-base')),
    #url(r'^home/$', 'search.views.home'),
    #url(r'^results/$', 'search.views.search'),
    #url(r'^search-form/$', home.search_form),
    #url(r'^search/$', home.search),
    url(r'^', HomeView.as_view(), name='home_url'),
]
