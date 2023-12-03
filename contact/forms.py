from django import forms  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from . import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.contrib.auth import password_validation  # type: ignore


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            },
        ),
        required=False,
        label='Imagem'
    )
    first_name = forms.CharField(
        label="Nome",
        help_text='Digite seu primeiro nome apenas'
    )
    last_name = forms.CharField(
        label='Sobrenome'
    )
    phone = forms.CharField(
        label='Telefone'
    )
    email = forms.EmailField(
        label='E-mail'
    )
    description = forms.CharField(
        label='Descrição',
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Escreva aqui'
        })
        # self.fields['description'].widget.attrs.update({
        #     'label': 'Descrição',
        # })

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
            )
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Escreva aqui'
        #         }
        #     )
        # }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'O primeiro e o segundo nome não podem ser iguais',
                    code='invalid'
                )
            )
        # self.add_error(
        #     None,
        #     ValidationError(
        #         'Mensagem de erro', code='invalid'
        #     )
        # )
        # self.add_error(
        #     None,
        #     ValidationError(
        #         'Mensagem de erro2', code='invalid'
        #     )
        # )
        return super().clean()

    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
    #     if first_name == 'ABC':
    #         self.add_error(
    #             'first_name',
    #             ValidationError(
    #                 'Digite um nome válido',
    #                 code='invalid'
    #             )
    #         )

    #     return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        label='Sobrenome',
        required=True,
        min_length=3,
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        min_length=3,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe esse email',
                                code='invalid')
            )
        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo obrigatório',
        error_messages={
            'min_length': 'Por favor, adicione mais que 2 caracteres.'
        }
    )
    last_name = forms.CharField(
        label='Sobrenome',
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo obrigatório',
        error_messages={
            'min_length': 'Por favor, adicione mais que 2 caracteres.',
            'max_length': 'Por favor, adicione menos que 30 caracteres.'
        }
    )
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label='Confirmação de Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Use a mesma senha de antes',
        required=False
    )
    email = forms.EmailField(
        label='E-mail',
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
            'password1', 'password2',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não coincidem  ')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe esse email',
                                    code='invalid')
                )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1
