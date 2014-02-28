from threadless_router.backends.http.views import BaseHttpBackendView
from threadless_router.celery.tasks import IncomingTask
from rpush.forms import PushForm
from lxml import etree
from django.http import QueryDict, HttpRequest, HttpResponse


class PushBackendView(BaseHttpBackendView):
    """ Backend view for handling inbound SMSes from Kannel """

    http_method_names = ['post']
    form_class = PushForm

    def form_valid(self, form):
        self.debug('form is valid')
        IncomingTask.delay(self.backend_name, **form.get_incoming_data())
        return HttpResponse('OK')


    def get_form_kwargs(self):
        xml = etree.fromstring(HttpRequest.read(self.request))

        kwargs = {
            'initial': self.get_initial(),
            'data': QueryDict('')
        }
        if self.request.method in ('POST', 'PUT'):
            needed_keys = ['MobileNumber', 'Text']
            post_args = []

            for element in xml:
                if element.attrib['name'] in needed_keys:
                    value = element.text or ''
                    post_args.append(element.attrib['name'] + '=' + value)

            kwargs['data'] = QueryDict('&'.join(post_args))

        return kwargs
