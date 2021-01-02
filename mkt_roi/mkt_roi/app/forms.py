from django import forms
from .models import MKTOffLine
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MKTOfflineForm(forms.ModelForm):
    canales = ['Impresos']#, 'TV', 'Radio', 'Exteriores', 'Otros']
    subcanales = ['Periódico Coppel']
    Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
    #Unidad_de_negocio = ['Retail', 'Servicios financieros', 'Atención a grupo coppel',
    #                     'Nuevos formatos']
    Segmentos = ['Ropa', 'Muebles', 'Zapatos', 'Crédito Coppel', 'Préstamo personal', 
    	'Coppel Pay', 'Seguros (Club de Protección)', 'Coppel Motos', 'Fashion Market', 'Plan de lealtad']

    objetivos = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=list(map(lambda x: (x, x),Objetivos_macro)  )  )
    segmentos = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=list(map(lambda x: (x, x), Segmentos)  )  )
    
    class Meta:
        model = MKTOffLine
        fields = "__all__"

 
