"""
URL configuration for fix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include,re_path
from django.contrib.auth.views import LoginView
from django.conf.urls.static import serve
from django.conf import settings

from posts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include("django.contrib.auth.urls")),
    path('accounts/register',views.register,name="register"),
    path("",views.home_page_views ,name="home"),
    path("filter", views.filter_notes_views ,name="filter-notes"),
    path("create", views.create_note_views ,name="create-note"),
    path("note/<note_uuid>", views.show_note_views, name="show-note"),
    # path("note/<note_uuid>/edit", views.edit_note_views, name="edit-note"),
    path("note/<note_uuid>/delete", views.delete_note_views, name="delete-note"),
    re_path(r"^media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
