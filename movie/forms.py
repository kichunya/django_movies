from django import forms

from .models import Comment, Rating, Stars


class CommentForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Comment
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=Stars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star", )
