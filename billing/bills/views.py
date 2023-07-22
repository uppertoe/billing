from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render  # noqa
from django.template.loader import render_to_string

from .models import Item


def search_items(request, category=None):
    if request.headers.get("HX-Request") == "true":
        query = request.GET.get("q", "")
        items = Item.search(query, category=category)
        template = "bills/items_list"
        context = {"items": items}
        return HttpResponse(render_to_string(template, context, request=request))
    else:
        return HttpResponseBadRequest("This URL is for use with HTMX")
