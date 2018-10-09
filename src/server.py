# Decide wheter to use SQLAlchemy (ORM) or MySQLdb (Might have to use a fork, MySQLDb does not have good python3 support) 
# For now going with pymysql as it is good enough and very similar to MySQLdb
# Please follow the following naming convention: long_function_name(var_one,var_two)
from flask import Flask,flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = 'totally a secret lolz'
db = pymysql.connect("localhost","root","","SE_Project",charset='utf8')
cursor = db.cursor()


@app.route('/')
def index():
    '''This function renders the index page of the EventManagement site'''
    return render_template('index.html')
@app.route('/checkemail',methods = ['POST','GET'])
def check_email():
    '''This function checks if the email is already in the database, i.e., already registered'''
    print("form is ",request.form)

    print("json is ",request.json)
    email = request.form['email']
    sql = """SELECT * FROM Customer WHERE email=%s"""
    args =([email])
    cursor.execute(sql,args)
    results = cursor.fetchall()
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
    hashed_pwd = generate_password_hash(pwd)

    #check if the user already exists 
    sql = """SELECT * FROM Customer WHERE email=%s"""
    args =([email])
    cursor.execute(sql,args)
    results = cursor.fetchall()
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
        cursor.execute(sql,args)
        db.commit()
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

    cursor.execute(sql,args)
    results = cursor.fetchall()
    if(results):
        row = results[0]
        if(check_password_hash(row[2],pwd)):
            # do session stuff
            print("Login succesfull!")
            session.clear()
            session['customer_id'] = row[0]
            session['name'] = row[1]
            return "True"
            # return redirect(url_for('home'))
        else:
            # wrong password, tell user 
            # print("Forgot password!")
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
    '''This funnction shows the user the homepage. Username will be displayed top right, 
    and all current events will be displayed on the page, dynamically.'''
    # use render templeate functionality to automatically add name and other data 
    #test data
    events = dict()
    events["Birthday"] = dict()
    events["Birthday"]["description"] = "Birthday Party for Ashley"
    events["Birthday"]["date"] = "06-08-2018"
    vendors = dict()
    vendors["Ivy Park Venue"] = dict()
    vendors["Ivy Park Venue"]["service"] = "Venue"
    vendors["Ivy Park Venue"]["status"] = "Confirmed"
    vendors["Ivy Park Venue"]["color"] = "green"
    vendors["HKG Catereres"] = dict()
    vendors["HKG Catereres"]["service"] = "Caterer"
    vendors["HKG Catereres"]["status"] = "Waiting"
    vendors["HKG Catereres"]["color"] = "orange"
    events["Birthday"]["vendors"] = vendors
    # return render_template('manage_events.html',name = session['name'])
    if 'name' in session:
        return render_template('manage_events.html',name = session['name'],events = events)
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

@app.route('/logout')
def logout():
    session.clear()
    redirect(url_for('index'))

if __name__ == '__main__':
	# run!
	app.run(debug=True)
