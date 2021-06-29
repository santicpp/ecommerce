from django.forms.models import ModelForm
from App_Inicio.models import Producto
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

#alta de producto
class FormNuevoProducto(ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'imagen', 'descripcion', 'precio', 'categoria']
        exclude = ['title']
    descripcion = forms.CharField(widget= forms.Textarea, label="body",required=True)
