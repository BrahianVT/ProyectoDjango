from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import stripe
# Create your views here. app checkout
# PARA DEFINIR LAS VISTAS DE LA APP CHECKOUT

#  OBTENEMOS EL stripe.api_key QUE ESTA EN EL ARCHIVO SETTINGS.PY
stripe.api_key = settings.STRIPE_SECRET_KEY
# @login_required DONDE SE TIENE QUE INICIAR SESION PARA PODER ACCEDOR A LA PAGINA
@login_required
def checkout(request):
    # publishKey , customer_id Y TODO LO DEMAS SON CONFIGURACIONES PARA EL PROCESO DE PAGO
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
            customer = stripe.Customer.retrieve(customer_id)
            customer.sources.create(source=token)
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency="usd",
                customer=customer,
                description="Example charge"
            )
        except stripe.error.CardError as e:
            # The card has been declined
            pass
    context = {'publishKey':publishKey}
    #DEBE TENER EL MISMO NOMBRE EL TEMPLATE DEL QUE ESTA EN LA CARPETA DE CHECKOUT/TEMPLATES
    template = 'checkout.html'
    return render(request,template,context)


# DUDAS CON EL PROCESO DE PAGO VER :https://stripe.com/docs/examples