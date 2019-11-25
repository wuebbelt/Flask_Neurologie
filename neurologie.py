# coding=utf8
from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import PatientForm, MesswerteForm, StartForm
from flask_sqlalchemy import SQLAlchemy
from math import sqrt, exp
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/ScoresErgebnisse.db'
db = SQLAlchemy(app)

class ScoresDB(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Schuljahre = db.Column(db.Integer, nullable=False)
    NCTA = db.Column(db.Integer, nullable=True)
    NCTB = db.Column(db.Integer, nullable=True)
    LTTTIME = db.Column(db.Integer, nullable=True)
    LTTERROR = db.Column(db.Integer, nullable=True)
    DST = db.Column(db.Integer, nullable=True)
    SDOT = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def calculate_score(data):

	"""
	Variables:
	NCTA 'NCTA: Number connection test (A); ZV A: Zahlen verbinden (A) (Zeit)'/
	NCTB 'NCTB: Number connection test (B); ZV B: Zahlen verbinden (A) (Zeit)'/
	LTTTIME 'LTT time: Line Tracing test (time); LNZ: Linien nachfahren (Zeit)'/
	LTTERROR  'LTT Error: Line Tracing test (errors); LNZ: Linien nachfahren (Fehler)'/
	DST 'DST: Digit Symbol test; ZS: Zahlen Symbol Test (Anzahl)'/
	SDOT 'SDOT: Serial Dotting test; KP: Kreise punktieren (Zeit)'/.

	Covariates:
	age
	gender
	Schuljahre
	"""

	age = int(data["age"])
	gender = int(data["gender"])
	Schuljahre = int(data["Schuljahre"])
	NCTA = int(data["NCTA"])
	NCTB = int(data["NCTB"])
	LTTTIME = int(data["LTTTIME"])
	LTTERROR = int(data["LTTERROR"])
	DST = int(data["DST"])
	SDOT = int(data["SDOT"])

	# Umkodierung (falls nötig):  Schuljahre in 3 Kategorien
	# Formal Educarion as contrast variables 
	if Schuljahre <= 9:
		FormalEducation = 1
	elif Schuljahre <= 12:
		FormalEducation = 2
	else:
		FormalEducation = 3

	# Formal Educarion as contrast variables .
	if FormalEducation == 2:
		FormalEducation2 = 1
	else:
		FormalEducation2 = 0
	if FormalEducation == 3:
		FormalEducation3 = 1
	else:
		FormalEducation3 = 0
	if FormalEducation == 3 or FormalEducation == 2:
		FormalEducation23 = 1
	else:
		FormalEducation23 = 0

	# gender
	gender -= 1	

	# NCTA 
	aNCTACovarH2019 = 2.641457
	b_ageNCTACovarH2019 = 0.010871
	b_FormalEducation2NCTACovarH2019 = 0
	b_FormalEducation3NCTACovarH2019=  0
	sNCTACovarH2019 = sqrt(0.079413)

	NCTA0COVARH2019  = exp(aNCTACovarH2019  + b_ageNCTACovarH2019 *age + b_FormalEducation2NCTACovarH2019 * FormalEducation2    + b_FormalEducation3NCTACovarH2019 * FormalEducation3 + 0 *sNCTACovarH2019  )
	NCTA1COVARH2019  = exp(aNCTACovarH2019  + b_ageNCTACovarH2019 *age + b_FormalEducation2NCTACovarH2019 * FormalEducation2    + b_FormalEducation3NCTACovarH2019 * FormalEducation3 + 1 * sNCTACovarH2019  )
	NCTA2COVARH2019  = exp(aNCTACovarH2019 + b_ageNCTACovarH2019 *age + b_FormalEducation2NCTACovarH2019 * FormalEducation2    + b_FormalEducation3NCTACovarH2019 * FormalEducation3 + 2* sNCTACovarH2019 )
	NCTA3COVARH2019  = exp(aNCTACovarH2019  + b_ageNCTACovarH2019 *age + b_FormalEducation2NCTACovarH2019 * FormalEducation2    + b_FormalEducation3NCTACovarH2019 * FormalEducation3 + 3 * sNCTACovarH2019  )
	NCTAm1COVARH2019 = exp(aNCTACovarH2019  + b_ageNCTACovarH2019 *age + b_FormalEducation2NCTACovarH2019 * FormalEducation2    + b_FormalEducation3NCTACovarH2019 * FormalEducation3 - 1 * sNCTACovarH2019 )

	NCTAScoreNormCOVARH2019 = 0
	if (NCTA >= NCTA1COVARH2019 ): NCTAScoreNormCOVARH2019 = -1
	if (NCTA >= NCTA2COVARH2019 ): NCTAScoreNormCOVARH2019  = -2
	if (NCTA >= NCTA3COVARH2019 ): NCTAScoreNormCOVARH2019 = -3
	if (NCTA <= NCTAm1COVARH2019): NCTAScoreNormCOVARH2019  = +1

	data["NCTA_Score"] = NCTAScoreNormCOVARH2019


	# NCTB
	aNCTBCovarH2019 = 3.830604
	b_ageNCTBCovarH2019 = 0.010027
	b_FormalEducation2NCTBCovarH2019 = -0.184867
	b_FormalEducation3NCTBCovarH2019 =-0.34977319  
	sNCTBCovarH2019 = sqrt(0.07484)

	NCTB0COVARH2019  = exp(aNCTBCovarH2019  + b_ageNCTBCovarH2019 *age + b_FormalEducation2NCTBCovarH2019 * FormalEducation2    + b_FormalEducation3NCTBCovarH2019 * FormalEducation3 + 0 *sNCTBCovarH2019  )
	NCTB1COVARH2019  = exp(aNCTBCovarH2019  + b_ageNCTBCovarH2019 *age + b_FormalEducation2NCTBCovarH2019 * FormalEducation2    + b_FormalEducation3NCTBCovarH2019 * FormalEducation3 + 1 * sNCTBCovarH2019  )
	NCTB2COVARH2019  = exp(aNCTBCovarH2019 + b_ageNCTBCovarH2019 *age + b_FormalEducation2NCTBCovarH2019 * FormalEducation2    + b_FormalEducation3NCTBCovarH2019 * FormalEducation3 + 2* sNCTBCovarH2019 )
	NCTB3COVARH2019  = exp(aNCTBCovarH2019  + b_ageNCTBCovarH2019 *age + b_FormalEducation2NCTBCovarH2019 * FormalEducation2    + b_FormalEducation3NCTBCovarH2019 * FormalEducation3 + 3 * sNCTBCovarH2019  )
	NCTBm1COVARH2019 = exp(aNCTBCovarH2019  + b_ageNCTBCovarH2019 *age + b_FormalEducation2NCTBCovarH2019 * FormalEducation2    + b_FormalEducation3NCTBCovarH2019 * FormalEducation3 - 1 * sNCTBCovarH2019 )

	NCTBScoreNormCOVARH2019= 0.
	if (NCTB >= NCTB1COVARH2019 ): NCTBScoreNormCOVARH2019 = -1
	if (NCTB >= NCTB2COVARH2019 ): NCTBScoreNormCOVARH2019  = -2
	if (NCTB >= NCTB3COVARH2019 ): NCTBScoreNormCOVARH2019 = -3
	if (NCTB <= NCTBm1COVARH2019): NCTBScoreNormCOVARH2019  = +1

	data["NCTB_Score"] = NCTBScoreNormCOVARH2019

	
	# LTT Time 
	aLTTTIMECovarH2019 = 4.131675
	b_ageLTTTIMECovarH2019 = 0.003448
	b_FormalEducation2LTTTIMECovarH2019 = 0
	b_FormalEducation3LTTTIMECovarH2019=  0
	sLTTTIMECovarH2019 = sqrt(0.077122)

	LTTTIME0COVARH2019  = exp(aLTTTIMECovarH2019  + b_ageLTTTIMECovarH2019 *age + b_FormalEducation2LTTTIMECovarH2019 * FormalEducation2    + b_FormalEducation3LTTTIMECovarH2019 * FormalEducation3 + 0 *sLTTTIMECovarH2019  )
	LTTTIME1COVARH2019  = exp(aLTTTIMECovarH2019  + b_ageLTTTIMECovarH2019 *age + b_FormalEducation2LTTTIMECovarH2019 * FormalEducation2    + b_FormalEducation3LTTTIMECovarH2019 * FormalEducation3 + 1 * sLTTTIMECovarH2019  )
	LTTTIME2COVARH2019  = exp(aLTTTIMECovarH2019 + b_ageLTTTIMECovarH2019 *age + b_FormalEducation2LTTTIMECovarH2019 * FormalEducation2    + b_FormalEducation3LTTTIMECovarH2019 * FormalEducation3 + 2* sLTTTIMECovarH2019 )
	LTTTIME3COVARH2019  = exp(aLTTTIMECovarH2019  + b_ageLTTTIMECovarH2019 *age + b_FormalEducation2LTTTIMECovarH2019 * FormalEducation2    + b_FormalEducation3LTTTIMECovarH2019 * FormalEducation3 + 3 * sLTTTIMECovarH2019  )
	LTTTIMEm1COVARH2019 = exp(aLTTTIMECovarH2019  + b_ageLTTTIMECovarH2019 *age + b_FormalEducation2LTTTIMECovarH2019 * FormalEducation2    + b_FormalEducation3LTTTIMECovarH2019 * FormalEducation3 - 1 * sLTTTIMECovarH2019 )

	LTTTIMEScoreNormCOVARH2019= 0
	if (LTTTIME >= LTTTIME1COVARH2019 ): LTTTIMEScoreNormCOVARH2019 = -1
	if (LTTTIME >= LTTTIME2COVARH2019 ): LTTTIMEScoreNormCOVARH2019  = -2
	if (LTTTIME >= LTTTIME3COVARH2019 ): LTTTIMEScoreNormCOVARH2019 = -3
	if (LTTTIME <= LTTTIMEm1COVARH2019): LTTTIMEScoreNormCOVARH2019  = +1

	data["LTTTIME_Score"] = LTTTIMEScoreNormCOVARH2019


	# LTT Error
	aLTTERRORCovarH2019 = 2.558560 
	b_ageLTTERRORCovarH2019 = 0.051284
	b_FormalEducation2LTTERRORCovarH2019 = 0
	b_FormalEducation3LTTERRORCovarH2019=  0
	sLTTERRORCovarH2019 = sqrt( 3.860729)

	LTTERROR0COVARH2019  = (aLTTERRORCovarH2019  + b_ageLTTERRORCovarH2019 *age + b_FormalEducation2LTTERRORCovarH2019 * FormalEducation2    + b_FormalEducation3LTTERRORCovarH2019 * FormalEducation3 + 0 *sLTTERRORCovarH2019  )**2
	LTTERROR1COVARH2019  = (aLTTERRORCovarH2019  + b_ageLTTERRORCovarH2019 *age + b_FormalEducation2LTTERRORCovarH2019 * FormalEducation2    + b_FormalEducation3LTTERRORCovarH2019 * FormalEducation3 + 1 * sLTTERRORCovarH2019  )**2
	LTTERROR2COVARH2019  = (aLTTERRORCovarH2019 + b_ageLTTERRORCovarH2019 *age + b_FormalEducation2LTTERRORCovarH2019 * FormalEducation2    + b_FormalEducation3LTTERRORCovarH2019 * FormalEducation3 + 2* sLTTERRORCovarH2019 )**2
	LTTERROR3COVARH2019  = (aLTTERRORCovarH2019  + b_ageLTTERRORCovarH2019 *age + b_FormalEducation2LTTERRORCovarH2019 * FormalEducation2    + b_FormalEducation3LTTERRORCovarH2019 * FormalEducation3 + 3 * sLTTERRORCovarH2019  )**2
	LTTERRORm1COVARH2019 = (aLTTERRORCovarH2019  + b_ageLTTERRORCovarH2019 *age + b_FormalEducation2LTTERRORCovarH2019 * FormalEducation2    + b_FormalEducation3LTTERRORCovarH2019 * FormalEducation3 - 1 * sLTTERRORCovarH2019 )**2

	LTTERRORScoreNormCOVARH2019= 0
	if (LTTERROR >= LTTERROR1COVARH2019 ): LTTERRORScoreNormCOVARH2019 = -1
	if (LTTERROR >= LTTERROR2COVARH2019 ): LTTERRORScoreNormCOVARH2019  = -2
	if (LTTERROR >= LTTERROR3COVARH2019 ): LTTERRORScoreNormCOVARH2019 = -3
	if (LTTERROR <= LTTERRORm1COVARH2019): LTTERRORScoreNormCOVARH2019  = +1

	data["LTTERROR_Score"] = LTTERRORScoreNormCOVARH2019 


	#  DST
	aDSTCovarH2019 = 4.103133
	b_ageDSTCovarH2019 = -0.006395
	b_FormalEducation2DSTCovarH2019 = 0.091533
	b_FormalEducation3DSTCovarH2019=  0.138129
	b_genderDSTCovarH2019 = 0.076659
	sDSTCovarH2019 = sqrt(0.025989)

	DST0COVARH2019  = exp(aDSTCovarH2019 + b_ageDSTCovarH2019 *age + b_FormalEducation2DSTCovarH2019 * FormalEducation2    + b_FormalEducation3DSTCovarH2019 * FormalEducation3  + b_genderDSTCovarH2019 * gender + 0 *sDSTCovarH2019  )
	DST1COVARH2019  = exp(aDSTCovarH2019 + b_ageDSTCovarH2019 *age + b_FormalEducation2DSTCovarH2019 * FormalEducation2    + b_FormalEducation3DSTCovarH2019 * FormalEducation3 + b_genderDSTCovarH2019 * gender -  1 * sDSTCovarH2019  )
	DST2COVARH2019  = exp(aDSTCovarH2019 + b_ageDSTCovarH2019 *age + b_FormalEducation2DSTCovarH2019 * FormalEducation2    + b_FormalEducation3DSTCovarH2019 * FormalEducation3 + b_genderDSTCovarH2019 * gender - 2 * sDSTCovarH2019 )
	DST3COVARH2019  = exp(aDSTCovarH2019 + b_ageDSTCovarH2019 *age + b_FormalEducation2DSTCovarH2019 * FormalEducation2    + b_FormalEducation3DSTCovarH2019 * FormalEducation3 + b_genderDSTCovarH2019 * gender - 3 * sDSTCovarH2019  )
	DSTp1COVARH2019 = exp(aDSTCovarH2019 + b_ageDSTCovarH2019 *age + b_FormalEducation2DSTCovarH2019 * FormalEducation2    + b_FormalEducation3DSTCovarH2019 * FormalEducation3  + b_genderDSTCovarH2019 * gender + 1 * sDSTCovarH2019 )

	DSTScoreNormCOVARH2019= 0
	if (DST <= DST1COVARH2019 ): DSTScoreNormCOVARH2019 = -1
	if (DST <= DST2COVARH2019 ): DSTScoreNormCOVARH2019  = -2
	if (DST <= DST3COVARH2019 ): DSTScoreNormCOVARH2019 = -3
	if (DST >= DSTp1COVARH2019): DSTScoreNormCOVARH2019  = +1

	data["DST_Score"] = DSTScoreNormCOVARH2019


	# SDOT	
	aSDOTCovarH2019 = 1.259429
	b_ageSDOTCovarH2019 = 0.001204
	b_FormalEducation23SDOTCovarH2019 = -0.026057 
	sSDOTCovarH2019 = sqrt(0.001729)

	SDOT0COVARH2019  = exp(exp(aSDOTCovarH2019 + b_ageSDOTCovarH2019 *age + b_FormalEducation23SDOTCovarH2019 * FormalEducation23    + 0 *sSDOTCovarH2019  ))
	SDOT1COVARH2019  = exp(exp(aSDOTCovarH2019 + b_ageSDOTCovarH2019 *age + b_FormalEducation23SDOTCovarH2019 * FormalEducation23   + 1 * sSDOTCovarH2019  ))
	SDOT2COVARH2019  = exp(exp(aSDOTCovarH2019 + b_ageSDOTCovarH2019 *age +  b_FormalEducation23SDOTCovarH2019 * FormalEducation23   + 2* sSDOTCovarH2019 ))
	SDOT3COVARH2019  = exp(exp(aSDOTCovarH2019 + b_ageSDOTCovarH2019 *age +  b_FormalEducation23SDOTCovarH2019 * FormalEducation23   + 3 * sSDOTCovarH2019  ))
	SDOTm1COVARH2019 = exp(exp(aSDOTCovarH2019 + b_ageSDOTCovarH2019 *age +b_FormalEducation23SDOTCovarH2019 * FormalEducation23   - 1 * sSDOTCovarH2019 ))

	SDOTScoreNormCOVARH2019= 0
	if (SDOT >= SDOT1COVARH2019 ): SDOTScoreNormCOVARH2019 = -1
	if (SDOT >= SDOT2COVARH2019 ): SDOTScoreNormCOVARH2019  = -2
	if (SDOT >= SDOT3COVARH2019 ): SDOTScoreNormCOVARH2019 = -3
	if (SDOT <= SDOTm1COVARH2019): SDOTScoreNormCOVARH2019  = +1

	data["SDOT_Score"] = SDOTScoreNormCOVARH2019 

	return data


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	form = StartForm()
	if form.validate_on_submit(): 
		session["patient"] =  "" 
		return redirect(url_for('patient'))
	return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/ergebnisse")
def ergebnisse():
    """
    NCTA 'NCTA: Number connection test (A); ZV A: Zahlen verbinden (A) (Zeit)'/
    NCTB 'NCTB: Number connection test (B); ZV B: Zahlen verbinden (A) (Zeit)'/
    LTTTIME 'LTT time: Line Tracing test (time); LNZ: Linien nachfahren (Zeit)'/
    LTTERROR  'LTT Error: Line Tracing test (errors); LNZ: Linien nachfahren (Fehler)'/
    DST 'DST: Digit Symbol test; ZS: Zahlen Symbol Test (Anzahl)'/
    SDOT 'SDOT: Serial Dotting test; KP: Kreise punktieren (Zeit)'/.
	
    Covariates:
    Age
    gender
    Schuljahre
    """

    # User Input
    data = {}
    data["Patient"] = session.get("Patient")
    data["age"] = session.get("age")
    data["Schuljahre"] = session.get("Schuljahre")
    data["gender"] = session.get("gender")
    data["NCTA"] = session.get("NCTA")
    data["NCTB"] = session.get("NCTB")
    data["LTTTIME"] = session.get("LTTTIME")
    data["LTTERROR"] = session.get("LTTERROR")
    data["DST"] = session.get("DST")
    data["SDOT"] = session.get("SDOT")
    data["notizen"] = session.get("notizen")

    data = calculate_score(data)

    if (data["gender"] == 1):
    	gender_decode = 'maennlich'
    else:
    	gender_decode = 'weiblich'
    scoresDB = ScoresDB(age=data["age"],
                        gender=data["gender"],
                        Schuljahre=data["Schuljahre"],
                        NCTA=data["NCTA"],
                        NCTB=data["NCTB"],
                        LTTTIME=data["LTTTIME"],
                        LTTERROR=data["LTTERROR"],
                        DST=data["DST"],
                        SDOT=data["SDOT"])
    db.session.add(scoresDB)
    db.session.commit()

    return render_template('ergebnisse.html', title='Ergebnisse', 
    	                    data=data)

@app.route("/patient", methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    req = request.form
    if form.validate_on_submit():
        session["Patient"] =  req.get("Patient")
        session["age"] =  req.get("age")
        session["Schuljahre"] = req.get("Schuljahre")
        session["gender"] = req.get("gender")
        return redirect(url_for('messwerte'))
    return render_template('patient.html', title='Patientendaten', 
    						form=form)


@app.route("/messwerte", methods=['GET', 'POST'])
def messwerte():
    form = MesswerteForm() 
    req = request.form
    print(form.validate_on_submit())
    print(req.get("NCTA"))
    session["NCTA"] =  req.get("NCTA", None) 
    print(session["NCTA"])
    if session["NCTA"] == '': print("Hallo")
    if form.validate_on_submit():
        print(req.get("NCTA"))
        session["NCTA"] =  req.get("NCTA", None) 
        print(req.get("NCTA"))
        session["NCTB"] =  req.get("NCTB")
        session["LTTTIME"] =  req.get("LTTTIME")
        session["LTTERROR"] = req.get("LTTERROR")
        session["DST"] =  req.get("DST")
        session["SDOT"] =  req.get("SDOT")
        session["notizen"] =  req.get("notizen")
        return redirect(url_for('ergebnisse'))
    return render_template('messwerte.html', title='Messwerte', 
    						form=form)    


if __name__ == '__main__':
	app.run(debug=True)