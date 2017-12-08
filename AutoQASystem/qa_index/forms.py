from django import forms


class AddQuestion(forms.Form):
    question_title = forms.CharField()
    question_desc = forms.CharField()