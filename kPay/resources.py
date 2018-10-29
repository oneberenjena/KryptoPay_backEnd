from django.contrib.auth.models import AbstractUser
from .models import Crypto, Commerce, Worker, Transaction, Admin, Cashier
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.utils import trailing_slash
from tastypie.http import HttpUnauthorized, HttpForbidden


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
        authentication = Authentication()
        # allowed_methods = ['get', 'post', 'put', 'delete']
        excludes = ['is_active', 'is_staff', 'is_superuser',
                    'last_login', 'password', 'resource_uri', 'username']
        filtering = {
            'commerce': ALL_WITH_RELATIONS,
            'ci': ('exact',),
            'username': ('exact',)
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        worker = authenticate(username=username, password=password)
        if worker:
            if worker.is_active:
                login(request, worker)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

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
