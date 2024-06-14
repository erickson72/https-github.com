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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)

            if not user:
                raise forms.ValidationError('Jogador não encontrado...')
            if not user.check_password(password):
                raise forms.ValidationError('Password errada...')
            if not user.is_active:
                raise forms.ValidationError('Este Jogador não está activo')
        return super(QuizUserLogin, self).clean(*args, **kwargs)




class QuizUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email')
    first_name = forms.CharField(required=True,label='Nome')
    last_name = forms.CharField(required=True,label='Sobrenome')

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
