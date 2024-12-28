from django import forms
from .models import SourceChannel, TargetChannel
from .validators import validate_source_target_unique


class SourceChannelForm(forms.ModelForm):
    target_channel = forms.ModelMultipleChoiceField(
        queryset=TargetChannel.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = SourceChannel
        fields = '__all__'
        widget = {
            'target_channel': forms.CheckboxSelectMultiple
        }


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
    