from django import forms 

class PathForm(forms.Form):
    PathForm = forms.CharField(required=True,label='image_path',max_length=255,strip=True,)
    