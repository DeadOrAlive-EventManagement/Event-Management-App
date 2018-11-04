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
    elif 'vendor_id' in session:
        return redirect(url_for("services"))
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

    # Email is valid
    if results:
        return "False"

    sql = """SELECT * FROM Vendor WHERE email=%s"""
    args =([email])

    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    # Email is valid
    if results:
        return "False"

    # # Email is invalid
    return "True"

@app.route('/doregister',methods = ['POST'])
def do_register():
    '''This function enters user details into the database, then shows the "You have registered! page'''
    # Get the values from the post form. Use generate_hash before saving for security reasons.
    name = request.form['registerName']
    names = name.split()
    email = request.form['loginEmail']
    number = request.form['registerPh']
    pwd = request.form['loginPwd']
    vendor = request.form.get('vendor',False)
    hashed_pwd = generate_password_hash(pwd)

    if vendor == 'on':
        sql = """SELECT * FROM vendor WHERE email=%s"""
        args =([email])
        cursor = db.cursor()
        cursor.execute(sql,args)
        results = cursor.fetchall()
        cursor.close()

        # Vendor has already registered
        if(results):
            #Do appropriate error handling
            return redirect(url_for('index'))
        else:
            location = request.form['location']

            sql = """INSERT INTO Vendor(email,vendor_name,phone_number,pwd,vendor_location) values(%s,%s,%s,%s,%s)"""
            args = (email,name,number,hashed_pwd,location)
            cursor = db.cursor()
            cursor.execute(sql,args)
            db.commit()
            cursor.close()
    else:
        sql = """SELECT * FROM Customer WHERE email=%s"""
        args =([email])
        cursor = db.cursor()
        cursor.execute(sql,args)
        results = cursor.fetchall()
        cursor.close()

        # Customer has already registered
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
def do_signin():
    '''This function authenticates the sign in by checking password against database.
    It also creates a session, with the Username stored.
    Redirects to /home so that it makes more sense to user'''
    #add checking procedure
    # Get the form values
    email = request.form["email"]
    pwd = request.form["pwd"]

    # Check if customer exists
    cursor = db.cursor()
    sql = "SELECT customer_id,first_name,pwd from Customer where email = %s"
    args = ([email])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    if results:
        row = results[0]

        if(check_password_hash(row[2],pwd)):
            # do session stuff
            session.clear()
            session['customer_id'] = row[0]
            session['name'] = row[1]
            return "True"
        else:
            # wrong password, tell user
            session.clear()
            return "False"

    # If we reach here, it means that the either the user is a vendor he has not registered with us yet
    cursor = db.cursor()
    sql = "SELECT vendor_id,vendor_name,pwd from Vendor where email = %s"
    args = ([email])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()

    # Check if customer exists
    if results:
        row = results[0]
        if(check_password_hash(row[2],pwd)):
            # do session stuff
            session.clear()
            session['vendor_id'] = row[0]
            session['name'] = row[1]
            return "True"
        else:
            # wrong password, tell user
            session.clear()
            return "False"
    # If we still reach here, it means that the user is not a registered one
    return "False"

@app.route('/signin',methods=['POST'])
def signin():
    '''Redirects to correct page if session values are set
    This is because password checking is done as part of form validation'''

    if('customer_id' in session):
        return redirect(url_for('home'))
    elif('vendor_id') in session:
        # TODO(JyothsnaKS): Fix header for vendor
        return redirect(url_for('home'))
    return redirect(url_for('index'))
    # return "False"

@app.route('/home')
def home():
    # This function shows the user the homepage for a user.
    # Username will be displayed top right, and all current events will be displayed on the page for the customer, dynamically.
    # For the vendor, all their services will be displayed, dynamically
    # Use render template functionality to automatically add name and other data

    if 'vendor_id' in session:
        return redirect(url_for('services'))

    # Sample dictionary template returned for customer:
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

    if 'customer_id' in session:
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
                elif subrow[0] == 2:
                    vendors[vendor_name]["status"] = "Rejected"
                    vendors[vendor_name]["color"] = "red"
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
    if 'customer_id' in session:
        return render_template('create_event.html', name = session['name'])
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    '''This funnction shows the user the contact us page. Username will be displayed top right,
   '''
    # use render templeate functionality to automatically add name and other data
    if 'name' in session:
        return render_template('contact.html', name = session['name'])
    return render_template('contact.html',name = "")

@app.route('/contactSend', methods=['GET','POST'])
def contacted():
    '''This funnction shows the user the contact us page. Username will be displayed top right,
   '''
    # use render templeate functionality to automatically add name and other data
    if 'name' in session:
        return render_template('contacted.html', name = session['name'])
    return render_template('contacted.html', name = "")

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/services")
def services():
    if 'vendor_id' in session:
        print(session)
        cursor = db.cursor()
        sql = " SELECT service_type,price_per_unit,description from services cross join vendor where vendor.vendor_id=services.vendor_id and vendor.vendor_id=%s"
        args = ([session['vendor_id']])
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        services = dict()

        for row in results:
            service_type = row[0]
            services[service_type] = dict()
            services[service_type]["price"] = str(row[1])
            services[service_type]["description"] = row[2]
        print(services)
        return render_template("manage_services.html", services = services)
    return redirect(url_for('index'))

@app.route("/cancelevent", methods=['POST'])
def cancelevent():
    # TODO(JyothsnaKS): Perform checks on data and other condition to decide if customer is allowed
    # to delete the event.
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

    if 'customer_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route("/managevendor",methods = ['GET','POST'])
def manage_vendor():
    if 'vendor_id' in session:

        # Query to get all events created assigned to a vendor
        sql = "SELECT * FROM Events e,Bookings b where b.event_id=e.event_id and b.vendor_id=%s"
        args = ([session['vendor_id']])

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
            #service_id for acceptance/rejection
            events[event_name]["serviceid"] = row[10]

            # Event description for the events
            events[event_name]["description"] = row[6]

            sql = "SELECT booking_status,first_name,service_type from bookings cross join customer,services where bookings.customer_id=customer.customer_id  and bookings.service_id=services.service_id and event_id=%s"
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
                elif subrow[0] == 2:
                    vendors[vendor_name]["status"] = "Rejected"
                    vendors[vendor_name]["color"] = "red"
                else:
                    vendors[vendor_name]["status"] = "Waiting"
                    vendors[vendor_name]["color"] = "orange"

            events[event_name]["vendors"] = vendors

            # Delete the metadata gathered earlier as this is no longer required
            del events[event_name]["meta"]

    return render_template('manage_vendor.html', name = session['name'], events = events)
    #return render_template("manage_vendor.html")

@app.route("/acceptrejectevent",methods=['GET','POST'])
def rejectevent():
    cursor = db.cursor()
    sql = "UPDATE bookings set booking_status=%s where service_id=%s"
    args = ([request.form['status'],request.form['serviceid']])
    print(request.form['status'],request.form['serviceid'] )
    cursor.execute(sql, args)
    db.commit()

    cursor.close()
    return redirect(url_for('manage_vendor'))
    #I have no idea why the below is present. Keeping it to maintain consistency with cancel event
    if 'customer_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('index'))
@app.route("/getvenue", methods=['POST'])
def getvenue():
    print("IN THE FUNCTION WE WANT TO BE IN : GETVENUE");
    # value= int(request.form['value'])
    # for i in request.form:
    #     print(i)
    data = request.get_json()
    print(data)
    # data = json.load(data);
    print("HERE IS DATA --------------------->",data['value'])
    cursor = db.cursor()
    sql = "SELECT vendor_name, price_per_unit , s.description, service_id, vendor_id FROM Vendor v NATURAL JOIN Services s where s.service_type = 'Venue' and price_per_unit < %s" ;
    args =([data['value']])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()
    venues = dict()
    for row in results:
        venue_name = row[0]
        venues[venue_name] = dict()
        venues[venue_name]["price"] = str(row[1])
        venues[venue_name]["description"] = row[2]
        venues[venue_name]["service_id"]= row[3]
        venues[venue_name]["vendor_id"]= row[4]
    print(venues)

    return json.dumps(venues);

@app.route("/getdecorator", methods=['POST'])
def getdecor():
    print("IN THE FUNCTION WE WANT TO BE IN : GETDECOR");
    # value= int(request.form['value'])
    # for i in request.form:
    #     print(i)
    data = request.get_json()
    print(data)
    # data = json.load(data);
    print("HERE IS DATA --------------------->",data['value'])
    cursor = db.cursor()
    sql = "SELECT vendor_name, price_per_unit , s.description, service_id , vendor_id FROM Vendor v NATURAL JOIN Services s where s.service_type = 'Decor' and price_per_unit < %s" ;
    args =([data['value']])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()
    decor = dict()
    for row in results:
        decor_name = row[0]
        decor[decor_name] = dict()
        decor[decor_name]["price"] = str(row[1])
        decor[decor_name]["description"] = row[2]
        decor[decor_name]["service_id"]= row[3]
        decor[decor_name]["vendor_id"]= row[4]
    # print(venues)
    # print(json.dumps(decor));
    return json.dumps(decor);

@app.route("/getcaterer", methods=['POST'])
def getcaterer():
    print("IN THE FUNCTION WE WANT TO BE IN : GETCATERER");
    # value= int(request.form['value'])
    # for i in request.form:
    #     print(i)
    data = request.get_json()
    print(data)
    # data = json.load(data);
    print("HERE IS DATA --------------------->",data['value'])
    cursor = db.cursor()
    sql = "SELECT vendor_name, price_per_unit , s.description, service_id ,vendor_id FROM Vendor v NATURAL JOIN Services s where s.service_type = 'Catering' and price_per_unit < %s" ;
    args =([data['value']])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()
    caterer = dict()
    for row in results:
        caterer_name = row[0]
        caterer[caterer_name] = dict()
        caterer[caterer_name]["price"] = str(row[1])
        caterer[caterer_name]["description"] = row[2]
        caterer[caterer_name]["service_id"]= row[3]
        caterer[caterer_name]["vendor_id"]= row[4]
    # print(venues)
    # print(json.dumps(decor));
    return json.dumps(caterer);

# to create event
@app.route("/eventcreate", methods=['POST'])
def eventcreate():
    print("IN THE FUNCTION WE WANT TO BE IN : EVENTCREATE");
    # value= int(request.form['value'])
    # for i in request.form:
    #     print(i)
    data = request.get_json()
    print(data)
    # data = json.load(data);
    print("HERE IS DATA --------------------->",data['venueDetails']['venueId'],data['decorDetails']['decorId'],data['catererDetails']['catererId'])
    print(int(data['venueDetails']['venueId']),int(data['decorDetails']['decorId']),int(data['catererDetails']['catererId']))
    print(type(int(data['venueDetails']['venueId'])))
    print(type(data['venueDetails']['venueId']))
    # cursor = db.cursor()
    sql_insert = "INSERT INTO Events(event_name,customer_id,budget,num_people,date_event,details) values(%s,%s,%s,%s,%s,%s)" ;
    args = (data['eventType'],session['customer_id'],data['eventBudget'],data["numPeople"],data['eventDate'],data['eventDescription'])
    print(args)
    cursor = db.cursor()
    cursor.execute(sql_insert,args)
    db.commit()
    sql_select = "SELECT event_id FROM Events where event_name =%s and customer_id= %s and budget= %s and num_people=%s and date_event=%s" ;
    args=(data['eventType'],session['customer_id'],data['eventBudget'],data["numPeople"],data['eventDate'])
    # args = (,,,,,data['eventDescription'])
    print(args)
    cursor.execute(sql_select,args)
    results = cursor.fetchall()
    event_id  = ""
    for row in results:
        event_id = str(row[0])
    sql_insert = "INSERT INTO Bookings(event_id,vendor_id,customer_id,service_id,booking_status) values(%s,%s,%s,%s,%s)" ;
    args = (event_id,data['venueDetails']['venueVendorId'],session['customer_id'],data['venueDetails']['venueId'],"Pending")
    print(args)
    cursor = db.cursor()
    cursor.execute(sql_insert,args)
    db.commit()
    sql_insert = "INSERT INTO Bookings(event_id,vendor_id,customer_id,service_id,booking_status) values(%s,%s,%s,%s,%s)" ;
    args = (event_id,data['decorDetails']['decorVendorId'],session['customer_id'],data['decorDetails']['decorId'],"Pending")
    print(args)
    cursor = db.cursor()
    cursor.execute(sql_insert,args)
    db.commit()
    sql_insert = "INSERT INTO Bookings(event_id,vendor_id,customer_id,service_id,booking_status) values(%s,%s,%s,%s,%s)" ;
    args = (event_id,data['catererDetails']['catererVendorId'],session['customer_id'],data['catererDetails']['catererId'],"Pending")
    print(args)
    cursor = db.cursor()
    cursor.execute(sql_insert,args)
    db.commit()
    cursor.close()
    return "true";

if __name__ == '__main__':
    # run!
    app.run(debug=True)
