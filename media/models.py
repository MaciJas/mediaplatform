from django.db import models
from typing import List


class Content(models.Model):
    description: str = models.TextField()
    authors: str = models.CharField(max_length=255)
    genre: str = models.CharField(max_length=255)
    rating: float = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    class Meta:
        verbose_name_plural: str = 'Content'

    def __str__(self) -> str:
        return f"{self.authors} - {self.description}"


class FileType(models.Model):
    name: str = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    file_type: FileType = models.ForeignKey(FileType, on_delete=models.CASCADE)
    file: models.FileField = models.FileField(upload_to='content/')

    class Meta:
        verbose_name_plural: str = 'Files'

    def __str__(self) -> str:
        return f"{self.file_type.name} ({self.id})"


class ContentFile(models.Model):
    content: Content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_files')
    file: File = models.ForeignKey(File, on_delete=models.CASCADE, related_name='content_files')

    class Meta:
        verbose_name_plural: str = 'ContentFiles'

    def __str__(self) -> str:
        return f"{self.content.authors} - {self.content.description} ({self.file.file_type.name})"


class Channel(models.Model):
    title: str = models.CharField(max_length=255)
    language: str = models.CharField(max_length=255)
    picture: models.ImageField = models.ImageField(upload_to='channel/', blank=True)
    subchannels: models.ManyToManyField = models.ManyToManyField('self', symmetrical=False, blank=True)
    contents: models.ManyToManyField = models.ManyToManyField(Content, blank=True)

    class Meta:
        verbose_name_plural: str = 'Channels'

    def __str__(self) -> str:
        return self.title

    def rating(self) -> float:
        if self.subchannels.count() == 0:
            contents_rating: float = self.contents.aggregate(models.Avg('rating'))['rating__avg']
            return contents_rating if contents_rating else 0
        else:
            subchannels_rating: float = 0
            for subchannel in self.subchannels.all():
                subchannels_rating += subchannel.rating()
            return subchannels_rating / self.subchannels.count()
