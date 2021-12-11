from django import forms

from . import models

class NoteForm(forms.ModelForm):

    class Meta:
        model = models.Notes
        fields = ('noteName', 'description', 'noteInformation')
        exclude = ('user', 'createDate', 'slug')