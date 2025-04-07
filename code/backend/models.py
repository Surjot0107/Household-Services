from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    full_name = db.Column(db.String,nullable=False)
    address = db.Column(db.String,nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String,nullable=False,default='active')
    phone = db.Column(db.Integer,nullable=False)

class professional(db.Model):
    __tablename__ = "professional"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    full_name = db.Column(db.String,nullable=False)
    service_provided = db.Column(db.String,nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String,nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String,nullable=False,default='waiting')
    phone = db.Column(db.Integer,nullable=False)

class services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer,primary_key=True)
    service_type = db.Column(db.String,nullable=False)
    service_name = db.Column(db.String,nullable=False)
    price = db.Column(db.Integer,nullable=False)

class booked_services(db.Model):
    __tablename__ = "booked_services"
    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer)
    prof_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    status = db.Column(db.String,nullable=False,default="requested")
    rating_by_customer = db.Column(db.Integer)
    remarks_by_customer = db.Column(db.String)
    date_requested = db.Column(db.String,nullable=False)
    date_completed = db.Column(db.String)

class admin(db.Model):
    __tablename__ = "admin"
    password = db.Column(db.String,primary_key=True,nullable=False)