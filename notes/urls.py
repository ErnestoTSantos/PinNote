from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.NotesView.as_view(), name='notes'),
    path('create/', views.CreateNoteView.as_view(), name='create'),
    path('delete/', views.DeleteView.as_view(), name='delete'),
    path('update/', views.UpdateView.as_view(), name='update'),
    path('<slug>/', views.NoteDetailsView.as_view(), name='details'),
]