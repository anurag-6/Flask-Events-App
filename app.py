
from operator import methodcaller
import os
import sqlite3
from winreg import REG_WHOLE_HIVE_VOLATILE
from flask import *
from datetime import datetime

app = Flask(__name__)

app.secret_key="fgfgdgvf"
#file upload
app.config['UPLOAD_FOLDER']=r".\static\uploads"



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/viewEvents')
def view_events():
    if request.method == "GET":
        con = sqlite3.connect('eventsApp.db')
        cur = con.cursor()
        cur.execute("select * from events")
        data=cur.fetchall()
        con.close()
        
        return render_template("ViewEvents.html",records=data)
    



   


@app.route('/addEvent',methods=['GET','POST'])
def add_event():
    if request.method == 'GET':

        return render_template("AddEvents.html") 
    elif request.method == 'POST':
        event = request.form['event']
        dt = request.form['dt']
        prio = request.form['prio']
        pic = request.files['pic']
        # convert iso time to local am/pm string 
        dt_conv = datetime.fromisoformat(dt)
        dt_final = dt_conv.strftime('%d-%m-%Y  %I:%M:%p')
        try:
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],pic.filename))
        except:
            pic.filename = None    
        con = sqlite3.connect('eventsApp.db')
        cur = con.cursor()
        cur.execute("insert into EVENTS values(NULL,?,?,?,?)",(event,dt_final,prio,pic.filename))
        con.commit()
        con.close()
        flash('New event "{}" added successfully'.format(event))

        return redirect(url_for('add_event'))


@app.route('/editEvent/<id>',methods=['POST']) 
def edit_event(id):
    
    ev = request.form['ev']
    dt = request.form['dt']
    pri = request.form['prior']
    pic = request.files['pic']
    try:
        # if the user select new image file update the filename in table
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'],pic.filename))
        con = sqlite3.connect('eventsApp.db')
        cur = con.cursor()
        cur.execute("update EVENTS set ev_img=? where id=?",(pic.filename,id))
        con.commit()
        con.close()

    except:
        # if the user not select any img file just ignore 
        # becausse at the below we are nor updating filename in table
        pass

    con = sqlite3.connect('eventsApp.db')
    cur = con.cursor()
    cur.execute("update EVENTS set ev_name=?,ev_date=?,ev_prio=? where id=?",(ev,dt,pri,id))
    con.commit()
    con.close() 
    flash('Event "{}" successfully'.format(ev))

    return redirect(url_for('view_events'))   



@app.route('/passedEvents',methods=['GET'])
def passed_events():
    
    dn = datetime.now()
    con = sqlite3.connect('eventsApp.db')
    cur = con.cursor()
    cur.execute("select * from events")
    data=cur.fetchall()
    

    # converting list of tuples to list of list for editing
    res = [list(ele) for ele in data]
    # changing the str time to datetime object
    for i in res:
        tom=datetime.strptime(i[2],'%d-%m-%Y %I:%M:%p')
        
        i[2]=tom

    passed=[]
    for item in res:
        
        if item[2] < dn:
            #  creating a new variable to fetch rows which is in passed date
            passed.append(item)
    
    
    # we are gettig the time as no am pm badge in passed so converting it to 12 hr str 
    for k in passed:
        k[2] = k[2].strftime('%d-%m-%Y  %I:%M:%p')

    
    
          
    return render_template("PassedEvents.html",data=passed)


@app.route('/deleteEvent/<id>',methods=['GET'])   
def delete_event(id):
    con = sqlite3.connect('eventsApp.db')
    cur = con.cursor()
    cur.execute('DELETE FROM EVENTS WHERE ID = ?',(id,))
    con.commit()
    con.close()
    return redirect(url_for('view_events'))

@app.route('/deleteAll')
def delete_all():
    conn = sqlite3.connect('eventsApp.db')
    curr = conn.cursor()
    curr.execute('delete from EVENTS')
    conn.commit()
    conn.close()
    return redirect(url_for('view_events'))





    






if __name__ == "__main__":
    app.run(debug=True)