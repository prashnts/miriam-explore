from django.urls import reverse
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

PAGING_CELLS = 9
PAGING_MID_CELL = PAGING_CELLS // 2

default_page = {'active': False, 'nr': None, 'ellipsis': False}
page = lambda **kwargs: {**default_page, **kwargs}


def get_paging_elements(current, size):
    '''Generates pagination buttons with ellipsis'''
    if size > PAGING_CELLS:
        pages = [page() for _ in range(PAGING_CELLS)]
        # Fill in first and last positions
        pages[0] = page(nr=1)
        pages[1] = page(nr=2)
        pages[PAGING_CELLS - 2] = page(nr=size - 1)
        pages[PAGING_CELLS - 1] = page(nr=size)

        if current <= PAGING_MID_CELL:
            # 'b' ellipse is enabled and the rest of the list is filled
            pages[PAGING_CELLS - 2] = page(ellipsis=True)
            for i in range(2, PAGING_CELLS - 2):
                pages[i] = page(nr=i + 1)
        elif (size - current) < PAGING_MID_CELL:
            # 'a' ellipse is enabled and the later part of the list is filled
            pages[1] = page(ellipsis=True)
            for i in range(2, PAGING_CELLS - 2):
                pages[i] = page(nr=size - PAGING_CELLS + i + 1)
        else:
            # both a and b ellipsis are enabled
            pages[1] = page(ellipsis=True)
            pages[PAGING_CELLS - 2] = page(ellipsis=True)

            # Current selected is put in centre
            pages[PAGING_MID_CELL] = page(nr=current)
            # Fill next and prev to mid point
            # CELL_COUNT - 5 := n{MID, FIRST, SECOND, LAST, SECONDLAST}
            for i in range(1, PAGING_CELLS - 6):
                pages[PAGING_MID_CELL + i] = page(nr=current + i)
                pages[PAGING_MID_CELL - i] = page(nr=current - i)
    else:
        pages = [page(nr=i + 1) for i in range(0, size)]

    for pg in pages:
        if pg['nr'] == current:
            pg['active'] = True

    return pages


@register.simple_tag
def render_tables_paginator(sample_id, current, size):
    pages = get_paging_elements(current, size)
    page_url = lambda page: reverse('browser_tables', kwargs={'sample_id': sample_id, 'page': page})

    prev_url = page_url(current - 1) if current > 1 else '#'
    next_url = page_url(current + 1) if current < size else '#'

    buttons = []
    buttons.append(f'<a role="button" class="pt-button pt-icon-arrow-left" href="{prev_url}"></a>')

    for page in pages:
        if page['ellipsis']:
            buttons.append('<a role="button" class="pt-button pt-icon-more" href="#"></a>')
        else:
            active = 'pt-active' if page['active'] else ''

            button = f'<a role="button" class="pt-button {active}" href="{page_url(page["nr"])}">{page["nr"]}</a>'
            buttons.append(button)

    buttons.append(f'<a role="button" class="pt-button pt-icon-arrow-right" href="{next_url}"></a>')

    buttons_rendered = '\n'.join(buttons)
    btn_group = f'<div class="pt-button-group np-paginator">{buttons_rendered}</div>'
    return mark_safe(btn_group)
