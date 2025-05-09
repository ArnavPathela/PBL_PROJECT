from flask import Flask, render_template, session
from applications.database import db
from applications.config import Config
from applications.model import *


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin_user = Admin.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = Admin(username='admin', password='admin_password', email='admin@abc.com', role='admin')
            db.session.add(admin_user)

        customer_user = User.query.filter_by(username='customer').first()
        if not customer_user:
            customer_user = User(username='customer', password='customer_password', email='customer@abc.com', role='customer', name='Customer', phone=9873) 
            db.session.add(customer_user)

        professional_user = Professional.query.filter_by(name='professional').first()
        if not professional_user:
            professional_user = Professional(name='professional', password='professional_password', email='professional@abc.com', role='professional', phone=9873, adhaarcard=826183 )
            db.session.add(professional_user)

        db.session.commit()

    return app

app = create_app()



# Import the route definitions after app creation
from applications.route import *

if __name__ == '__main__':

    # Run the Flask application
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid the issue with reloading in development mode
