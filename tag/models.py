from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
import string
from random import SystemRandom

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    # Campos para relação generica
    # Representa o model que queremos encaixar aqui
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Representa o id da linha do model descrito acima
    object_id = models.CharField(max_length=100)

    # Um campo que representa a relação genérica que conhece os campos acima
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name