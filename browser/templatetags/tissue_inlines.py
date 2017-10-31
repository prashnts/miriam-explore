import json
import django.core.serializers.json

from django.template import Library
from django.utils.safestring import mark_safe
from pydash import py_

from browser.utils import get_fixture

register = Library()

# Make a nice-looking identifier for use within js.
make_identifier = lambda id: py_(['np', id]).join('_').camel_case().value()


@register.filter
def humanise(text):
    return py_.human_case(text)

@register.filter(is_safe=True)
def jsonify(object, args=None):
    return json.dumps(object, cls=django.core.serializers.json.DjangoJSONEncoder)

@register.simple_tag
def render_inlined_objects(objects, identifier):
    template = '<script id="{0}" type="application/json">{1}</script>'
    return mark_safe(template.format(identifier, jsonify(objects)))

@register.simple_tag
def render_tissues():
    payload = get_fixture('browser.exp--tissues.yaml')
    uid = make_identifier('tissues')
    return render_inlined_objects(payload, uid)
