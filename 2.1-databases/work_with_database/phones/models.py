from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    price = models.IntegerField()
    release_date = models.DateTimeField()
    lte_exists  = models.BooleanField()
    slug = models.SlugField()