from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="İstifadəçi adı")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="İstifadəçi adı")
    email = forms.EmailField(label="E-poçt", required=True)  # E-poçt sahəsi
    password = forms.CharField(max_length=20, label="Parol", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parol Təsdiqi", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parollar uyğunlaşmır")

        return cleaned_data
