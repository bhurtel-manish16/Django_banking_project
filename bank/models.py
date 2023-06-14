from django.db import models

# Create your models here.
class Payment(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=120)
    account_number = models.IntegerField()
    cureent_amount = models.CharField(max_length=14)

    def __str__(self):
        return self.name

class Tranactions(models.Model):
    acc_no = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=2, default="")
    date = models.DateTimeField()
    description = models.CharField(max_length=100)
    amount = models.CharField(max_length=100000000000000000000)
    balance_history  =models.CharField(max_length=14, default=0)
    

    def __str__(self):
        return self.acc_no