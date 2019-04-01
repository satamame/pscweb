"""pscweb_prj URL Configuration

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
from django.urls import path, include

from accounts.views import profile

urlpatterns = [
    path('', profile, name='root'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # 上の include については、「Djangoの認証システムを使用する」参照
    # https://docs.djangoproject.com/ja/2.0/topics/auth/default/
    path('scripts/', include('scripts.urls')),
    path('gs_schdl/', include('gs_schdl.urls')),
    path('admin/', admin.site.urls),
]
