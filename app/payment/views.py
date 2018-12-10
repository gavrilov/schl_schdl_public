import stripe
from flask import Blueprint, abort, request, current_app, redirect, url_for, flash
from flask_babel import _
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
    flash(_('Card has been added'), 'success')
    return redirect(redirect_url())


@payment.route('/update_card_and_pay', methods=['POST'])
@login_required
def update_card_and_pay():
    # Update Card and Pay in one click. This def for special button on class enrollment page
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    token = request.form['stripeToken']
    class_id = request.form['class_id']
    student_id = request.form['student_id']
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
    flash(_('Card has been added'), 'success')
    return redirect(url_for('schdl_class.payment_class', class_id=class_id, student_id=student_id))


def redirect_url(default='user.main'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
