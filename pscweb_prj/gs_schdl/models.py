from django.db import models

# Create your models here.
class Production(models.Model):
    title = models.CharField('Title of production', max_length=255)
    gs_id = models.CharField('ID of Google spreadsheet', max_length=255)

    def __str__( self):
        return self. title
