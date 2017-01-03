from django.contrib import admin

# Register your models here.

# Definimos los modelos que se utilizaran desde la administracion que son los modelos profile y userStripe
from .models import profile,userStripe
class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = profile

admin.site.register(profile,profileAdmin)

class userStripeAdmin(admin.ModelAdmin):
    class Meta:
        model = userStripe

admin.site.register(userStripe,userStripeAdmin)