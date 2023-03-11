from django.db import models

# Create your models here.
class MedicineDet(models.Model):
    medadd = models.CharField(max_length=100)
    medowner = models.CharField(max_length=50)
    medcontact = models.CharField(max_length=20) 
    medshop = models.CharField(max_length=100)
    medname = models.CharField(max_length=100)
    medextra = models.CharField(max_length=50)
    medpow = models.CharField(max_length=100)
    medquan = models.CharField(max_length=50)
    medexp = models.CharField(max_length=100)

    def __str__(self):
        return self.medshop + '->' + self.medname
