#!-*- coding: utf-8 -*-
from django.db import models


class Company(models.Model):
    """Модель компании пользователя"""
    hidden = models.BooleanField()

    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    info = models.TextField()
    address = models.TextField()


class Client(models.Model):
    """Модель клиента компании company пользователя"""
    SEX_CHOICES = (('NA', 'N/A'),
                   ('M', 'Male'),
                   ('F', 'Female'))

    hidden = models.BooleanField()

    company = models.ForeignKey('Company')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(choices=SEX_CHOICES, max_length=16)
    birth_date = models.DateField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    mail = models.EmailField(blank=True)


class Service(models.Model):
    """Модель услуги предоставляемой компанией пользователя company"""
    hidden = models.BooleanField()

    company = models.ForeignKey('Company')
    name = models.CharField(max_length=255)


class Executor(models.Model):
    """Модель исполнителя, производящего услуги компании company"""
    hidden = models.BooleanField()

    company = models.ForeignKey('Company')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    services = models.ManyToManyField('Service')


class PricingItem(models.Model):
    """Модель цены услуги service, производимой исполнителем executor"""
    executor = models.ForeignKey('Executor')
    service = models.ForeignKey('Service')
    price = models.PositiveIntegerField()


class Order(models.Model):
    """Модель заказа услуги"""
    ORDER_STATUS_CHOICES = (('O', 'Opened'),
                            ('E', 'Executed'),
                            ('C', 'Cancelled'))

    hidden = models.BooleanField()

    client = models.ForeignKey('Client')
    executor = models.ForeignKey('Executor')
    services = models.ManyToManyField('Service')
    calculated_price = models.PositiveIntegerField()
    user_price = models.PositiveIntegerField()

    planned_time = models.DateTimeField()
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=1)






