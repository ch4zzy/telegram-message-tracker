from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, SourceChannel, TargetChannel, User
from .validators import validate_source_target_unique


class SourceChannelForm(forms.ModelForm):
    target_channel = forms.ModelMultipleChoiceField(
        queryset=TargetChannel.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = SourceChannel
        fields = "__all__"
        widget = {"target_channel": forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        target_channels = cleaned_data.get("target_channel")
        if target_channels:
            error_message = validate_source_target_unique(
                self.instance, "pre_add", target_channels
            )
            if error_message:
                self.add_error("target_channel", error_message)
        return cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, required=True, help_text="Enter a valid email address."
    )
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def match_password(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords dont match.")
        return cd["password2"]


class UpdateSourceListForm(forms.ModelForm):
    class Meta:
        model = SourceChannel
        fields = ["name", "source_link"]


class UpdateTargetListForm(forms.ModelForm):
    class Meta:
        model = TargetChannel
        fields = ["name", "source_link"]


class UpdatePostListForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]


class CreateSourceChannelForm(forms.ModelForm):
    class Meta:
        model = SourceChannel
        fields = ["name", "source_link", "active_following"]


class CreateTargetChannelForm(forms.ModelForm):
    class Meta:
        model = TargetChannel
        fields = ["name", "source_link", "auto_post"]
