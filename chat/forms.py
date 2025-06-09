from django import forms
from chat.models import Chat, Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["name", "avatar"]


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content', 'media']
        widgets = {
            "media": forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'avatar']