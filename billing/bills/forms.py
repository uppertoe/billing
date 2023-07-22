from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.urls import reverse

from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["date", "initials", "dob", "procedure", "items", "profile", "processed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Find the HTMX url
        # The category for searching can be set in the URL
        url_name = "search_items"
        url = reverse(url_name)

        self.fields["items"].widget.attrs["hx-get"] = url
        self.fields["items"].widget.attrs["hx-trigger"] = "changed"
        self.fields["items"].widget.attrs["hx-swap"] = "outerHTML"
        self.fields["items"].widget.attrs["name"] = "q"

        # Define the crispy_forms layout
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Field("date", css_class="datepicker"),  # Assuming you use datepicker CSS class for the date field
            Field("initials"),
            Field("dob", css_class="datepicker"),  # Assuming you use datepicker CSS class for the dob field
            Field("procedure"),
            Field("items", css_class="select2"),
            Field("profile"),
            Field(
                "processed", css_class="datepicker"
            ),  # Assuming you use datepicker CSS class for the processed field
            Submit("submit", "Submit", css_class="btn-primary"),
        )
