from django import forms
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from django.contrib.auth.forms import UserCreationForm as UCF
from .models import User, Experience


class DateInput(forms.DateInput):
    input_type = 'date'


class UserCreationForm(UCF):
    class Meta(UCF.Meta):
        model = User


class ExpUser(forms.ModelForm):
    class Meta:
        model = Experience
        # fields = ("title", "company", "start_date",
        #           "end_date", "present", "description")
        exclude = ('user',)
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            # 'description': CKEditorWidget()
        }

    def __init__(self, *args, **kwargs):
        super(ExpUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.render_hidden_fields = True
        self.helper.render_required_fields = True
        self.helper.render_unmentioned_fields = True
    #     self.layout = Layout(
    #         # Row(HTML(
    #         #     "{% if forloop.first %}Message displayed only in the first form of a formset forms list{% endif %}"),
    #         #     Fieldset("Total Experience {{ forloop.counter }}",
    #                      Row(Field('title')),
    #                      Row(Field('company')),
    #                      Row(Field('description')),
    #                      Row(Field('start_date')),
    #                      Row(Field('end_date')),
    #                      Row(Field('present'))

    #         # HTML("{% if forloop.last %}<input type='submit' name='Done'>{% endif %}")
    #     )
    #     # self.render_required_fields = True
    #     # self.helper.form_id = 'ExpChangeForm'
    #     # self.helper.form_method = 'post'
    #     # self.render_required_fields = True
