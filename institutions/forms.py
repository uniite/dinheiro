from django import forms

from institutions.models import Institution


class InstitutionForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = Institution
