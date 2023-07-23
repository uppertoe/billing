from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.forms.widgets import DateInput, TimeInput

from .models import Case, Item

# from django.urls import reverse


class CaseForm(forms.ModelForm):
    base_items = forms.ModelChoiceField(queryset=Item.get_base_items())
    procedures = forms.ModelChoiceField(queryset=Item.get_procedures())
    modifiers = forms.ModelChoiceField(queryset=Item.get_modifiers())

    class Meta:
        model = Case
        fields = ["date", "initials", "dob", "procedure", "start", "end"]
        widgets = {
            "date": DateInput(attrs={"type": "date", "format": "%d-%m-%Y"}),
            "dob": DateInput(attrs={"type": "date"}),
            "start": TimeInput(attrs={"type": "time"}),
            "end": TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Find the HTMX url
        # The category for searching can be set in the URL
        # url_name = "search_items"
        # url = reverse(url_name)

        # self.fields["items"].widget.attrs["hx-get"] = url
        # self.fields["items"].widget.attrs["hx-trigger"] = "changed"
        # self.fields["items"].widget.attrs["hx-swap"] = "outerHTML"
        # self.fields["items"].widget.attrs["name"] = "q"

        # Define the crispy_forms layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "date",
            "initials",
            "dob",
            "procedure",
            "start",
            "end",
            "base_items",
            "procedures",
            "modifiers",
            Submit("submit", "Save"),
        )

    def save(self, commit=True):
        case_instance = super().save(commit=False)

        # Get the ManyToMany fields
        base_items = self.cleaned_data.get("base_items", [])
        procedures = self.cleaned_data.get("procedures", [])
        modifiers = self.cleaned_data.get("modifiers", [])

        # Futher validation can be performed here

        # Exclude empty items
        items = [item_list for item_list in [base_items, procedures, modifiers] if item_list]

        if commit:
            case_instance.save()
            case_instance.items.set(items)

        return case_instance
