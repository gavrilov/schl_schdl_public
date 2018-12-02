import stripe
from flask import render_template, current_app, flash
from flask_security import current_user

from app.models import User


def add_card_button():
    return render_template('payment/add_card_button.html')


def my_cards():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not current_user.stripe_id:
        return "You do not have any cards"
    customer = stripe.Customer.retrieve(current_user.stripe_id)
    cards = customer.sources.data
    return render_template('payment/my_cards.html', cards=cards)


def my_payments(user_id=None):
    if not user_id:
        user = current_user
    else:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            flash('User with id={} did not find'.format(user_id), 'danger')
            return 'User with id={} did not find'.format(user_id)
    # Show all payments to customer
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not user.stripe_id:
        return "You do not have any payments"
    payments = stripe.Charge.list(customer=user.stripe_id)['data']
    if not payments:
        return "You do not have any payments"
    return render_template('payment/my_payments.html', payments=payments)


def charge_customer(amount, description):
    # TODO figure out - is that def not in app context, and can not use current_user directly???
    # TODO update 11/21/2018 - I removed current_user variable - and it still works

    # When it's time to charge the customer again, retrieve the customer ID.
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        charge = stripe.Charge.create(
            amount=amount,  # in cents
            currency='usd',
            description=description,
            customer=current_user.stripe_id,
            receipt_email=current_user.email
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
