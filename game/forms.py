from typing import Any
from django import forms
from game.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class AnswerInlineFormer(forms.BaseInlineFormSet):
    def clean(self):
        super(AnswerInlineFormer,self).clean()

        is_correct_answer = 0
        for answer_form in self.forms:
            if not answer_form.is_valid():
                return
            if answer_form.cleaned_data and answer_form.cleaned_data.get('is_correct') is True:
                is_correct_answer += 1
        try:
            assert  is_correct_answer == Question.NUMBER_OF_ACCEPTED_ANSWER
        except AssertionError:
            raise forms.ValidationError('Somente uma resposta é permitida')
    


class QuizUserLogin(forms.Form):
    username = forms.CharField(label='',help_text='Utilizador',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Informe um utilizador'}))
    password = forms.CharField(label='',help_text='Senha',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Informe uma senha'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)

            if not user:
                raise forms.ValidationError('Utilizador e/ou Senha inválidos.')
            if not user.check_password(password):
                raise forms.ValidationError('Password errada...')
            if not user.is_active:
                raise forms.ValidationError('Este Jogador não está activo')
        return super(QuizUserLogin, self).clean(*args, **kwargs)




class QuizUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(required=True,label='Nome',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True,label='Sobrenome',widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Utilizador',help_text='Obrigatório. 150 carateres ou menos. Apenas letras, dígitos @/./+/-/_.',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Palavra-passe',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmação da palavra-passe',help_text='Introduza a palavra-passe como acima, para verificação.',widget=forms.PasswordInput(attrs={'class':'form-control'}))


    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ] 


class DefficultyForm(forms.Form):
    difficulty = forms.ModelChoiceField(queryset=Difficulty.objects.all(), label='Saleccione o nível', widget=forms.Select,)
    class Meta:
        model = Difficulty
        fields = '__all__'
    