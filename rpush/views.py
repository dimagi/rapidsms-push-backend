from django.http import HttpResponse

from threadless_router.backends.http.views import BaseHttpBackendView
from rpush.forms import PushForm


class PushBackendView(BaseHttpBackendView):
    """ Backend view for handling inbound SMSes from Kannel """

    http_method_names = ['post']
    form_class = PushForm

