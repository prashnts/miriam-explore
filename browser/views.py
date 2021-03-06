import pandas as pd
import math

from annoying.decorators import render_to
from django.http.response import HttpResponse

from browser.utils import get_fixture, get_sample

DEFAULT_SAMPLE_ID = 'emtab2919-adrenal_gland'
SAMPLE_CHUNK_SIZE = 500

experiments = get_fixture('browser.exp--tissues.yaml')


@render_to('browser/sankey.html')
def sankey(request):
    return {
        'experiments': experiments,
    }


@render_to('browser/tables.html')
def tables(request, sample_id=DEFAULT_SAMPLE_ID, page=1):
    if page < 1:
        page = 1

    sample = get_sample(sample_id)

    chunk = slice(SAMPLE_CHUNK_SIZE * (page - 1), SAMPLE_CHUNK_SIZE * page)

    table = sample.loc[chunk].to_html(border=0, classes='pt-table pt-striped pt-condensed np-table')
    return {
        'sample_id': sample_id,
        'current': page,
        'page_max': math.ceil(len(sample) / SAMPLE_CHUNK_SIZE),

        'experiments': experiments,
        'table': table,
    }


def tables_download(request, sample_id):
    sample = get_sample(sample_id)
    csv = sample.to_csv(mode='b')
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=miriam-explore--{sample_id}.csv'
    return response
