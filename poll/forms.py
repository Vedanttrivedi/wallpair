from django import forms
from .models import Questions
from django.contrib.auth.forms import UserCreationForm


class QuestionCreateForm(forms.ModelForm):
	class Meta:
		model = Questions
		fields = ['question','image1','image2']

