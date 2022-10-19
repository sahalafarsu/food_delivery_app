import stripe

# Create your views here.
from django.shortcuts import redirect
from django.views import generic

# from cart.views import cart_detail
from django.views.generic import TemplateView

from food_delivery_project import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(generic.View):
    def post(self,request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        price=request.session['total']
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(price * 100),
                        'product_data': {
                            'name': 'Restio-Order'
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',

            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',

        )
        return redirect(checkout_session.url, code=303)

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"
