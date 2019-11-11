from flask import render_template, url_for, flash, redirect, request, session
from forms import PatientForm, MesswerteForm, StartForm

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	form = StartForm()
	if form.validate_on_submit(): 
		session["main.patient"] =  "" 
		return redirect(url_for('patient'))
	return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/ergebnisse")
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


@app.route("/patient", methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    req = request.form
    if form.validate_on_submit():
    	session["patient"] =  req.get("patient") 
    	session["alter"] =  req.get("alter")
    	session["schuljahre"] = req.get("schuljahre")
    	session["geschlecht"] = req.get("geschlecht") 
    	return redirect(url_for('messwerte'))
    return render_template('patient.html', title='Patientendaten', form=form)


@app.route("/messwerte", methods=['GET', 'POST'])
def messwerte():
    form = MesswerteForm() 
    req = request.form
    if form.validate_on_submit():
    	session["test1"] =  req.get("test1") 

if __name__ == '__main__':
	app.run(debug=True)