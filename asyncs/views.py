try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .helpers import encoder_fabric

"""
from pushme.mq import get_sender

sender = get_sender(
    'snakemq',
    ('localhost', 4000)
)
"""


class BaseView(View):

    def render_to_json_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        if isinstance(context, str):
            return HttpResponse(context, **response_kwargs)
        return HttpResponse(
            json.dumps(context,
                       cls=encoder_fabric(self.request)),
            **response_kwargs
        )

    def redirect(self, reverse_name, args=None, **kwargs):
        return HttpResponseRedirect(reverse(reverse_name, args=args), **kwargs)

    def redirect_to_url(self, url, **kwargs):
        return HttpResponseRedirect(url, **kwargs)


class AsyncView(BaseView):
    """ Test view for async exchange
    """
    def dispatch(self, *args, **kwargs):
        return super(AsyncView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise BlockingIOError('GET request is not allowed.')

    def post(self, request, *args, **kwargs):
        msg = request.POST.get('message')
        """
        sender.send(data=msg, topic='send-message')
        """
        return self.render_to_json_response({'message': msg})
