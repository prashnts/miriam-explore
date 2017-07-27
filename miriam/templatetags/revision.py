import os

from django import template
from django.conf import settings
from dealer.git import git

register = template.Library()

@register.simple_tag
def revision(prod=False):
    if 'HEROKU_SLUG_COMMIT' in os.environ:
      rev = os.environ['HEROKU_SLUG_COMMIT'][:7]
    else:
      rev = git.revision if git.revision else 'unknown'

    if settings.DEBUG or settings.STAGING:
      channel = 'staging' if settings.STAGING else 'dev'
      return '#%s @%s' % (rev, channel)
    else:
      return ''
