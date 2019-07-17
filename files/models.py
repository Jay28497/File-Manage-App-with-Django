from django.db import models


# Create your models here.
class Document(models.Model):
    file_name = models.CharField(max_length=30)
    document = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
