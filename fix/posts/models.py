import uuid

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField


class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True)


class Meta:
    bd_table = "users"
    ordering = ["-created_at"]
    indexes = [models.Index(fields=("created_at",), name="created_at_index")]
    indexes = [models.Index(fields=("title",), name="title_index")]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)



def upload_to(instance: "Note", filename: str):
    return f"{instance.uuid}/{filename}"


class Note(models.Model):
    objects = None
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255,verbose_name="Заголовок")
    content = RichTextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_to, null=True,blank=True, verbose_name="Превью")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,verbose_name="Пользователь")
    objects = models.Manager

    tags = models.ManyToManyField(Tag, related_name='notes',verbose_name="Теги")



#
def __str__(self):
    return f'Заметка: "{self.title}"'


@receiver(post_delete, sender=Note)
def after_delete_note(sender, instance: Note, **kwargs):
    if instance.image:
        note_media_folder = settings.MEDIA_ROOT / str(instance.uuid)
        for file in note_media_folder.glob("*"):
            file.unlink(missing_ok=True)
        note_media_folder.rmdir()
