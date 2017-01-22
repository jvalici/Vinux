from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# models.py

class ContactInfo(models.Model):
    postalAdrress = models.CharField(max_length=200)
    email =  models.EmailField()
    webSiteAddress = models.URLField()
    telephoneNumber = models.CharField(max_length=200)

class WineProducer(models.Model):
    name = models.CharField(max_length=200)
    contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    
class WineProductionArea(models.Model):
    name = models.CharField(max_length=200)
    
class WineType(models.Model):
    type = models.CharField(max_length=200)
    productionArea = models.ForeignKey(WineProductionArea)
    
class WineBottle(models.Model):
    producer = models.ForeignKey(WineProducer)
    type = models.ForeignKey(WineType)
    name = models.CharField(max_length=200)
    vintage = models.PositiveSmallIntegerField( validators=[MinValueValidator(1900), MaxValueValidator(2100)] )

class WineCellar(models.Model):
    owner = models.ForeignKey(User, editable = False)
    
class StoredWineBottle(models.Model):
    vineCellar = models.ForeignKey(WineCellar)
    bottle = models.ForeignKey(WineBottle)
    
class WineBottleReview(models.Model):
    bottle = models.ForeignKey(WineBottle)
    user = models.ForeignKey(User, editable = False)
    reviewText = models.TextField()
    mark = models.PositiveSmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(20)] )