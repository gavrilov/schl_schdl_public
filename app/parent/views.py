from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from app.models import Parent
from .forms import ParentForm


parent = Blueprint('parent', __name__, template_folder='templates')


@parent.route('/', methods=['GET', 'POST'])
def main():
    # TODO filter current parent by current students or so
    parents = Parent.query.filter_by().all()
    return render_template('parent/parent_list.html', parents=parents, current_parents_only=False)


@parent.route('/all', methods=['GET', 'POST'])
def parent_list():
    parents = Parent.query.all()
    return render_template('parent/parent_list.html', parents=parents, current_parents_only=False)


@parent.route('/<parent_id>', methods=['GET', 'POST'])
def info(parent_id):
    current_parent = Parent.query.filter_by(id=parent_id).first()
    if current_parent:
        return render_template('parent/parent_info.html', parent=current_parent)
    else:
        flash("Parent with id " + str(parent_id) + " did not find", "danger")
        return redirect(url_for('parent.main'))



@parent.route('/add', methods=['GET', 'POST'])
def add_parent():
    form = ParentForm()
    if form.validate_on_submit():
        new_parent = Parent()
        form.populate_obj(new_parent)
        # save new school to db
        db.session.add(new_parent)
        db.session.commit()
        flash(new_parent.first_name + " " + new_parent.last_name + " created", "success")
        return redirect(url_for('parent.main'))
    else:
        return render_template('parent/add.html', form=form)



@parent.route('/edit/<parent_id>', methods=['GET', 'POST'])
def edit_parent(parent_id):
    current_parent = Parent.query.filter_by(id=parent_id).first()
    form = ParentForm()
    if form.validate_on_submit():
        form.populate_obj(current_parent)
        #save to db
        db.session.commit()
        flash(current_parent.first_name + " " + current_parent.last_name + " edited", "success")
        return redirect(url_for('parent.main'))
    else:
        if current_parent:
            form = ParentForm(obj=current_parent)
            return render_template('parent/edit.html', form=form, parent_id=parent_id)
        else:
            flash("Parent with id " + str(parent_id) + " did not find", "danger")
            return redirect(url_for('parent.main'))
