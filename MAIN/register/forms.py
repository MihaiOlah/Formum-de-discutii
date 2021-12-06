from django import forms
from django import forms
from main.models import Author

# Aici vom actualiza profilul
# Se vor actualiza campurile de nume, biografie si poza de profil
class UpdateForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ("fullName", "bio", "profile_pic")