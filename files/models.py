from django.db import models


class File(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    class Meta:
        db_table = 'files'
