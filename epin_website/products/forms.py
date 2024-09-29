from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="İstifadəçi adı")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="İstifadəçi adı")
    email = forms.EmailField(label="E-poçt", required=True)  # E-poçt sahəsini əlavə edin
    password = forms.CharField(max_length=20, label="Parol", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parol Təsdiqi", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parollar uyğunlaşmır")

        return cleaned_data
    

class SearchForm(forms.Form):
    query = forms.CharField(label='Axtarış', max_length=100)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)