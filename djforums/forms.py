from django.forms import ModelForm
from .models import UserProfile,Defaultimg

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user',]
class DefaultimgForm(ModelForm):
	class Meta:
		model = Defaultimg