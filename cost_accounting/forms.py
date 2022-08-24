from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q


class UserRegister(UserCreationForm):
    """Форма регистрации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'fadeIn third', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Repeat you password'}))
    policy_agree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'policyAgree'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'policy_agree')


class UserAuthentication(AuthenticationForm):
    """Форма атуентификации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))


class AddCategory(forms.ModelForm):
    """Форма добавления новой категории трат"""
    def __init__(self, user, *args, **kwargs):
        super(AddCategory, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control form-control-lg', 'placeholder': 'Например, "Питомцы"...'}
        self.fields['group'].widget.attrs = {'class': 'form-control form-control-lg'}
        self.fields['group'].queryset = Group.objects.filter(user__username=user.username)

    class Meta:
        model = Category
        exclude = ('author', )


class AddSpending(forms.ModelForm):
    """Форма добавления новых расходов"""
    def __init__(self, user, *args, **kwargs):
        super(AddSpending, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(Q(creator__isnull=True) | Q(creator=user)
                                  | Q(group__user=User.objects.get(username=user.username))).distinct()
        self.fields['category'].widget.attrs = {'class': 'form-control form-control-lg'}
        self.fields['amount'].widget.attrs = {'class': 'form-control form-control-lg', 'type': 'number', 'min': 0, 'placeholder': '300...'}

        self.fields['short_description'].widget.attrs = {'class': 'form-control form-control-lg',
                                                         'placeholder': 'Колбаса - 200р, Газировка - 70р, ну и по-мелочи купил...'}

    class Meta:
        model = Spending
        fields = ('category', 'amount', 'short_description')
        exclude = ('payer',)


class CreateGroup(forms.ModelForm):
    """Форма создания новой пользовательской группы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': 'Например, "Команда разработки"'}

    class Meta:
        model = Group
        fields = ('name', )


class CreateGroupInviteForm(forms.ModelForm):
    """Форма создания приглашения пользователя в группу"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['guest'].widget = forms.TextInput(attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': 'Например, "Иннокентий"'})

    class Meta:
        model = InviteToGroup
        fields = ('guest', )
