from applications.database import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')  
    username =  db.Column(db.String(100), nullable=False)
    name =  db.Column(db.String(100), nullable=False)
    phone =   db.Column(db.String(20), nullable=True)


class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='admin')  
    


class Professional(db.Model):
    __tablename__ = 'professional'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(50), default='professional')  
    adhaarcard = db.Column(db.Integer,nullable = True)
    past_exp =  db.Column(db.String(100),nullable = True)
    approved =  db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='active')
    rating = db.Column(db.Float, default=0.0)

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service', backref=db.backref('professionals', lazy=True))

    
    
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)  
    service_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default="open") 
    completion_date = db.Column(db.DateTime, nullable=True) 

    user = db.relationship('User', backref='bookings')
    professional = db.relationship('Professional', backref='bookings')
