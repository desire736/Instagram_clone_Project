from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Комментарий", max_length=1000)
