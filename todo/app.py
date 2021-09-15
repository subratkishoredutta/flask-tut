# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 17:14:38 2021

@author: Asus
"""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    task=db.Column(db.String(200), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    flag=db.Column(db.Integer, nullable=False)
    
    def __repr__(self)-> str :
        return F"{self.sno}-{self.task}"
    
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        task=request.form['task']
        desc=request.form['description']
        todo =Todo(task=task,description=desc,flag=1)
        db.session.add(todo)
        db.session.commit()
    allto=Todo.query.all()
    return render_template('index.html',allto=allto)
    
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        task=request.form['task']
        desc=request.form['description']
        todo =Todo.query.filter_by(sno=sno).first()
        todo.task=task
        todo.description=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    updrec=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',updrec=updrec)

@app.route('/done/<int:sno>',methods=['GET','POST'])
def done(sno):
    donerec=Todo.query.filter_by(sno=sno).first()
    donerec.flag=0
    db.session.add(donerec)
    db.session.commit()
    return redirect('/')
    
@app.route('/delete/<int:sno>')
def delete(sno):
    delrec=Todo.query.filter_by(sno=sno).first()
    db.session.delete(delrec)
    db.session.commit()
    return redirect('/')

if __name__ =="__main__":
    app.run(debug=True,port=5000)
