# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class Crypto(models.Model):
    cryptoName = models.CharField(
        max_length=64, primary_key=True, unique=True)

    class Meta:
        db_table = 'crypto'
        verbose_name = 'Crypto Currency'
        verbose_name_plural = 'Crypto Currencies'

    def __str__(self):
        return self.cryptoName


class Commerce(models.Model):
    commerce_name = models.CharField(max_length=256)
    rif = models.PositiveIntegerField(primary_key=True, unique=True)
    email = models.EmailField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    tlf = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    cryptos = models.ManyToManyField(
        Crypto, through='Transaction', related_name='commerces', blank=True)

    class Meta:
        db_table = 'commerce'
        verbose_name = 'Commerce'

    def __str__(self):
        return self.commerce_name


class Worker(AbstractUser):
    second_name = models.CharField(max_length=50, blank=True, null=True)
    second_last_name = models.CharField(max_length=50, blank=True, null=True)
    ci = models.CharField(max_length=8, primary_key=True, unique=True)
    tlf = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(null=True)
    city = models.CharField( max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    commerce = models.ForeignKey(
        Commerce, related_name='commerce', on_delete=models.CASCADE, blank=True,null=True)

    REQUIRED_FIELDS = ['email', 'ci', 'commerce']

    class Meta:
        db_table = 'worker'
        verbose_name = 'Worker'
        unique_together = ("ci", "commerce")

    def __str__(self):
        return self.ci


class Admin(Worker):

    class Meta:
        db_table = 'admin'
        verbose_name = 'Commerce Admin'

    def __str__(self):
        return "Administrador %s. CI-%s." % (self.first_name, self.ci)


class Cashier(Worker):
    admin = models.ManyToManyField(
        Admin, related_name='admin', blank=True)

    class Meta:
        db_table = 'cashier'
        verbose_name = 'Commerce Cashier'

    def __str__(self):
        return "Cajero: %s. CI-%s." % (self.first_name, self.ci)


class Transaction(models.Model):
    # Class self-attributes
    ref_num = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    amount_bs = models.DecimalField(max_digits=100, decimal_places=2)
    amount_crypto = models.DecimalField(max_digits=100, decimal_places=8)
    tx_id = models.CharField(max_length=256, unique=True)

    # Class dependencies
    commerce = models.ForeignKey(Commerce, on_delete=models.CASCADE)
    cashier = models.ForeignKey(
        Worker, related_name='transaction', on_delete=models.CASCADE)
    crypto = models.ForeignKey(
        Crypto, related_name='transaction', on_delete=models.CASCADE)

    class Meta:
        db_table = 'transaction'
        unique_together = ("commerce", "ref_num")
        verbose_name = 'Transaction'

    def __str__(self):
        return "Trans. #%s @ %s." % (str(self.ref_num), self.commerce)
