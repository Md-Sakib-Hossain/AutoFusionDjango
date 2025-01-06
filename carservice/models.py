from django.db import models

# Create your models here.
class ServiceList(models.Model):
    name=models.CharField(max_length=25,blank=False,null=False)
    email=models.EmailField()
    service=models.CharField(max_length=25,blank=False,null=False)
    date=models.DateField()

    status = models.CharField(max_length=20, default='Pending')
    a_status = models.CharField(max_length=10, default='Pending')

    
    def __str__(self):
        return self.name



class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='insertservice')
    learn=models.URLField(max_length=200, default='https://example.com')


    def __str__(self):
        return self.title

