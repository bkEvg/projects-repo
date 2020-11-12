from django import forms
from .models import Color




colors = [('{}'.format(color.name), '{}'.format(color.name)) for color in Color.objects.all()]

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField()
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
	color = forms.TypedChoiceField(choices=colors)