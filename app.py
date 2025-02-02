from flask import Flask, render_template, request, redirect
import mysql.connector
from config import DB_CONFIG
# Database configuration

mydb = mysql.connector.connect(**DB_CONFIG)

mycursor = mydb.cursor()
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/addnote',methods=['GET','POST'])
def addnote():
    if request.method=='POST':
        content = request.form.get('notes')
        mycursor.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        mydb.commit()
        return redirect('/')
    return render_template('addnote.html')

@app.route('/viewnote')
def viewnote():
    mycursor.execute("SELECT * FROM notes")
    notes = mycursor.fetchall()
    return render_template('viewnote.html',notes=notes)

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST':
        note_id = request.form.get('id')
        mycursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        mydb.commit()
        mycursor.execute("SET @new_id = 0") 
        mycursor.execute("UPDATE notes SET id = (@new_id := @new_id + 1)")  
        mycursor.execute("ALTER TABLE notes AUTO_INCREMENT = 1")  
        mydb.commit()
        return redirect('/')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)