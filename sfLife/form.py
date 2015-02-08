from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    hcp = forms.BooleanField(label='Hospitals and Clinics')
    food = forms.BooleanField(label='Food')
    schools = forms.BooleanField(label='Schools')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['hcp'].required = False
        self.fields['food'].required = False
        self.fields['schools'].required = False


# from django import forms
# from .models import Search

# class SearchForm(forms.ModelForm): #PostForm is the name of our form and ModelForm is a template form by Django
#     class Meta: #where we tell Django which model should be used to create (like rails form_for)
#         model = Search
#         fields = ('name', 'hcp', 'food', 'schools')