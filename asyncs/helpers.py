from datetime import datetime, date
from django.core import serializers
from django.db.models import Model, QuerySet
from django.forms import BaseForm
from django.template import RequestContext

try:
    import json
except ImportError:
    import simplejson as json

class FormEncoder(json.JSONEncoder):
    request = None

    def default(self, obj):
        if isinstance(obj, BaseForm):
            return render_crispy_form(obj, context=RequestContext(self.request))
        elif isinstance(obj, Model):
            result = serializers.serialize('json', [obj])
            return result.strip('[]')
        elif isinstance(obj, datetime):
            return obj.strftime('%d.%m.%Y')
        elif isinstance(obj, date):
            return obj.strftime('%d.%m.%Y')
        elif isinstance(obj, QuerySet):
            return list(obj)

        return json.JSONEncoder.default(self, obj)


def encoder_fabric(request):
    FormEncoder.request = request
    return FormEncoder
