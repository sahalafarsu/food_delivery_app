#
# # Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
#
# # from .models import Customer
import stripe
#
from subscription_app.models import Customer,CustomerStatus

stripe.api_key = settings.STRIPE_SECRET_KEY

def special(request):
    return render(request, 'membership/specials.html')


def premium(request):
    return render(request, 'membership/premium.html')


@login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(
            request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
                subscription = stripe.Subscription.retrieve(
                    request.user.customer.stripe_subscription_id)
                product = stripe.Product.retrieve(subscription.plan.product)
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False

    return render(request, 'membership/premium.html',
                  {'membership': membership,
                   'cancel_at_period_end': cancel_at_period_end})


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(
            customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    # return HttpResponse('completed')
    return render(request, 'premium.html', {'customers': customers})


# from django.shortcuts import render
#
#
def join(request):
    return render(request, 'membership/join.html')


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'], )
        customer = Customer()

        # customer.user = request.user

        # ORM Querry
        customer = Customer.objects.get(user=request.user)
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        CustomerStatus.status = 'active'

        customer.save()
        subscription = stripe.Subscription.retrieve(
            customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
    return render(request, 'membership/premium.html', {'subscription': subscription, 'product': product})


def cancel(request):
    return render(request, 'membership/cancel.html')


@login_required
def checkout(request):
    try:
        if request.user.customer.membership:
            return redirect('subscription_app:settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'daily'
        final_dollar = 25
        membership_id = 'price_1L18jCSDsPN3RN8SSomGsnup'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'weekly':
                membership = 'weekly'
                membership_id = 'price_1L18jCSDsPN3RN8S5z4H4tDV'
                final_dollar = 125

            elif request.GET['membership'] == 'monthly':
                membership = 'monthly'
                membership_id = 'price_1L18jCSDsPN3RN8StFEGlpOe'
                final_dollar = 400

        # Create Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/subscription_appsuccess?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'membership/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})


def pausesubscription(request):
    cid = stripe.Subscription.retrieve(
        request.user.customer.stripe_subscription_id),
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection={
            'behavior': 'mark_uncollectible',
        },
    )
    Customer.status = 'pause'
    # return HttpResponse("Successfully paused")
    return render(request, 'membership/premium.html')


def resumesubscription(request):
    cid = stripe.Subscription.retrieve(
        request.user.customer.stripe_subscription_id),
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection='',
    )
    Customer.status = 'active'
    # return HttpResponse("Resumed")
    return render(request, 'membership/premium.html')


def updatesubscription(request):
    if request.method == 'GET':
        current_subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        # new plan
        stripe.Subscription.modify(
            current_subscription.id,
            cancel_at_period_end=False,
            proration_behavior='create_prorations',

            # the new subscription
            items=[{
                'id': current_subscription['items']['data'][0].id,
                'price': 'price_1L18jCSDsPN3RN8StFEGlpOe',
                # 'id': current_subscription['items'].data[0].id,
                # note if you have more than one Plan per Subscription, you'll need to improve this. This assumes one plan per sub.
                # 'deleted': True,
            },
            #     {
            #     'price': 'price_1L18jCSDsPN3RN8StFEGlpOe',
            # }
            ]
        )
                # stripe.Invoice.send_invoice('{{INVOICE_ID}}')

        return render(request, 'membership/premium.html')

def Deletesubscription(request):
    stripe.Subscription.delete(stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)),
    Customer.objects.get(user=request.user).delete()
    Customer.objects.create(user=request.user)

    return redirect('/deletemsg')
