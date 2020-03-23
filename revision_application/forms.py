from django import forms

# # # # # # # #
# Upload File #
# # # # # # # #


class UploadImageForm(forms.Form):
    file = forms.ImageField()


class UploadPdfForm(forms.Form):
    file = forms.FileField()


# # # # # # # #
# Reg & login #
# # # # # # # #


class LoginForm(forms.Form):
    username = forms.CharField(label="username:", required=True)
    password = forms.CharField(label="password:", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username:", required=True)
    password1 = forms.CharField(label="password:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="re-enter password:", widget=forms.PasswordInput)
    email = forms.EmailField(label="email:", required=True)

    def clean_password2(self):
        print(self)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2


