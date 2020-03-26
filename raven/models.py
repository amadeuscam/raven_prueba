from django.db import models
from django.core.files.storage import FileSystemStorage
import hashlib

# Create your models here.
from django.shortcuts import redirect


class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name
        else:
            return super(MediaFileSystemStorage, self)._save(name, content)







class RavenFiles(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=100)
    r_file = models.FileField(storage=MediaFileSystemStorage())
    md256sum = models.CharField(max_length=36)

    def __str__(self):
        return self.created

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md256 = hashlib.sha256()
            for chunk in self.r_file.chunks():
                md256.update(chunk)
            self.md256sum = md256.hexdigest()
        super(RavenFiles, self).save(*args, **kwargs)


