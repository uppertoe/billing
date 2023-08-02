from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Case, Item


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["date", "age", "age_unit", "procedure", "start", "end"]
        widgets = {
            "date": forms.DateInput(format=("%Y-%m-%d"), attrs={"type": "date", "format": "dd/mm/yyyy"}),
            "start": forms.TimeInput(attrs={"type": "time"}),
            "end": forms.TimeInput(attrs={"type": "time"}),
            "age_unit": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["base_item"] = forms.ModelChoiceField(queryset=Item.get_base_items())
        self.fields["modifier_items"] = forms.ModelMultipleChoiceField(
            queryset=Item.get_modifier_items(), required=False
        )
        self.fields["extra_items"] = forms.ModelMultipleChoiceField(queryset=Item.get_extra_items(), required=False)

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
        self.helper.form_method = "POST"

    def save(self, commit=True):
        case_instance = super().save(commit=False)

        # Get the ManyToMany fields
        base_item = self.cleaned_data["base_item"]
        modifier_items = self.cleaned_data.get("modifier_items", [])
        extra_items = self.cleaned_data.get("extra_items", [])

        items = [base_item] + list(modifier_items) + list(extra_items)

        # Futher validation can be performed here

        if commit:
            case_instance.save()
            case_instance.items.set(items)

        return case_instance
