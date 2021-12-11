from django import forms 
from django.contrib.auth.models import User

from . import models

class UserFormCreate(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    password_2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmation password'
    )

    def __int__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password_2', 'email',)

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_data_2 = cleaned.get('password_2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_shot = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório!'

        if user_db:
            validation_error_msgs['username'] = error_msg_user_exists

        if email_db:
            validation_error_msgs['email'] = error_msg_email_exists

        if not password_data:
            validation_error_msgs['password'] = error_msg_required_field

        if not password_data_2:
            validation_error_msgs['password_2'] = error_msg_required_field

        if password_data:
            if password_data != password_data_2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_2'] = error_msg_password_match
                    
            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_shot

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('date', 'cpf', 'country')
        exclude = ('user',)


class UserFormUpdate(forms.ModelForm):
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
    )

    password_2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmation password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password_2', 'email',)

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        username_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_data_2 = cleaned.get('password_2')

        user_db = User.objects.filter(username=username_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_shot = 'Sua senha precisa de pelo menos 6 caracteres'

        if username_data != user_db.username:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

        if email_data != user_db.email:
            if user_db.email:
                validation_error_msgs['email'] = error_msg_email_exists

        if password_data:
            if password_data != password_data_2:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password_2'] = error_msg_password_match
                    
            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_shot
