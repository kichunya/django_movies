from django import forms

from .models import Comment, Rating, Stars
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    """Форма отзыва"""
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=Stars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star", )
