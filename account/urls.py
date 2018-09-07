from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views as v
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', v.index, name='index'),
    url(r'^account/signup.html$', v.signup, name='signup'),
    url(r'^account/login.html$', v.login, name='login'),
    url(r'^account/(?P<userEmail>.*)/postlist.html$', v.postlist, name='postlist'),
    url(r'^account/(?P<userEmail>.*)/userhome.html$', v.userhome, name='userhome'),
    url(r'^account/(?P<postId>.*)/post.html$', v.post, name='post'),
    url(r'^account/(?P<postId>.*)/editpost.html$', v.editpost, name='editpost'),
    url(r'^account/(?P<userEmail>.*)/newpost.html$', v.newpost, name='newpost'),
    url(r'account/(?P<apptReviewID>[0-9]+)/delete$', v.deletepost, name='deletepost')


]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
