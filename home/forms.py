from django import forms
from .models import Comment, AuthorProfile, Question, blogModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from froala_editor.widgets import FroalaEditor


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]

    content = forms.CharField(widget=FroalaEditor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))


class blogForm(forms.ModelForm):
    class Meta:
        model = blogModel
        fields = ["title", "content", "summary", "tags", "image", "published_at"]

    content = forms.CharField(widget=FroalaEditor)
    summary = forms.CharField(widget=FroalaEditor)
    published_at = forms.DateField(widget=FroalaEditor, input_formats=["%d/%m/%Y"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["name", "email", "phone", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class FormProfile(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ("bio", "instagram")

    placeholders = {"bio": "Something about you...", "instagram": "Your Instagram..."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        for field_name, field in self.fields.items():
            if field_name in self.placeholders:
                self.fields[field_name].widget.attrs["placeholder"] = self.placeholders[
                    field_name
                ]

        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))
