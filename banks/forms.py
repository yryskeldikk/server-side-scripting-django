from django import forms

from .models import Bank, Branch


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["name", "swift_code", "inst_num", "description"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "id": "bank_name"}
            ),
            "swift_code": forms.TextInput(
                attrs={"class": "form-control", "id": "swift_code"}
            ),
            "inst_num": forms.TextInput(
                attrs={"class": "form-control", "id": "inst_num"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "id": "description"}
            ),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "id": "name"}
            ),
            "transit_num": forms.TextInput(
                attrs={"class": "form-control", "id": "transit_num"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "id": "address"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "email"}),
            "capacity": forms.NumberInput(
                attrs={"class": "form-control", "id": "capacity"}
            ),
        }
