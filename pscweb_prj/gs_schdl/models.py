from django.db import models

class Production(models.Model):
    title = models.CharField('Title of production', max_length=255)
    gs_id = models.CharField('ID of Google spreadsheet', max_length=255)

    def __str__(self):
        return self.title


class Member(models.Model):
    prod_id = models.ForeignKey(Production, on_delete=models.CASCADE)
    name = models.CharField('Name of member', max_length=255)

    def __str__(self):
        return self.name


class Team(models.Model):
    prod_id = models.ForeignKey(Production, on_delete=models.CASCADE)
    name = models.CharField('Name of team', max_length=255)
    members = models.ManyToManyField(Member)

    def __str__(self):
        return self.name

