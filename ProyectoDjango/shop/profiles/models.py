from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
# Creamos los modelos que se utilizaran
# Para el modelo Profile solo definimos 3 campos nombre, usuario y descripcion
class profile(models.Model):
    name = models.CharField(max_length=200 , null=False , default='')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True )
    description = models.TextField(null = True)
    def __unicode__(self):
        return self.name

# modelo para crear el usuario de stripe necesario para realizar pagos
class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200 , null = True , blank=True)

    def __unicode__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username

# Este metodo sera utilizado para crear usuario de stripe o asignarlo si es que ya esta creado
def stripeCallback(sender, request,user, **kwargs):
    user_atripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print 'creted for %s' %(user.username)
    if user_atripe_account.stripe_id is None or user_atripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_atripe_account.stripe_id = new_stripe_id['id']
        user_atripe_account.save()

# Este metodo sera utilizado para crear perfil o asignarlo si ya esta creado
def profileCallback(sender, request, user,**kwargs):
    userProfile, is_created = profile.objects.get_or_create(user = user)
    if is_created:
        userProfile.name = user.username
        userProfile.save()

# cada vez que se inicie y se cree otra cuenta se realizaran los metodos stripeCallback y profileCallback
user_logged_in.connect(stripeCallback)
user_signed_up.connect(stripeCallback)

user_signed_up.connect(profileCallback)