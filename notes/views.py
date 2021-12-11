from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from . import models

from . import forms

class NotesView(View):
    template_name = 'notes/homeNotes.html'
    paginate_by = 10

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        user = self.request.user

        notes = models.Notes.objects.all().filter(user=user)

        self.context = {
            'notes': notes,
        }

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

class CreateNoteView(View):
    template_name = 'notes/createNote.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.context = {
            'createNoteForm': forms.NoteForm(data=self.request.POST or None),
        }

        self.noteForm = self.context['createNoteForm']

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.noteForm.is_valid():
            return self.render
        else:
            if self.request.user.is_authenticated:
                note = self.noteForm.save(commit=False)
                note.user = self.request.user
                note.save()
                return redirect('notes:create')
            else:
                return redirect('profile:login')

    def get(self, *args, **kwargs):
        return self.render


class DeleteView(View):
    def get(self, *args, **kwargs):
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            return redirect('notes:notes')

        notes = models.Notes.objects.filter(id=variation_id).delete()
        self.request.session.save()
        return redirect('notes:notes')

class UpdateView(View):
    template_name = 'notes/update.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.id_note = self.request.GET.get('vid')

        self.note = models.Notes.objects.filter(id=self.id_note).first()

        self.context = {
            'updateNote':forms.NoteForm(data=self.request.POST or None, instance=self.note),
        }

        self.noteForm = self.context['updateNote']

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.noteForm.is_valid():
            return self.render
        else:
            noteName = self.noteForm.cleaned_data.get('noteName')
            description = self.noteForm.cleaned_data.get('description')
            noteInformation = self.noteForm.cleaned_data.get('noteInformation')

            if self.request.user.is_authenticated:
                user = get_object_or_404(User, username=self.request.user.username)

                note = models.Notes.objects.all().filter(id=self.id_note)
                note.noteName = noteName
                note.description = description
                note.noteInformation = noteInformation
                self.note.save()

        return redirect('notes:notes')

    def get(self, *args, **kwargs):
        return self.render

class NoteDetailsView(DetailView):
    model = models.Notes
    template_name = 'notes/details.html'
    context_object_name = 'notes'
    slug_url_kwarg = 'slug'