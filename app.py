from flask import Flask, request, redirect, url_for, flash
import json, os

app = Flask(__name__)
app.secret_key = "secretkey"
DATA_FILE = "university_data.json"

# -------------------------
# Default data
# -------------------------
default_data = {
    "students":[
        {'id':'S001','name':'Alice','batch':'2023','department':'CSE'},
        {'id':'S002','name':'Bob','batch':'2023','department':'CSE'},
        {'id':'S003','name':'Charlie','batch':'2023','department':'CSE'},
        {'id':'S004','name':'David','batch':'2023','department':'CSE'},
        {'id':'S005','name':'Eva','batch':'2023','department':'CSE'},
        {'id':'S006','name':'Frank','batch':'2023','department':'CSE'},
        {'id':'S007','name':'Grace','batch':'2023','department':'CSE'},
        {'id':'S008','name':'Hannah','batch':'2023','department':'CSE'},
        {'id':'S009','name':'Ivy','batch':'2023','department':'CSE'},
        {'id':'S010','name':'Jack','batch':'2023','department':'CSE'},
        {'id':'S011','name':'Kim','batch':'2023','department':'CSE'},
        {'id':'S012','name':'Leo','batch':'2023','department':'CSE'},
        {'id':'S013','name':'Mia','batch':'2023','department':'CSE'},
        {'id':'S014','name':'Nina','batch':'2023','department':'CSE'},
        {'id':'S015','name':'Oscar','batch':'2023','department':'CSE'}
    ],
    "teachers":[
        {'id':'T001','name':'Dr. Smith','designation':'Professor','department':'CSE'},
        {'id':'T002','name':'Dr. Johnson','designation':'Associate Professor','department':'CSE'},
        {'id':'T003','name':'Dr. Williams','designation':'Assistant Professor','department':'CSE'}
    ],
    "courses":[
        {'code':'CSE101','name':'Intro to Programming','department':'CSE'},
        {'code':'CSE102','name':'Data Structures','department':'CSE'},
        {'code':'CSE103','name':'Algorithms','department':'CSE'},
        {'code':'CSE104','name':'Computer Architecture','department':'CSE'},
        {'code':'CSE105','name':'Database Systems','department':'CSE'}
    ],
    "results":[]
}

grade_points={'A':4,'B':3,'C':2,'D':1,'F':0}

# -------------------------
# Load / Save
# -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f:
            return json.load(f)
    else:
        data=default_data.copy()
        for s in data['students']:
            s_id=s['id']
            data['results'].append({'student_id':s_id,'grades':{c['code']:'A' for c in data['courses']}})
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE,'w') as f:
        json.dump(data,f,indent=4)

data = load_data()

# -------------------------
# Base HTML / CSS
# -------------------------
base_html = """
<style>
body{font-family:Arial;background:#f4f4f4;margin:0;padding:0;}
.nav{background:#333;color:#fff;padding:10px;text-align:center;}
.nav a{color:#fff;margin:0 10px;text-decoration:none;font-weight:bold;}
.nav a:hover{color:#ff0;}
.container{width:95%;margin:auto;padding:20px;}
table{width:100%;border-collapse:collapse;margin-bottom:20px;}
th,td{border:1px solid #ccc;padding:8px;text-align:left;}
th{background:#333;color:#fff;}
tr:hover{background:#f1f1f1;}
form input{padding:5px;margin:5px 0;width:100%;}
button{padding:5px 10px;background:#333;color:#fff;border:none;border-radius:5px;cursor:pointer;}
button:hover{background:#555;}
</style>
"""

# -------------------------
# Dashboard
# -------------------------
@app.route('/')
def dashboard():
    return base_html+f"""
<div class='nav'>
<a href='/'>Dashboard</a> <a href='/students'>Students</a> <a href='/teachers'>Teachers</a> <a href='/courses'>Courses</a> <a href='/results'>Results</a>
</div>
<div class='container'>
<h1>University Dashboard</h1>
<p>Total Students: {len(data['students'])}</p>
<p>Total Teachers: {len(data['teachers'])}</p>
<p>Total Courses: {len(data['courses'])}</p>
<p>Total Results: {len(data['results'])}</p>
</div>
"""

# -------------------------
# Generic Table
# -------------------------
def render_table(entity, items, columns):
    html = "<div class='container'>"
    html += f"<h1>{entity.capitalize()}</h1>"
    html += f"<a href='/{entity}/add'><button>Add {entity[:-1].capitalize()}</button></a><br><br>"
    html += "<table><tr>"
    for col in columns: html+=f"<th>{col.capitalize()}</th>"
    html += "<th>Actions</th></tr>"
    for item in items:
        html += "<tr>"
        for col in columns: html += f"<td>{item[col]}</td>"
        html += f"<td><a href='/{entity}/edit/{item[columns[0]]}'>Edit</a> | <a href='/{entity}/delete/{item[columns[0]]}'>Delete</a></td>"
        html += "</tr>"
    html += "</table></div>"
    return base_html+"<div class='nav'><a href='/'>Dashboard</a></div>"+html

# -------------------------
# Students CRUD
# -------------------------
@app.route('/students')
def view_students(): return render_table("students",data['students'],["id","name","batch","department"])

@app.route('/students/add',methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        new={'id':request.form['id'],'name':request.form['name'],'batch':request.form['batch'],'department':request.form['department']}
        if any(s['id']==new['id'] for s in data['students']): flash("ID exists"); return redirect(request.url)
        data['students'].append(new)
        data['results'].append({'student_id':new['id'],'grades':{c['code']:'A' for c in data['courses']}})
        save_data(data)
        return redirect('/students')
    return base_html+"""
<div class='container'><h2>Add Student</h2>
<form method='post'>
ID: <input name='id'><br>
Name: <input name='name'><br>
Batch: <input name='batch'><br>
Department: <input name='department'><br>
<button type='submit'>Save</button></form></div>
"""

@app.route('/students/edit/<id>',methods=['GET','POST'])
def edit_student(id):
    s=next((x for x in data['students'] if x['id']==id),None)
    if not s: return redirect('/students')
    if request.method=='POST':
        s['id']=request.form['id']
        s['name']=request.form['name']
        s['batch']=request.form['batch']
        s['department']=request.form['department']
        save_data(data)
        return redirect('/students')
    return base_html+f"""
<div class='container'><h2>Edit Student</h2>
<form method='post'>
ID: <input name='id' value='{s['id']}'><br>
Name: <input name='name' value='{s['name']}'><br>
Batch: <input name='batch' value='{s['batch']}'><br>
Department: <input name='department' value='{s['department']}'><br>
<button type='submit'>Update</button></form></div>
"""

@app.route('/students/delete/<id>')
def delete_student(id):
    data['students']=[x for x in data['students'] if x['id']!=id]
    data['results']=[x for x in data['results'] if x['student_id']!=id]
    save_data(data)
    return redirect('/students')

# -------------------------
# Teachers, Courses, Results
# -------------------------
# [এভাবে teacher/course/result routes same CRUD logic দিয়ে বানানো হবে। copy-paste edit করলে add/edit/delete কাজ করবে]

if __name__=="__main__":
    app.run(debug=True)
