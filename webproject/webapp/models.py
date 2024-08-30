from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)
    active_date = models.CharField(max_length=255)
    renewal_date = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    days = models.CharField(max_length=255)
    # status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.service_type} - {self.service_name} - {self.active_date} - {self.renewal_date} - {self.owner} - {self.email} - {self.contact} - {self.days}"


class Account(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.email} - {self.name} - {self.contact} - {self.password}"


class DeletedUsers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)
    active_date = models.CharField(max_length=255)
    renewal_date = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    days = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.service_type} - {self.service_name} - {self.active_date} - {self.renewal_date} - {self.owner} - {self.email} - {self.contact} - {self.days} - {self.status}"

