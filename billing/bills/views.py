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
            # Retrieve the Profile object with id=1
            profile_obj = Profile.objects.get(id=1)

            # Assign the retrieved profile_obj to the profile field of the form's instance
            form.instance.profile = profile_obj
            form.save()
            return redirect("home")
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
        return queryset.filter(profile__user=self.request.user)


class ProfileListView(ListView):
    model = Profile
    template_name = "bills/profile_list.html"
    context_object_name = "profiles"
