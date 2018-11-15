import stripe
from flask import render_template, current_app
from flask_security import current_user


def add_card_button():
    return render_template('payment/add_card_button.html')


def my_cards():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not current_user.stripe_id:
        return "You do not have any cards"
    customer = stripe.Customer.retrieve(current_user.stripe_id)
    cards = customer.sources.data
    return render_template('payment/my_cards.html', cards=cards)


def my_payments():
    # Show all payments to customer
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not current_user.stripe_id:
        return "You do not have any payments"
    payments = stripe.Charge.list(customer=current_user.stripe_id)['data']
    if not payments:
        return "You do not have any payments"
    return render_template('payment/my_payments.html', payments=payments)


def charge_customer(current_user, amount, description):
    # TODO figure out - is that def not in app context, and can not use current_user directly???
    # When it's time to charge the customer again, retrieve the customer ID.
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    charge = stripe.Charge.create(
        amount=amount,  # in cents
        currency='usd',
        description=description,
        customer=current_user.stripe_id,
        receipt_email=current_user.email
    )
    return charge
