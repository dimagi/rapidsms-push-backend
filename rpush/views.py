from django.http import HttpResponse

from threadless_router.backends.http.views import BaseHttpBackendView
from rpush.forms import PushForm
from lxml import etree
from django.http import QueryDict

class PushBackendView(BaseHttpBackendView):
    """ Backend view for handling inbound SMSes from Kannel """

    http_method_names = ['post']
    form_class = PushForm

    def rebuild_xml_string_from_request(self):
        """
        Hack.

        The xml submitted to the endpoint gets broken up in a query dict
        on submission so we have to put these back together (replacing the
        '=' that it was originally split on) then encode it with utf-8 so
        that it can be processed by lxml.
        """

        return '='.join(self.request.POST.iteritems().next()).encode('utf-8')

    def get_form_kwargs(self):
        rebuilt_xml = self.rebuild_xml_string_from_request()
        xml = etree.fromstring(rebuilt_xml)

        kwargs = {
            'initial': self.get_initial(),
            'data': QueryDict('')
        }
        if self.request.method in ('POST', 'PUT'):
            needed_keys = ['MobileNumber', 'Text']
            post_args = []
            for element in xml:
                if element.attrib['name'] in needed_keys:
                    post_args.append(element.attrib['name'] + '=' + element.text)

            kwargs['data'] = QueryDict('&'.join(post_args))

        return kwargs
