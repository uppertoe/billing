from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView

from .forms import CaseForm
from .models import Case, Item, Profile


def search_items(request, category=None):
    if request.headers.get("HX-Request") == "true":
        query = request.GET.get("q", "")
        items = Item.search(query, category=category)
        template = "bills/items_list"
        context = {"items": items}
        return HttpResponse(render_to_string(template, context, request=request))
    else:
        return HttpResponseBadRequest("This URL is for use with HTMX")


@login_required
def create_case(request):
    if request.method == "POST":
        form = CaseForm(request.POST)

        if form.is_valid():
            # Set the Profile to the user
            instance = form.save(commit=False)
            instance.profile = Profile.objects.get(user=request.user)
            form.save()

            return redirect("case_list")
    else:
        form = CaseForm()

    return render(request, "bills/case_form.html", {"form": form})


class CaseListView(LoginRequiredMixin, ListView):
    model = Case
    template_name = "bills/case_list.html"
    context_object_name = "cases"

    # Restrict to own cases
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(profile__user=self.request.user).prefetch_related("items")


class ProfileListView(ListView):
    model = Profile
    template_name = "bills/profile_list.html"
    context_object_name = "profiles"
    queryset = Profile.objects.all().prefetch_related("cases__items")
