# coding=utf8
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_basicauth import BasicAuth
from forms import PatientForm, PatientMHHForm, MesswerteForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user
from math import sqrt, exp
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/ScoresErgebnisse.db'
app.config['BASIC_AUTH_USERNAME'] = 'PSE'
app.config['BASIC_AUTH_PASSWORD'] = 'Schomerus'
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

class ScoresDB(db.Model):

    ID = db.Column(db.Integer, primary_key=True)
    Studie = db.Column(db.String(200), nullable=False)
    Pseudonym = db.Column(db.String(200), nullable=False)
    Alter = db.Column(db.Integer, nullable=False)
    Geschlecht = db.Column(db.String(10), nullable=False)
    Schuljahre = db.Column(db.Integer, nullable=False)
    NCTA = db.Column(db.Integer, nullable=True)
    NCTA_Score = db.Column(db.Integer, nullable=False)
    NCTB = db.Column(db.Integer, nullable=True)
    NCTB_Score = db.Column(db.Integer, nullable=False)
    LTTTIME = db.Column(db.Integer, nullable=True)
    LTTTIME_Score = db.Column(db.Integer, nullable=False)
    LTTERROR = db.Column(db.Integer, nullable=True)
    LTTERROR_Score = db.Column(db.Integer, nullable=False)
    DST = db.Column(db.Integer, nullable=True)
    DST_Score = db.Column(db.Integer, nullable=False)
    SDOT = db.Column(db.Integer, nullable=True)
    SDOT_Score = db.Column(db.Integer, nullable=False)
    Gesamt_Score = db.Column(db.Integer, nullable=False)
    Bemerkungen = db.Column(db.String(500), nullable=True)
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

	data["Gesamt_Score"] = 0

	age = int(data["age"])
	gender = int(data["gender"])
	Schuljahre = int(data["Schuljahre"])
	if data["NCTA"].isnumeric():
		NCTA = int(data["NCTA"])
	if data["NCTB"].isnumeric():
		NCTB = int(data["NCTB"])
	if data["LTTTIME"].isnumeric():
		LTTTIME = int(data["LTTTIME"])
	if data["LTTERROR"].isnumeric():
		LTTERROR = int(data["LTTERROR"])
	if data["DST"].isnumeric():
		DST = int(data["DST"])
	if data["SDOT"].isnumeric():
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
	if data["NCTA"].isnumeric():
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
		data["Gesamt_Score"] += NCTAScoreNormCOVARH2019

	else:
		data["NCTA_Score"] = -3
		data["Gesamt_Score"] += -3
		data["NCTA"] = 'missing'    
    
	# NCTB
	if data["NCTB"].isnumeric():
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
		data["Gesamt_Score"] += NCTBScoreNormCOVARH2019
	else:
		data["NCTB_Score"] = -3
		data["Gesamt_Score"] += -3
		data["NCTB"] = 'missing'    
	
	# LTT Time 
	if data["LTTTIME"].isnumeric():
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
		data["Gesamt_Score"] += LTTTIMEScoreNormCOVARH2019
	else:
		data["LTTTIME_Score"] = -3
		data["Gesamt_Score"] += -3
		data["LTTTIME"] = 'missing'
 
	# LTT Error
	if data["LTTERROR"].isnumeric():	
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
		data["Gesamt_Score"] +=  LTTERRORScoreNormCOVARH2019
	else:
		data["LTTERROR_Score"] = -3
		data["Gesamt_Score"] += -3
		data["LTTERROR"] = 'missing'    
   
	#  DST
	if data["DST"].isnumeric():
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
		data["Gesamt_Score"] += DSTScoreNormCOVARH2019
	else:
		data["DST_Score"] = -3
		data["Gesamt_Score"] += -3
		data["DST"] = 'missing'    

	# SDOT	
	if data["SDOT"].isnumeric():	
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
		data["Gesamt_Score"] += SDOTScoreNormCOVARH2019
	else:
		data["SDOT_Score"] = -3
		data["Gesamt_Score"] += -3
		data["SDOT"] = 'missing'   
    
	return data

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	return render_template('home.html', title='PSE-Hauptseite')

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
    data["Datum"] = datetime.now().strftime('%d.%m.%Y %H:%M')         
     
    data = calculate_score(data)
    
    db_data = {}
    db_data["Studie"] = session.get("Studie")
    db_data["Pseudonym"] = session.get("Pseudonym")
    db_data["age"] = session.get("age")
    db_data["Schuljahre"] = session.get("Schuljahre")
    db_data["gender"] = session.get("gender")
    db_data["NCTA"] = session.get("NCTA")
    if db_data["NCTA"] == 'missing':
        db_data["NCTA"] = ''  
    db_data["NCTA_Score"] = data["NCTA_Score"]
    
    db_data["NCTB"] = session.get("NCTB")
    if db_data["NCTB"] == 'missing':     
        db_data["NCTB"] = ''
    db_data["NCTB_Score"] = data["NCTB_Score"]
    
    db_data["LTTTIME"] = session.get("LTTTIME")
    if db_data["LTTTIME"] == 'missing':
        db_data["LTTTIME"] = ''
    db_data["LTTTIME_Score"] = data["LTTTIME_Score"]
    
    db_data["LTTERROR"] = session.get("LTTERROR")
    if db_data["LTTERROR"] == 'missing': 
        db_data["LTTERROR"] = ''  
    db_data["LTTERROR_Score"] = data["LTTERROR_Score"]
    
    db_data["DST"] = session.get("DST")
    if db_data["DST"] == 'missing':
        db_data["DST"] = ''
    db_data["DST_Score"] = data["DST_Score"]
    
    db_data["SDOT"] = session.get("SDOT")
    if db_data["SDOT"] == 'missing':
        db_data["SDOT"] = ''   
    db_data["SDOT_Score"] = data["SDOT_Score"]
    
    db_data["Gesamt_Score"] = data["Gesamt_Score"]
    
    db_data["notizen"] = session.get("notizen") 
    db_data["Datum"] = datetime.now().strftime('%d.%m.%Y %H:%M')     

    if db_data["Studie"] != "" and db_data["Pseudonym"] != "":
        scoresDB = ScoresDB(Studie        = db_data["Studie"],
                            Pseudonym     = db_data["Pseudonym"],
                            Alter         = db_data["age"],
                            Geschlecht    = db_data["gender"],
                            Schuljahre    = db_data["Schuljahre"],
                            NCTA          = db_data["NCTA"],
                            NCTA_Score    = db_data["NCTA_Score"],                            
                            NCTB          = db_data["NCTB"],
                            NCTB_Score    = db_data["NCTB_Score"],                            
                            LTTTIME       = db_data["LTTTIME"],
                            LTTTIME_Score = db_data["LTTTIME_Score"],                            
                            LTTERROR      = db_data["LTTERROR"],
                            LTTERROR_Score= db_data["LTTERROR_Score"],                            
                            DST           = db_data["DST"],
                            DST_Score     = db_data["DST_Score"],                            
                            SDOT          = db_data["SDOT"],
                            SDOT_Score    = db_data["SDOT_Score"],      
                            Gesamt_Score  = db_data["Gesamt_Score"],
                            Bemerkungen   = db_data["notizen"])
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
    return render_template('patient.html', title='Patientendaten Extern', 
    						form=form)


@app.route("/patientMHH", methods=['GET', 'POST'])
@basic_auth.required
def patientMHH():
    form = PatientMHHForm()
    req = request.form
    flash(u"MHH-Modus - Werte werden abgespeichert!", 'info')
    geflasht = True 
    if form.validate_on_submit():
        session["Studie"] = req.get("Studie")
        session["Pseudonym"] =  req.get("Pseudonym")
        session["age"] =  req.get("age")
        session["Schuljahre"] = req.get("Schuljahre")
        session["gender"] = req.get("gender")
        return redirect(url_for('messwerte'))
    return render_template('patientMHH.html', title='Patientendaten MHH', 
    						form=form)  
  
@app.route("/messwerte", methods=['GET', 'POST'])
def messwerte():
    form = MesswerteForm() 
    req = request.form
    geflasht = False
    if form.validate_on_submit():
        session["NCTA"] =  req.get("NCTA") 
        if session["NCTA"].isnumeric() and int(session["NCTA"]) > 80:
          flash(u"Extremer Wert für 'Zahlen verbinden (A)' ", 'warning')
          geflasht = True          
        session["NCTB"] =  req.get("NCTB")
        if session["NCTB"].isnumeric() and int(session["NCTB"]) > 250:
          flash(u"Extremer Wert für 'Zahlen verbinden (B)' ", 'warning')
          geflasht = True           
        session["LTTTIME"] =  req.get("LTTTIME")
        if session["LTTTIME"].isnumeric() and int(session["LTTTIME"]) > 500:
          flash(u"Extremer Wert für 'Linien nachfahren (Zeit)' ", 'warning')
          geflasht = True           
        session["LTTERROR"] = req.get("LTTERROR")
        if session["LTTERROR"].isnumeric() and int(session["LTTERROR"]) > 200:
          flash(u"Extremer Wert für 'Linien nachfahren (Fehler)' ", 'warning')
          geflasht = True  
        session["DST"] =  req.get("DST")
        if session["DST"].isnumeric() and int(session["DST"]) > 400:
          flash(u"Extremer Wert für 'Zahlen Symbol Test' ", 'warning')
          geflasht = True          
        session["SDOT"] =  req.get("SDOT")
        if session["SDOT"].isnumeric() and int(session["SDOT"]) > 300:
          flash(u"Extremer Wert für 'Kreise punktieren' ", 'warning')
          geflasht = True           
        session["notizen"] =  req.get("notizen")
        if geflasht:
          flash(u"Korrekturmöglichkeit mit Browsernavigation", 'info')
        return redirect(url_for('ergebnisse'))
    return render_template('messwerte.html', title='Messwerte', 
    						form=form)    

  
if __name__ == '__main__':
	app.run(debug=True)