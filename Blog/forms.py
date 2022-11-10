from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea)
