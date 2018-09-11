from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views as v
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^signup$', v.signup, name='signup'),
    url(r'^$', v.login, name='login'),
    url(r'^login$', v.login, name='login'),
    url(r'^logout$', v.logout,  name='logout'),
    url(r'^(?P<employeeEmail>.*)/postlist$', v.postlist, name='postlist'),
    url(r'^(?P<employeeEmail>.*)/employeehome$', v.employeehome, name='employeehome'),
    url(r'^(?P<postId>.*)/post$', v.post, name='post'),
    url(r'^(?P<postId>.*)/editpost$', v.editpost, name='editpost'),
    url(r'^(?P<employeeEmail>.*)/newpost$', v.newpost, name='newpost'),
    url(r'^(?P<postId>[0-9]+)/delete$', v.deletepost, name='deletepost')


]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
