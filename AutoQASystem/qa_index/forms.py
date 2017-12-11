from django import forms


class AddQuestion(forms.Form):
    question_title = forms.CharField()
    question_desc = forms.CharField()


class CommentForm(forms.Form):
    comment = forms.CharField(min_length=1)