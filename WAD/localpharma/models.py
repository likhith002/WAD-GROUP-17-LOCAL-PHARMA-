from django.db import models
from django.conf import  settings
# Create your models here.


class pharmacyowner(models.Model):
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email= models.CharField(max_length=254)

    license_file = models.FileField(null=True)
    permission_file = models.FileField(null=True)
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = models.CharField(max_length=6 ,choices=gender_choices)
    
    phone1=models.CharField(max_length=10)
    phone2=models.CharField(max_length=10)
    
    shopname = models.CharField(max_length=50)
    DOB=models.DateField()

    city = models.CharField(max_length=250)
    streetno=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    pincode=models.CharField(max_length=6)


class customer(models.Model):

    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email= models.CharField(max_length=254)

    
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = models.CharField(max_length=6 ,choices=gender_choices)
    
    phone1=models.CharField(max_length=10)
    phone2=models.CharField(max_length=10)
    

    DOB=models.DateField()

    city = models.CharField(max_length=250)
    streetno=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    pincode=models.CharField(max_length=6)



class contactus(models.Model):
    name = models.CharField(max_length=255)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=255)
    query=models.CharField(max_length=255)



class pharmacymedicine(models.Model):
    eid=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    quantity=models.CharField(max_length=255)
    mid=models.CharField(max_length=255)
    pin=models.CharField(max_length=6)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone1 = models.CharField(max_length=10)
    city = models.CharField(max_length=250)
    streetno = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    shopname = models.CharField(max_length=50)


class medicine(models.Model):
    manufacturer_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_composition = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    pack_size_label = models.CharField(max_length=100, blank=True, null=True)
    isprescriptionrequired = models.CharField(db_column='isPrescriptionRequired', max_length=30, blank=True, null=True)  # Field name made lowercase.
    url_to_scrape = models.CharField(max_length=255, blank=True, null=True)
    side_effects=models.CharField(max_length=1000,blank=True,null=True)
    alternate_brands=models.CharField(max_length=1000,blank=True,null=True)
    benefits=models.CharField(max_length=1000,blank=True,null=True)
    uses=models.CharField(max_length=1000,blank=True,null=True)
    storage_conditions=models.CharField(max_length=1000,blank=True,null=True)
    salt_composition=models.CharField(max_length=1000,blank=True,null=True)


