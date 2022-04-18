from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

class EmailPostForm(forms.Form):  
    name = forms.CharField(max_length=25)  
    email = forms.EmailField()  
    to = forms.EmailField()  
    comments = forms.CharField(required=False, widget=forms.Textarea)