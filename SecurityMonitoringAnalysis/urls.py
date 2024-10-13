"""SecurityMonitoringAnalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

import settings

# from django.conf import settings

urlpatterns = [
    url(r"^", include("interview.urls")),
    url(r"^", include("MonitorTypes.urls")),
    # path('simpleui/', include('simpleui.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')), 
]

from django.conf.urls.static import static
if settings.base:
    from django.conf import settings
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = _('独居女性数据采集分析报警系统')
