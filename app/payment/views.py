import stripe
from flask import render_template, Blueprint, current_app, request, redirect, url_for, flash
from flask_security import current_user, login_required

from app import db

payment = Blueprint('payment', __name__, template_folder='templates')


@payment.route('/')
@login_required
def add_card_button():
    return render_template('payment/add_card_button.html')


@payment.route('/update_card', methods=['POST'])
@login_required
def update_card():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    token = request.form['stripeToken']
    if not current_user.stripe_id:
        # Create a Stripe Customer:
        customer = stripe.Customer.create(source=token, email=current_user.email)
        current_user.stripe_id = customer.id
        db.session.commit()
    else:
        # Update a Card of Customer
        customer = stripe.Customer.retrieve(current_user.stripe_id)
        customer.source = token
        customer.save()
    # return redirect(url_for('payment.my_cards'))
    return "Your Stripe id is {}".format(current_user.stripe_id)


@payment.route('/my_cards')
@login_required
def my_cards():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not current_user.stripe_id:
        return "You do not have any cards"
    customer = stripe.Customer.retrieve(current_user.stripe_id)
    cards = customer.sources.data
    return render_template('payment/my_cards.html', cards=cards)


@payment.route('/my_payments')
@login_required
def my_payments():
    # Show all payments to customer
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if not current_user.stripe_id:
        return "You do not have any payments"
    payments = stripe.Charge.list(customer=current_user.stripe_id)['data']
    if not payments:
        return "You do not have any payments"
    return render_template('payment/my_payments.html', payments=payments)


@payment.route('/charge')
@login_required
def charge():
    if not current_user.stripe_id:
        flash('Please add a card')
        return 'Please add a card'  # TODO redirect to user_payment_page
    charge_customer(current_user.stripe_id)
    return redirect(url_for('payment.my_payments'))


def charge_customer(customer_id):
    # When it's time to charge the customer again, retrieve the customer ID.
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    charge = stripe.Charge.create(
        amount=3800,  # $15.00 this time
        currency='usd',
        customer=customer_id,  # Previously stored, then retrieved
    )
