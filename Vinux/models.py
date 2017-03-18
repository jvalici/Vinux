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
    name = models.CharField(max_length=200, primary_key=True)
    includingArea = models.ForeignKey('self',blank=True, null=True)
    
class WineType(models.Model):
    appelation = models.CharField(max_length=200)
    color = models.CharField(max_length=1,choices=(('w', 'white'),('r','red'),('p','pink'))) #w: white, r: red, p:pink
    productionArea = models.ForeignKey(WineProductionArea)
    
class WineBottle(models.Model):
    producer = models.ForeignKey(WineProducer)
    type = models.ForeignKey(WineType)
    name = models.CharField(max_length=200)
    vintage = models.PositiveSmallIntegerField( validators=[MinValueValidator(1900), MaxValueValidator(2100)] )
    
class BottleUserReview(models.Model):
    user = models.ForeignKey(User)
    bottle = models.ForeignKey(WineBottle)
    mark = models.PositiveSmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(20)] )
    pairing = models.TextField()
    comment = models.TextField()
    
class BottleWebReview(models.Model):
    bottle = models.ForeignKey(WineBottle)
    link = models.URLField()

class WineCellar(models.Model):
    owner = models.ForeignKey(User)
    
class StoredWineBottle(models.Model):
    vineCellar = models.ForeignKey(WineCellar)
    bottle = models.ForeignKey(WineBottle)
    priceIn = models.DecimalField(decimal_places=2, max_digits=7,  validators=[MinValueValidator(0)])
    
