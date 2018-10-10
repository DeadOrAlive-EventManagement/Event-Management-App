# Decide whether to use SQLAlchemy (ORM) or MySQLdb (Might have to use a fork, MySQLDb does not have good python3 support) 
# For now going with pymysql as it is good enough and very similar to MySQLdb
# Please follow the following naming convention: long_function_name(var_one,var_two)
from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = 'totally a secret lolz'
# db = pymysql.connect("localhost", "root", "root", "SE_Project")
db = pymysql.connect("localhost", "root", "", "SE_Project", charset="latin1")
cursor = db.cursor()



@app.route('/')
def index():
    '''This function renders the index page of the EventManagement site'''
    if 'customer_id' in session:
        return redirect(url_for("home"))
    return render_template('index.html')

@app.route('/checkemail',methods = ['POST','GET'])
def check_email():
    '''This function checks if the email is already in the database, i.e., already registered'''
    print("form is ", request.form)
    print("json is ", request.json)

    email = request.form['email']
    sql = """SELECT * FROM Customer WHERE email=%s"""
    args =([email])

    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    if(results):
        return "False"
    return "True"

@app.route('/doregister',methods = ['POST'])
def do_register():
    '''This function enters user details into the database, then shows the "You have registered! page'''
    #Get the values from the post form. Use generate_hash before saving for security reasons.
    name = request.form['registerName'] 
    names = name.split()
    email = request.form['loginEmail']
    number = request.form['registerPh']
    pwd = request.form['loginPwd']
    vendor = request.form.get('vendor',False)
    print(vendor)
    hashed_pwd = generate_password_hash(pwd)

    #check if the user already exists 
    sql = """SELECT * FROM Customer WHERE email=%s"""
    args =([email])
    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    if(results):
        #Do appropriate error handling
        return redirect(url_for('index'))
    else:
        sql = """INSERT INTO Customer(email,first_name,middle_name,last_name,phone_number,pwd) values(%s,%s,%s,%s,%s,%s)"""
        if(len(names) == 1):
            args = (email,names[0],None,"",number,hashed_pwd)
        elif(len(names) == 2):
            args = (email,names[0],None,names[1],number,hashed_pwd)
        else:
            args = (email,names[0],names[1],names[2],number,hashed_pwd)
        cursor = db.cursor()
        cursor.execute(sql,args)
        db.commit()
        cursor.close()
    # Using the redirect function because then the "/registered endpoint will show up, which makes more sense to user"
    return redirect(url_for('registered'))

@app.route('/register')
def register():
    '''This function renders the register page'''
    return render_template('register.html')

@app.route('/registered')
def registered():
    return render_template('registered.html')


@app.route('/dosignin',methods=['POST'])
def do_sigin():
    '''This function authenticates the sign in by checking password against database.
    It also creates a session, with the Username stored.
    Redirects to /home so that it makes more sense to user'''
    #add checking procedure
    #get values
    email = request.form["email"]
    pwd = request.form["pwd"]
    #do the check
    sql = "SELECT customer_id,first_name,pwd from Customer where email = %s"
    args = ([email])

    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    if(results):
        row = results[0]

        if(check_password_hash(row[2],pwd)):
            # do session stuff
            session.clear()
            session['customer_id'] = row[0]
            session['name'] = row[1]
            print("IN do_signin login")
            return "True"
            # return redirect(url_for('home'))
        else:
            # wrong password, tell user 
            print("Forgot password!")
            session.clear()
            return "False"
            # return redirect(url_for('index'))
    return "False"

@app.route('/signin',methods=['POST'])
def signin():
    '''Redirects to correct page if session values are set
    This is because password checking is done as part of form validation'''

    if('customer_id' in session):
        return redirect(url_for('home'))
    return redirect(url_for('index'))
    # return "False"

@app.route('/home')
def home():
    # This function shows the user the homepage for a customer. Username will be displayed top right, 
    # and all current events will be displayed on the page, dynamically.
    # Use render template functionality to automatically add name and other data

    # Sample dictionary template returned:
    # events = dict()
    # events["Birthday"] = dict()
    # events["Birthday"]["description"] = "Birthday Party for Ashley"
    # events["Birthday"]["eventid"] = 1
    # events["Birthday"]["date"] = "06-08-2018"
    # vendors = dict()
    # vendors["Ivy Park Venue"] = dict()
    # vendors["Ivy Park Venue"]["service"] = "Venue"
    # vendors["Ivy Park Venue"]["status"] = "Confirmed"
    # vendors["Ivy Park Venue"]["color"] = "green"
    # vendors["HKG Catereres"] = dict()
    # vendors["HKG Catereres"]["service"] = "Caterer"
    # vendors["HKG Catereres"]["status"] = "Waiting"
    # vendors["HKG Catereres"]["color"] = "orange"
    # events["Birthday"]["vendors"] = vendors

    if 'name' in session:
        # Query to get all events created by a customer
        sql = "SELECT * FROM Events where customer_id=%s"
        args = ([session['customer_id']])

        # Executing the query
        cursor = db.cursor()
        cursor.execute(sql,args)
        results = cursor.fetchall()
        cursor.close()

        # Dictionary returned by this function which will hold the event related information for a customer
        events =  dict()

        # Collect event related information for a customer and store it as metadata temporarily
        for row in results:
            event_name = row[1]
            events[event_name] = dict()
            events[event_name]["meta"] = row

        # For every event created by customer extract information - service type, vendor name and booking status
        # by a cross join of bookings, vendor and services table
        for event in events:
            row = events[event]["meta"]

            # TODO(JyothsnaKS): Replace this event id to ensure uniqueness
            event_name = row[1]
            # Uniquely identifies all events
            events[event_name]["eventid"] = row[0]
            # Scheduled data for the event
            events[event_name]["date"] = row[5]

            # Event description for the events
            events[event_name]["description"] = row[6]
            
            sql = "SELECT booking_status,vendor_name,service_type from bookings cross join vendor,services where bookings.vendor_id=vendor.vendor_id and vendor.vendor_id=services.vendor_id and bookings.service_id=services.service_id and event_id=%s"
            args = ([row[0]])

            cursor = db.cursor()
            cursor.execute(sql,args)
            results = cursor.fetchall()
            cursor.close()
            vendors = dict()

            # Added vendors and service information for a specific event to a dictionary
            for subrow in results:
                vendor_name = subrow[1]
                vendors[vendor_name] = dict()
                vendors[vendor_name]["service"] = subrow[2]

                # 1 is for True when the vendor has confirmed service for an event
                if subrow[0] == 1: 
                    vendors[vendor_name]["status"] = "Confirmed"
                    vendors[vendor_name]["color"] = "green"
                else:
                    vendors[vendor_name]["status"] = "Waiting"
                    vendors[vendor_name]["color"] = "orange"

            events[event_name]["vendors"] = vendors

            # Delete the metadata gathered earlier as this is no longer required
            del events[event_name]["meta"]

        return render_template('manage_events.html', name = session['name'], events = events)
    return redirect(url_for('index'))

@app.route('/create')
def create():
    '''This funnction shows the user the create event page. Username will be displayed top right, 
    and all current events will be displayed on the page, dynamically.'''
    # use render templeate functionality to automatically add name and other data 
    if 'name' in session:
        return render_template('create_event.html',name = session['name'])
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    '''This funnction shows the user the contact us page. Username will be displayed top right, 
   '''
    # use render templeate functionality to automatically add name and other data 
    if 'name' in session:
        return render_template('contact.html',name = session['name'])
    return render_template('contact.html',name = "")

@app.route('/contactSend', methods=['GET','POST'])
def contacted():
    '''This funnction shows the user the contact us page. Username will be displayed top right, 
   '''
    # use render templeate functionality to automatically add name and other data 
    if 'name' in session:
        return render_template('contacted.html',name = session['name'])
    return render_template('contacted.html',name = "")

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/services")
def services():
    services = dict()
    services["catering"] = dict()
    services["catering"]["description"] = "Some info here"
    services["catering"]["price"] = "1000$"
    return render_template("manage_services.html",services = services)

@app.route("/cancelevent", methods=['POST'])
def cancelevent():
    print('cancelevent', request.form['eventid'])

    cursor = db.cursor()
    sql = "DELETE from bookings where event_id=%s"
    args = ([request.form['eventid']])
    cursor.execute(sql, args)
    db.commit()
    sql = "DELETE from events where event_id=%s"
    args = ([request.form['eventid']])
    cursor.execute(sql, args)
    db.commit()
    cursor.close()
    
    # TODO(JyothsnaKS): Need to fix the URL redirect
    if 'name' in session:
        return redirect(url_for('home'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    # run!
    app.run(debug=True)

