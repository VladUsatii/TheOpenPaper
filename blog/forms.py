from django.forms import ModelForm, TextInput, widgets
from .models import City, Comment


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'Add your location'})}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['write_comment']