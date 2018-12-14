import stripe
from flask import Blueprint, abort, request, current_app, redirect, url_for, flash
from flask_babelex import _
from flask_security import login_required, current_user, roles_required

from app import db
from app.models import User
from app.payment import charge_customer
from app.payment.forms import PaymentForm

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


@payment.route('/update_user_card/<user_id>', methods=['POST'])
@roles_required('admin')
def update_user_card(user_id):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    token = request.form['stripeToken']
    this_user = User.query.filter_by(id=user_id).first()
    if not this_user:
        flash(_('User did not find'), 'danger')
        return redirect(redirect_url())
    if not this_user.stripe_id:
        # Create a Stripe Customer:
        customer = stripe.Customer.create(source=token, email=this_user.email)
        this_user.stripe_id = customer.id
        db.session.commit()
    else:
        # Update a Card of Customer
        customer = stripe.Customer.retrieve(this_user.stripe_id)
        customer.source = token
        customer.save()
    flash(_('Card has been added'), 'success')
    return redirect(redirect_url())


@payment.route('/charge_user', methods=['POST'])
@roles_required('admin')
def charge_user():
    form = PaymentForm()
    user_id = int(form.user_id.data)
    this_user = User.query.filter_by(id=user_id).first()
    if not this_user:
        flash(_('User did not find'), 'danger')
        return redirect(redirect_url())
    elif not this_user.stripe_id:
        flash(_('User does not have any card information'), 'danger')
        return redirect(redirect_url())
    else:
        if form.validate_on_submit():
            amount = int(form.amount.data * 100)  # to cents
            description = form.description.data
            charge = charge_customer(amount=amount, description=description, user=this_user)
            if charge.status == 'succeeded':
                flash(_('Card has been charged'), 'success')
            else:
                flash(charge.failure_message, 'danger')
                flash(_('Something wrong with your payment'), 'danger')
            return redirect(redirect_url())
        else:
            # TODO render fields with errors in all project
            flash(_('Something wrong with your charge. Try one more time.'), 'danger')
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
