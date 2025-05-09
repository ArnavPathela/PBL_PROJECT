from main import app 
from flask import render_template,request,session,url_for,redirect,flash
from flask import session
from applications.model import *




@app.route('/home')
def home():
    if session.get('role') == 'customer':
        username = session.get('username')
        if username is None:
            hello_message = '''Welcome to the HouseHold Services App
            Please login to access the services'''
        else:
            hello_message = f"Hello {username}, welcome back!"
        return redirect(url_for('customerdash'))
    
    elif session.get('role') == 'professional':
       
        professional_id = session.get('professional_id')
        if professional_id:
            professional = Professional.query.filter_by(id=professional_id).first()
            if professional and not professional.approved:
                return redirect(url_for('under_scrutiny'))
            else:
                return redirect(url_for('professionaldash'))
            
    
    elif session.get('role') == 'admin':
        return redirect(url_for('admindash'))
    
    return render_template('index.html', hello="Hello Guest, Please Sign in/Sign Up") 

    




@app.route('/custlogin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('custlogin.html')
    else:
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        # Debugging: Log received data
        print(f"Received email: {email}")
        print(f"Received password: {password}")

        if not email:
            flash('Email is required')
            print("Missing email")
            return redirect(url_for('login'))
        if not password:
            flash('Password is required')
            print("Missing password")
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email')
            print("Invalid email: User not found")
            return redirect(url_for('login'))
        
        if user.password == password:
            session['email'] = user.email
            session['username'] = user.username  
            session['role'] = user.role  
            flash('Login Successfully')
            print("Login successful")
            return redirect(url_for('home'))
        else:
            flash('Invalid password')
            print("Invalid password")
            return redirect(url_for('login'))

        
    
        


@app.route('/proflogin', methods=['GET', 'POST'])
def proflogin():
    if request.method == 'GET':
        return render_template('proflogin.html')
    else:
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        
        if not email:
            flash('Email is required')
            return redirect(url_for('proflogin'))
        if not password:
            flash('Password is required')
            return redirect(url_for('proflogin'))
        
        user = Professional.query.filter_by(email=email).first()

       
        if not user:
            flash('Invalid email')
            return redirect(url_for('proflogin'))
        
        
        if user.password == password:  
            session['professional_id'] = user.id 
            session['name'] = user.name 
            session['role'] = user.role  

            
            if user.approved:
                flash('Login Successfully')
                return redirect(url_for('home'))  
            
            elif user.status == 'blocked':
                flash('your account is blocked due to poor ratings')
                return redirect(url_for('blocked'))
            
            else:
                flash('Your profile is under scrutiny. Please wait for approval.')
                return redirect(url_for('under_scrutiny')) 
        else:
            flash('Invalid password')
            return redirect(url_for('proflogin'))

        

@app.route('/adminlog',methods = ['GET','POST'])
def adminlog():
    if(request.method == 'GET'):
        return render_template('adminlog.html')
    else:
        email = request.form.get('email',None)
        password = request.form.get('password',None)

        if not email:
            print("email is required")
            return redirect(url_for('adminlog'))
        if not password:
            print("password is required")
            return redirect(url_for('adminlog'))
        
        adminn = Admin.query.filter_by(email=email).first()
        if not adminn:
            flash('invalid email')
            return redirect(url_for('adminlog'))
        if adminn.password == password:
            session['email'] = adminn.email
            session['role'] = adminn.role
            flash('logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('invalid password')
            return redirect(url_for('adminlog'))

        



        


@app.route('/logout')
def logout():
    # Check if the action from the AI assistant is 'logout'
        session.pop('email', None)
        session.pop('role', None)
        session.pop('username',None)
        print("Session after logout:", session)
        return redirect(url_for('home'))




        
        
        
    


@app.route('/custreg' , methods = ['GET','POST'])
def custreg():
    if request.method == 'GET':
        return render_template('custregister.html')
    if request.method =='POST':
        name = request.form.get('name',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        username =  request.form.get('username',None)
        phone = request.form.get('phone',None)
        address =  request.form.get('address',None)

        #data check

        if not username:
            flash('Username is required')
            return redirect(url_for('custreg'))
        
        user  = User.query.filter_by(username = username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('custreg'))
        
        if not  email:
            flash('Email is required')
            return redirect(url_for('custreg'))
        
        user =  User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('custlogin'))
        if not password:
            flash('password is required')
            return redirect(url_for('custreg'))
        if not name:
            flash('Name is required')
            return redirect(url_for('custreg'))
        
        

        user = User(name = name,
            email = email,
            password = password,
            username = username,
            phone = phone,
            )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    

@app.route('/admindash')
def admindash():
     return render_template('admindash.html')


@app.route('/customerdash')
def customerdash():
    return render_template('customerdash.html')


@app.route('/professionaldash')
def professionaldash():
    return render_template('professionaldash.html')

@app.route('/bookservice')
def bookservice():
    return render_template('bookservice.html')


@app.route('/bookedservice')
def  bookedservice():
    return render_template('booked.html')

@app.route('/custprofeed')
def custprofeed():
    return render_template('custoprofeed.html')
        
        

@app.route('/searchservice', methods=['GET'])
def search_service():
    service_name = request.args.get('service_name')
    service = Service.query.filter_by(name=service_name).first()
    professionals = service.professionals if service else []
    return render_template('bookservice.html', service_name=service_name, professionals=professionals, service_searched=True)


@app.route('/assign_service', methods=['GET', 'POST'])
def assign_service():
    if request.method == 'POST':
        # Handle form submission and assignment
        professional_id = request.form.get('professional_id')
        service_id = request.form.get('service_id')

        professional = Professional.query.get(professional_id)
        service = Service.query.get(service_id)

        if professional and service:
            professional.service_id = service.id  # Assign the service to the professional
            db.session.commit()
            flash("Assigned successfully", "success")
        else:
            flash("Professional or Service not found.", "error")

        return redirect(url_for('assign_service'))  # Redirect after assignment

    # Handle GET request (show form)
    professionals = Professional.query.all()
    services = Service.query.all()
    return render_template('assignservice.html', professionals=professionals, services=services)

    




@app.route("/profreg", methods=['GET', 'POST'])
def profreg():
    if request.method == 'GET':
        return render_template('profregister.html')
    
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        adhaarcard = request.form.get('adhaarcard')
        past_exp = request.form.get('past_exp')

        
        if not name:
            flash('Name is required')
            return redirect(url_for('profreg'))
        if not email:
            flash('Email is required')
            return redirect(url_for('profreg'))
        pro = Professional.query.filter_by(email=email).first()
        if pro:
            flash('Email already exists')
            return redirect(url_for('proflogin'))
        if not password:
            flash('Password is required')
            return redirect(url_for('profreg'))

        
        if adhaarcard and not adhaarcard.isdigit():
            flash('Adhaar Card must contain only numbers')
            return redirect(url_for('profreg'))

        
        pro = Professional(
            name=name,
            email=email,
            password=password,
            phone=phone,
            adhaarcard=int(adhaarcard) if adhaarcard else None,
            past_exp=past_exp
        )

        
        try:
            db.session.add(pro)
            db.session.commit()
            flash('User created successfully')
            return redirect(url_for('proflogin'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving the data')
            print("Error:", e)
            return redirect(url_for('profreg'))

    


@app.route('/addservice', methods=['GET', 'POST'])
def addservice():
    if request.method == 'POST':
        
        name = request.form.get('name')  
        description = request.form.get('description')
        price = request.form.get('price')

  
        print(f"Name: {name}, Description: {description}, Price: {price}")

        
        if name is None:
            print("Name is None")
        if description is None:
            print("Description is None")
        if price is None:
            print("Price is None")

        
        if not name or not description or not price:
            flash('All fields are required')
            return redirect(url_for('addservice'))

       
        try:
            price = int(price)
        except ValueError:
            flash('Price must be a valid number')
            return redirect(url_for('addservice'))

      
        add = Service(name=name, description=description, price=price)

        try:
            db.session.add(add)
            db.session.commit()
            flash('Service added successfully')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            db.session.rollback()
        return redirect(url_for('addservice'))

    return render_template('addservices.html')

                    
        
        

@app.route('/assign')
def assignserviceform():
    professionals = Professional.query.all()
    services = Service.query.all()
    return render_template('assignservice.html', professionals=professionals, services=services)


@app.route('/views')
def viewser():
    service = Service.query.all()
    return render_template('views.html', service=service)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    try:
        db.session.delete(service)
        db.session.commit()
        return redirect('/views') 
    except:
        return "There was an issue deleting the service."

    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_service(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        try:
            db.session.commit()
            return redirect('/views') 
        except:
            return "There was an issue updating the service."
    else:
        return render_template('edit.html', service=service)


@app.route('/viewprof')
def viewprof():
    prof = Professional.query.all()  
    return render_template('viewprof.html', prof=prof)  

@app.route('/profile/<int:id>')
def profile(id):
   
    professional = Professional.query.filter_by(id=id).first()

    
    if professional and not professional.approved:
        return render_template('under.html')  

    
    return render_template('profile.html', professional=professional)

@app.route('/under_scrutiny')
def under_scrutiny():
    return render_template('under.html')


@app.route('/approve_professionals')
def approve_professionals():
    prof = Professional.query.filter_by(approved=False).all()
    return render_template('approve.html', prof=prof)

@app.route('/approve/<int:id>')
def approve_professional(id):
    professional = Professional.query.get_or_404(id)
    professional.approved = True
    db.session.commit()
    flash(f"Professional {professional.name} has been approved.")
    return redirect(url_for('approve_professionals'))

@app.route('/reject/<int:id>')
def reject_professional(id):
    professional = Professional.query.get_or_404(id)
    db.session.delete(professional)
    db.session.commit()
    flash(f"Professional {professional.name} has been rejected and removed.")
    return redirect(url_for('approve_professionals'))



@app.route('/block/<int:id>', methods=['POST'])
def block_professional(id):
    # Query the professional by ID
    professional = Professional.query.get_or_404(id)
    
    # Set the status to 'blocked'
    professional.status = 'blocked'
    
    try:
        # Commit the changes to the database
        db.session.commit()
        flash('Professional has been blocked successfully.')
    except Exception as e:
        flash('There was an issue blocking the professional.')
    
    # Redirect back to the view professionals page
    return redirect(url_for('viewprof'))


@app.route('/blocked')
def blocked():
    return render_template('blocked.html')

@app.route('/book/<int:professional_id>', methods=['POST'])
def book_professional(professional_id):
    flash("Booking confirmed!", "success") 
    return redirect(url_for('search_service'))



@app.route('/my-bookings')
def my_bookings():
    user_id = session.get('user_id')  # Get user ID from session
    
    if user_id is None:
        flash("Please log in to view your bookings.", "error")
        return redirect(url_for('login'))  # Redirect to login page if no user_id in session
    
    open_bookings = Booking.query.filter_by(user_id=user_id, status="open").all()
    closed_bookings = Booking.query.filter_by(user_id=user_id, status="closed").all()
    
    return render_template('bookings.html', open_bookings=open_bookings, closed_bookings=closed_bookings)
