from django.contrib.auth.models import AbstractUser
from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from .models import Crypto, Commerce, Worker, Transaction, Admin, Cashier


class CryptoResource(ModelResource):
    class Meta:
        queryset = Crypto.objects.all()
        resource_name = 'crypto'
        filtering = {
            'cryptoName': ('exact','iexact',)
        }
        authorization = Authorization()


class CommerceResource(ModelResource):
    class Meta:
        queryset = Commerce.objects.all()
        resource_name = 'commerce'
        filtering = {
            'rif': ('exact',)
        }
        authorization = Authorization()


class WorkerResource(ModelResource):
    commerce = fields.ForeignKey(CommerceResource, 'commerce')

    class Meta:
        queryset = Worker.objects.all()
        resource_name = 'worker'
        authorization = Authorization()
        max_limit = 0
        limit = 100
        excludes = ['is_active', 'is_staff', 'is_superuser',
                    'last_login', 'password', 'resource_uri', 'username']
        filtering = {
            'commerce': ALL_WITH_RELATIONS,
            'ci': ('exact',)
        }


class TransactionResource(ModelResource):
    worker = fields.ForeignKey(WorkerResource, 'worker')
    crypto = fields.ForeignKey(CryptoResource, 'crypto')
    commerce = fields.ForeignKey(CommerceResource, 'commerce')

    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'
        filtering = {
            'worker': ALL_WITH_RELATIONS,
            'commerce': ALL_WITH_RELATIONS,
            'crypto': ALL_WITH_RELATIONS
        }
        authorization = Authorization()
