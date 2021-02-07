"""bmat_works URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from works import views as views

router = routers.DefaultRouter()
# CRUD
router.register(r'works', views.WorkViewSet)
router.register(r'contributors', views.ContributorViewSet)
router.register(r'sources', views.SourceViewSet)
# Other views
router.register(r'import_csv', views.ImportCSVViewSet, basename='import_csv')
router.register(r'export_csv', views.ExportCSVViewSet, basename='export_csv')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
