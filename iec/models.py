from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.
DESC=(
    ('Book','Book'),
    ('Fliers','Fliers'),
    ('Poster','Poster'),
    ('Notebook','Notebook'),
    ('Booklet','Booklet'),
   
)
class Book(models.Model):
    name=models.CharField(max_length=200,null=True, blank=True,default='IEC materirals')
    def __str__(self):
        return self.name
class Iec(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.ForeignKey(Book,on_delete=models.CASCADE)
    description = models.CharField(choices=DESC,null=True, blank=True,max_length=200)
    thematic=models.CharField('thematic',null=True,blank=True,max_length=200)
    copies=models.IntegerField(null=True,blank=True,default=0)

    issued = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    
    class Meta:
        order_with_respect_to = 'created'