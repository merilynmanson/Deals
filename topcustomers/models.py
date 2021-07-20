from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()
    file_name = models.CharField(max_length=150)

    class Meta:
        db_table = 'deals'


class Customer(models.Model):
    name = models.CharField(max_length=150)
    spent_money = models.IntegerField()
    gems = models.TextField(max_length=150)
    file_name = models.CharField(max_length=150)

    class Meta:
        db_table = 'customers'
