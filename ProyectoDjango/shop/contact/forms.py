from django import forms

# Se crea el formulario que se mostrara en la pagina que consta de 3 campos nombre,correo y comentarios.
class contactForm(forms.Form):
    name = forms.CharField(required = False, max_length= 100 , help_text='100 caract. max')
    email = forms.EmailField(required = True)
    comment = forms.CharField(required = True, widget = forms.Textarea)