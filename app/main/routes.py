from flask import render_template, url_for, flash, redirect, request, session
from . import main
from .forms import PatientForm, MesswerteForm, StartForm


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
	form = StartForm()
	if form.validate_on_submit(): 
		session["main.patient"] =  "" 
		return redirect(url_for('main.patient'))
	return render_template('home.html', form=form)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/ergebnisse")
def ergebnisse():
    data={}
    data["patient"]=session.get("patient")
    data["alter"]=session.get("alter")
    data["schuljahre"]=session.get("schuljahre")
    data["geschlecht"]=session.get("geschlecht")
    data["test1"]=session.get("test1")
    data["test2"]=session.get("test2")
    data["test3"]=session.get("test3")
    data["test4"]=session.get("test4")
    data["notizen"]=session.get("notizen")
    return render_template('ergebnisse.html', title='Ergebnisse', 
    	                    data=data)


@main.route("/patient", methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    req = request.form
    if form.validate_on_submit():
    	session["patient"] =  req.get("patient") 
    	session["alter"] =  req.get("alter")
    	session["schuljahre"] = req.get("schuljahre")
    	session["geschlecht"] = req.get("geschlecht") 
    	return redirect(url_for('main.messwerte'))
    return render_template('patient.html', title='Patientendaten', form=form)


@main.route("/messwerte", methods=['GET', 'POST'])
def messwerte():
    form = MesswerteForm() 
    req = request.form
    if form.validate_on_submit():
    	session["test1"] =  req.get("test1") 
    	session["test2"] =  req.get("test2") 	
    	session["test3"] =  req.get("test3") 	
    	session["test4"] =  req.get("test4") 	
    	session["test5"] =  req.get("test5") 	
    	session["notizen"] =  req.get("notizen") 		
    	return redirect(url_for('main.ergebnisse'))
    return render_template('messwerte.html', title='Messwerte', form=form)
