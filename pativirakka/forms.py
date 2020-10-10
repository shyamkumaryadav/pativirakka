from django import forms
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from django.contrib.auth.forms import UserCreationForm as UCF
from .models import User, Experience


class DateInput(forms.DateInput):
    input_type = 'date'


class UserCreationForm(UC
    F):
    class Meta(UCF.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ExpUser(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ('user',)
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            # 'description': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ExpUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.render_hidden_fields = True
        self.helper.render_required_fields = True
        self.helper.render_unmentioned_fields = True
        self.helper.layout = Layout(
            Row(Column('title'), Column('company')),
            Row(Column('start_date'), Column(
                PrependedText('end_date', '<button type="button" class="close" aria-label="Close" onclick="window.tag_id=this.parentNode.parentNode.parentNode.getElementsByTagName(\'input\')[0].id.split(\'-\').slice(0, -1);window.tag_id.push(\'end_date\');document.getElementById(tag_id.join(\'-\')).value = \'\';"><span aria-hidden="true">&times;</span></button>', active=True))),
            Row('description')
        )
