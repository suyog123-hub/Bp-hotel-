from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,EmailValidator
from django.utils import timezone
# Create your models here.
class MenuTitle(models.Model):
    title=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.title

class  menu_items(models.Model):
    category=models.ForeignKey(MenuTitle,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=200,null=True)
    desc=models.TextField(null=True)
    price=models.IntegerField()

class gallery_img(models.Model):
    image=models.ImageField(upload_to="gallery",null=True)

class review1(models.Model):
    desc=models.TextField(null=True)
    name=models.CharField(max_length=200)
    short_desc=models.CharField(max_length=200,null=True)


class Reserve(models.Model):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True,validators=[EmailValidator()])
    phone=models.IntegerField(null=True)
    number_of_people=models.PositiveBigIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)],default=1)
    date=models.DateField()
    time=models.TimeField()
    request1=models.TextField()
    is_confirmed=models.BooleanField(default=False)

