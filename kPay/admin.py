# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Crypto, Commerce, Cashier, Admin, Transaction, Worker

# Register your models here.
admin.site.register(Crypto)
admin.site.register(Commerce)
admin.site.register(Worker)
admin.site.register(Cashier)
admin.site.register(Admin)
admin.site.register(Transaction)
