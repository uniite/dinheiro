from django import forms

from finance.models import Institution


class InstitutionForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = Institution
