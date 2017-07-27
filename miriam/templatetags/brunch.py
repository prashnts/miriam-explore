from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.filter(needs_autoescape=True)
def js_bundle(bundle, autoescape=True):
    fmt = '''
    <script type='text/javascript' src='{url}'></script>
    <script type='text/javascript'>require('{bundle}')();</script>
    '''
    src = 'js/{0}.js'.format(bundle.replace('/', '_'))
    return mark_safe(fmt.format(url=static(src), bundle=bundle))


@register.filter(needs_autoescape=True)
def style_bundle(bundle, autoescape=True):
    fmt = "<link rel='stylesheet' type='text/css' href='{url}'>"
    src = 'css/{0}.css'.format(bundle.replace('/', '_'))
    return mark_safe(fmt.format(url=static(src)))
