from django.conf.urls.defaults import *

from rpush import views


urlpatterns = patterns('',
    url(r"^(?P<backend_name>[\w-]+)/?$", views.PushBackendView.as_view(),
        name='push-backend'),
)
