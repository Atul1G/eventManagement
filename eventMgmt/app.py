from flask import Flask,request,render_template,session,redirect,url_for
from flask_mysqldb import MySQL 
import MySQLdb.cursors 

app=Flask(__name__)

app.secret_key = 'K0XP18HzzHRvWrWxxwqv'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'app_account'
  
mysql = MySQL(app) 

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/eventTrack",methods=['POST','GET'])
def eventTrack():
    if request.method == 'POST':
        id=request.form['eventnumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM app_eventlist WHERE id = %s",(str(id))) 
        data = cursor.fetchall() #data from database 
        print(data)
        return render_template('eventTrack.html',value=data,display_style="block")
    else:
         return render_template('eventTrack.html',display_style="none")


@app.route("/eventBook",methods=['POST','GET'])
def eventBook():
    if request.method == 'POST':
        eventType = request.form['Event Type']
        menuType = request.form['menutype']
        quantity = request.form['quantity']
        
        dj = request.form['dj']
        decor = request.form['decor']
        venue = request.form['Venue List']
        estimate=0
        if eventType == 'Wedding':
            estimate+=int(30000)
        elif eventType == 'Family Function':
            estimate+=int(10000)
        else:
            estimate+=int(50000)
        
        if menuType == 'Veg':
            estimate+=(int(quantity)*200)
        else:
            estimate+=(int(quantity)*300)
        
        if dj=='Yes':
            estimate+=5000
        if decor == 'Yes':
            estimate+=10000
        
        if venue == 'Hotel Taj':
            estimate+=100000
        
        if venue == 'Banquet Hall':
            estimate+=75000

        if venue == 'PB Multipurpose Hall':
            estimate+=50000
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('INSERT INTO app_eventlist(`eventType`,`buffet`,`quantity`,`dj`,`decor`,`venue`,`status`,`total_amt`) VALUES(% s,% s,%s,% s,% s,% s,%s,%s)',(eventType,menuType,int(quantity),dj,decor,venue,"Pending",int(estimate))) 
        mysql.connection.commit()
        id=cursor.lastrowid
        info="Event Book Request has been Sent!!! and Booking Request Id is '"+str(id)+"'. Remember this to Track the Event Status"
        return render_template('eventBook.html',info=info)
    else: 
        return render_template('eventBook.html')

@app.route('/update_status',methods=['POST','GET'])
def update():
            if request.method == 'POST' and 'event id' in request.form and 'event status' in request.form:
                eventid = request.form['event id']
                event_status = request.form['event status']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('UPDATE app_eventlist SET `status` = %s WHERE `id` = %s',(event_status,int(eventid))) 
                mysql.connection.commit()
                id=cursor.lastrowid
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute("SELECT * FROM app_eventlist") 
                data = cursor.fetchall() #data from database
                msg="Status of "+ str(eventid)+" Changed to "+event_status
                return render_template('update_status.html',status_value=msg,value=data)
            else:
                if request.method == 'POST':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                    cursor.execute("SELECT * FROM app_eventlist") 
                    data = cursor.fetchall() #data from database
                    return render_template('update_status.html',status_value="Error",value=data)
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                    cursor.execute("SELECT * FROM app_eventlist") 
                    data = cursor.fetchall() #data from database
                    return render_template('update_status.html',value=data)

     
    

@app.route("/adminLogin")
def adminLogin():
    return render_template('adminLogin.html')
    
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('adminLogin')) 
    

@app.route("/form_login",methods=['POST','GET'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM app_login WHERE username = % s AND password = % s', (username, password )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('form_login.html',status_value=msg) 
        else: 
            status_value = 'Incorrect username / password !'
            return render_template('adminLogin.html',info=status_value)
    else:
        return render_template('form_login.html') 
 


if __name__=='__main__':
    app.run()