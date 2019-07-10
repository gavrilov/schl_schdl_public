import stripe
from flask import render_template, current_app
from flask_babelex import lazy_gettext as _l
from flask_security import current_user


def add_card_button():
    return render_template('payment/add_card_button.html')


def my_cards(user=current_user):
    # get User object and return html code
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not user.stripe_id:
        return _l('You do not have any cards')
    try:
        customer = stripe.Customer.retrieve(user.stripe_id)
        cards = customer.sources.data
    except stripe.error.InvalidRequestError as e:

        body = e.json_body
        current_app.logger.error(
            'Unable to get card information for user id={}. Check Stripe API Key. {}'.format(user.id, body))
        return _l('Error: Unable to get your card information')
    except stripe.error.APIError as e:
        body = e.json_body
        current_app.logger.error(
            'Unable to get payment information for user id={}. Check Stripe API Key. {}'.format(user.id, body))
        return _l('Error: Unable to get your payment information')
    return render_template('payment/my_cards.html', cards=cards)


def my_payments(user=current_user):
    # get User object and return html code
    # Show all payments to customer
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not user.stripe_id:
        return _l('You do not have any payments')
    try:
        payments = stripe.Charge.list(customer=user.stripe_id)['data']
    except stripe.error.InvalidRequestError as e:
        body = e.json_body
        current_app.logger.error(
            'Unable to get payment information for user id={}. Check Stripe API Key. {}'.format(user.id, body))
        return _l('Error: Unable to get your payment information')
    except stripe.error.APIError as e:
        body = e.json_body
        current_app.logger.error(
            'Unable to get payment information for user id={}. Check Stripe API Key. {}'.format(user.id, body))
        return _l('Error: Unable to get your payment information')
    if not payments:
        return _l('You do not have any payments')
    return render_template('payment/my_payments.html', payments=payments)


def charge_customer(amount, description, user=current_user):
    # When it's time to charge the customer again, retrieve the customer ID.
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        charge = stripe.Charge.create(
            amount=amount,  # in cents
            currency='usd',
            description=description,
            customer=user.stripe_id,
            receipt_email=user.email
        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        # get that decilned charge with error message
        charge = stripe.Charge.retrieve(body['error']['charge'])
        return charge
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        body = e.json_body
        current_app.logger.error('Too many requests made to the Stripe API too quickly. {}'.format(body))
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        body = e.json_body
        current_app.logger.error('Invalid parameters were supplied to Stripe API. {}'.format(body))
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        body = e.json_body
        current_app.logger.error('Authentication with Stripe API failed. Check API keys. {}'.format(body))
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        body = e.json_body
        current_app.logger.error('Network communication with Stripe failed. {}'.format(body))
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        body = e.json_body
        current_app.logger.error('Network communication with Stripe failed. {}'.format(body))
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        current_app.logger.error('Something else happened, completely unrelated to Stripe')
        pass
    else:
        # return charge if we dont have errors
        return charge


def refund_charge(charge, amount, description, reason):
    # When it's time to charge the customer again, retrieve the customer ID.
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        refund = stripe.Refund.create(
            charge=charge,  # i.e. ch_1Dj57c2eZvKYlo2CzWCUpc0h
            amount=amount,  # in cents
            metadata={'description': description},
            reason=reason  # duplicate, fraudulent, requested_by_customer
        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        current_app.logger.error('Card Error. {}'.format(body))
        pass
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        body = e.json_body
        current_app.logger.error('Too many requests made to the Stripe API too quickly. {}'.format(body))
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        body = e.json_body
        current_app.logger.error('Invalid parameters were supplied to Stripe API. {}'.format(body))
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        body = e.json_body
        current_app.logger.error('Authentication with Stripe API failed. Check API keys. {}'.format(body))
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        body = e.json_body
        current_app.logger.error('Network communication with Stripe failed. {}'.format(body))
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        body = e.json_body
        current_app.logger.error('Network communication with Stripe failed. {}'.format(body))
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        current_app.logger.error('Something else happened, completely unrelated to Stripe')
        pass
    else:
        # return charge if we dont have errors
        return refund
