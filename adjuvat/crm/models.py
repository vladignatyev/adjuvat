#!-*- coding: utf-8 -*-
from django.db import models


class Company(models.Model):
    """Модель компании пользователя"""
    hidden = models.BooleanField()

    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    info = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.title, self.address, self.phone)


class Client(models.Model):
    """Модель клиента компании company пользователя"""
    SEX_CHOICES = (('M', 'Male'),
                   ('F', 'Female'))

    hidden = models.BooleanField()

    company = models.ForeignKey('Company')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(choices=SEX_CHOICES, max_length=16)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True)
    mail = models.EmailField(blank=True)

    def __unicode__(self):
        return u"%s: %s %s" % (self.company.title, self.first_name, self.last_name)


class Service(models.Model):
    """Модель услуги предоставляемой компанией пользователя company"""
    hidden = models.BooleanField()

    company = models.ForeignKey('Company')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s: %s" % (self.company.title, self.name)


class Executor(models.Model):
    """Модель исполнителя, производящего услуги компании company"""
    hidden = models.BooleanField()

    company = models.ForeignKey('Company')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    services = models.ManyToManyField('Service')

    def __unicode__(self):
        return u"%s: %s %s" % (self.company.title, self.first_name, self.last_name)


class PricingItem(models.Model):
    """Модель цены услуги service, производимой исполнителем executor"""
    executor = models.ForeignKey('Executor')
    service = models.ForeignKey('Service')
    price = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s: %s %s `%s` за %s Р." % (self.executor.company.title,
                               self.executor.first_name,
                               self.executor.last_name,
                               self.service.name,
                               self.price)


class Order(models.Model):
    """Модель заказа услуги"""
    ORDER_STATUS_CHOICES = (('O', 'Opened'),
                            ('E', 'Executed'),
                            ('C', 'Cancelled'))

    hidden = models.BooleanField()

    client = models.ForeignKey('Client')
    executor = models.ForeignKey('Executor')
    services = models.ManyToManyField('Service')

    calculated_price = models.PositiveIntegerField(blank=True)
    user_price = models.PositiveIntegerField(blank=True)

    planned_time_start = models.DateTimeField()
    planned_time_end = models.DateTimeField()
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=1)






