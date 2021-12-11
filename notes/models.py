from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    noteName = models.CharField('Título', max_length=50)
    createDate = models.DateTimeField(default=timezone.now)
    description = models.CharField('Descrição', max_length=50)
    noteInformation = models.TextField('Informações da nota')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.user)}_{slugify(self.noteName)}'
            self.slug = slug

        super().save(*args,**kwargs)

    def __str__(self):
        return self.noteName

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"