import stripe
from flask import Blueprint, abort, request, current_app, redirect, url_for, flash
from flask_security import login_required, current_user

from app import db

payment = Blueprint('payment', __name__, template_folder='templates')


@payment.route('/')
def main():
    return abort(404)


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
    flash('Your card has been added', 'success')
    return redirect(url_for('user.main'))
