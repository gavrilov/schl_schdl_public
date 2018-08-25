from app.database import db
from app.schdl_class.models import Schdl_Class

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='subject', lazy='dynamic')
    #director_name = db.Column('director_name', db.Unicode(2048))
    #email = db.Column('email', db.Unicode(2048))
    #email2 = db.Column('email2', db.Unicode(2048))
    #phone1 = db.Column('phone1', db.Unicode(2048))
    #phone2 = db.Column('phone2', db.Unicode(2048))
    #website = db.Column('website', db.Unicode(2048))
    #addresses = db.relationship('EasypostDefaultAddress', backref='user', lazy='dynamic')
"""

class EasypostDefaultAddress(db.Model):
    __tablename__ = "easypost_default_addresses"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    easypost_address_id = db.Column('easypost_address_id', db.Unicode(2048))
    user_id = db.Column(db.Integer, db.ForeignKey('easypost_users.id'))
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    company = db.Column('company', db.Unicode(2048))
    street1 = db.Column('street1', db.Unicode(2048))
    street2 = db.Column('street2', db.Unicode(2048))
    city = db.Column('city', db.Unicode(2048))
    state = db.Column('state', db.Unicode(2048))
    country = db.Column('country', db.Unicode(2048))
    zip = db.Column('zip', db.Unicode(2048))
    phone = db.Column('phone', db.Integer)
    



class EasypostShipment(db.Model):
    __tablename__ = "easypost_shipments"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    easypost_shipment_id = db.Column('easypost_shipment_id', db.Unicode(2048))
    user_id = db.Column(db.Integer, db.ForeignKey('easypost_users.id'))
    from_first_name = db.Column('from_first_name', db.Unicode(2048))
    from_last_name = db.Column('from_last_name', db.Unicode(2048))
    from_company = db.Column('from_company', db.Unicode(2048))
    to_first_name = db.Column('to_first_name', db.Unicode(2048))
    to_last_name = db.Column('to_last_name', db.Unicode(2048))
    to_company = db.Column('to_company', db.Unicode(2048))
    postage_label = db.Column('postage_label', db.Unicode(2048))
    status = db.Column('status', db.Unicode(2048))

"""