from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from gmapi.forms.widgets import GoogleMap
from location.models import Activity, Location, Skill, Province

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, MultiField
from crispy_forms.bootstrap import FormActions

import re

class MyInfoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('email'),
            Field('first_name', css_class='input-xlarge'),
            Field('last_name', css_class='input-xlarge'),
            Field('skills', style="background: #FAFAFA; padding: 10px;"),
            Field('other_skills', css_class='input-xlarge'),
            FormActions(
                Submit('save', _('Save'), css_class="btn btn-primary"),
            )
        )        
        super(MyInfoForm, self).__init__(*args, **kwargs)

    email = forms.CharField(label=_('E-mail'), max_length=50, 
        widget=forms.HiddenInput())
    first_name = forms.CharField(label=_('First name'), max_length=50)
    last_name = forms.CharField(label=_('Last name'), max_length=50)
    skills = forms.ModelMultipleChoiceField(
        label=_('Skill'),
        required=False,
        queryset=Skill.objects.all(), 
        widget=forms.widgets.CheckboxSelectMultiple()
    )
    other_skills = forms.CharField(required=False, label=_('Other skills'), max_length=200)

class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('email'),
            Field('old_password', css_class='input-xlarge'),
            Field('new_password1', css_class='input-xlarge'),
            Field('new_password2', css_class='input-xlarge'),
            FormActions(
                Submit('save', _('Save'), css_class="btn btn-primary"),
            )
        )        
        super(UserForm, self).__init__(*args, **kwargs) 

    email = forms.CharField(label=_('E-mail'), max_length=50, 
        widget=forms.HiddenInput())
                
    old_password = forms.CharField(required=False,
        label=_('Password'), widget=forms.PasswordInput()
    )
    
    new_password1 = forms.CharField(required=False,
        label=_('New password'), widget=forms.PasswordInput()
    )

    new_password2 = forms.CharField(required=False,
        label=_('New password (again)'), widget=forms.PasswordInput()
    )
    
    def clean_old_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['old_password']
        if authenticate(email=email, password=password):
            return password
        raise forms.ValidationError(_('Wrong password'))
        
    def clean_new_password2(self):
        if 'new_password1' in self.cleaned_data or 'new_password2' in self.cleaned_data:
            password1 = self.cleaned_data['new_password1']
            password2 = self.cleaned_data['new_password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError(_('Password do not match'))        
        
class RegistrationForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('first_name', css_class='input-xlarge'),
            Field('last_name', css_class='input-xlarge'),
            Field('email', css_class='input-xlarge'),
            Field('password1', css_class='input-xlarge'),
            Field('password2', css_class='input-xlarge'),
            FormActions(
                Submit('register', _('Register'), css_class="btn btn-primary"),
            )
        )
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
    first_name = forms.CharField(label=_('First name'), max_length=50)
    last_name = forms.CharField(label=_('Last name'), max_length=50)
    email = forms.EmailField(label=_('E-mail'))
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=_('Password (again)'), widget=forms.PasswordInput()
    )
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError(_('Password do not match'))
            
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_('E-mail is already taken.'))
        
class MapForm(forms.Form):
    gmap = forms.Field(widget=GoogleMap(attrs={'width':800, 'height':600, 'nojquery':True}))
    
class SearchMapForm(forms.Form):
    gmap = forms.Field(widget=GoogleMap(attrs={'width':380, 'height':400, 'nojquery':True}))
    
class LocationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('place_name', css_class='input-xlarge'),
            Field('status', css_class='input-xlarge'),            
            Field('organization', css_class='input-xlarge'),
            Field('relation', css_class='input-xlarge'),
            Field('phone_number', css_class='input-xlarge'),
            Field('address', rows="4", css_class='input-xlarge'),
            Div('hide_email', 'hide_phone_number', 'hide_address', css_class="privacy_info"),
            Field('latitude', css_class='input-xlarge'),
            Field('longitude', css_class='input-xlarge'),
            Field('city', css_class='input-xlarge'),
            Field('country', css_class='input-xlarge'),
            Field('activities', style="background: #FAFAFA; padding: 10px;"),
            Field('additional_info', rows="8", css_class='input-xlarge'),
            FormActions(
                Submit('save', _('Save'), css_class="btn btn-primary"),
            )
        )        
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['activities'].label = _('Activities')
        self.fields['latitude'].label = _('Latitude')
        self.fields['longitude'].label = _('Longitude')
    
    class Meta:
        model = Location
        fields = (
            'status', 'organization', 'relation',
            'place_name', 'longitude', 'latitude', 
            'address', 'phone_number',
            'hide_email', 'hide_phone_number', 'hide_address',
            'activities', 'additional_info', 'city', 'country')
        widgets = {
            'address': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }
        
    additional_info = forms.CharField(
        label=_('Additional information'),
        required=False,
        widget=forms.Textarea(attrs={'rows':8, 'cols':40}),
        help_text=_('<p class="text-warning">Do not enter any request'
        ' or suggestion into this field. Please use this'
        ' <a href="https://spreadsheets.google.com/viewform?formkey=dFRRZ3djOVVVX3IxYTExUEZDamI3enc6MQ">channel</a> instead.</p>')
    )
    
    city = forms.CharField(        
        widget=forms.widgets.Select(
            choices=map(lambda x: (x.name, x.name),Province.objects.all())
        )
    )
    
    latitude = forms.FloatField(max_value=90, min_value=-90)
    longitude = forms.FloatField(max_value=180, min_value=-180, 
        help_text=_('<p class="text-warning">Please use the map on the right side to locate your place.</p>'))
    activities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Activity.objects.order_by('-priority').all(), 
        widget=forms.widgets.CheckboxSelectMultiple()
    )
