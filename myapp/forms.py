from django import forms
from myapp.models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('name','email','user_type','password','clickup_id')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name'}),
            'email':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'user_type':forms.Select(attrs={'class':'form-control', 'placeholder':'User type'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'clickup_id':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter clickup id'}),
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = CustomUser.objects.get(email=email)
            print(match)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError("this email address already use")

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user