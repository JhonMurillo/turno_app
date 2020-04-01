from django import forms

from turnos.models import Turno

class TurnoForm(forms.ModelForm):

    # def save(self):
    #     print('save form..')
    #     data = self.cleaned_data
    #     print(data)
    #     # data.pop('password_confirmation')

    #     # user = User.objects.create_user(**data)
    #     # profile = Profile(user=user)
    #     # profile.save()

    class Meta:

        model = Turno
        fields= ('asesor', 'cliente')

    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']
        print(cliente)
        if cliente != None:
            raise forms.ValidationError('Ingrese su nombre.')
        return cliente