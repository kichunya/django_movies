from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Comment
        fields = ("name", "email", "text")
