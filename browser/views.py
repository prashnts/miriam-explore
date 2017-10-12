from django.shortcuts import render

from browser.utils import get_fixture


def sankey(request):
    expts = get_fixture('browser.exp--tissues.yaml')

    context = {
      'experiments': expts,
    }

    return render(request, 'browser/sankey.html', context)

