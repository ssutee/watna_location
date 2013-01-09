from django_messages.forms import ComposeForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, MultiField
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.models import User

class MyComposeForm(ComposeForm):
    
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('recipient', css_class='input-xlarge'),
            Field('subject', css_class='input-xlarge'),
            Field('body', css_class='input-xlarge'),
            FormActions(
                Submit('save', _('Save'), css_class="btn btn-primary"),
            )
        )        
        super(MyComposeForm, self).__init__(*args, **kwargs)
        
    def clean_recipient(self):
        return [self.cleaned_data['recipient']]