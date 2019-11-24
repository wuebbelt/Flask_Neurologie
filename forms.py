# coding=utf8
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class StartForm(FlaskForm):
    submit = SubmitField('Start der Auswertung')


class PatientForm(FlaskForm):
    Patient = StringField('Patientenidentifikation',
                        validators=[Length(min=2, max=40)])
    age = IntegerField('Alter',
                        validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    Schuljahre = IntegerField('Schuljahre',
                        validators=[DataRequired()])
    gender = SelectField('Geschlecht', coerce=int,
                        choices=[(0, '--'), 
                                (1, 'männlich'), 
                                (2, 'weiblich')],
                        validators=[DataRequired(message="Bitte treffen Sie eine Auswahl")])

    submit = SubmitField('Weiter zur Erfassung der Messwerte')

class MesswerteForm(FlaskForm):
    NCTA = IntegerField('Zahlen verbinden (A) (Zeit in Sekunden)',
                        validators=[NumberRange(min=5, max=100)])
    NCTB = IntegerField('Zahlen verbinden (B) (Zeit in Sekunden)', 
    	                validators=[NumberRange(min=5, max=100)])
    LTTTIME = IntegerField('Linien nachfahren (Zeit in Sekunden)', 
    	                validators=[NumberRange(min=5, max=100)])
    LTTERROR = IntegerField('Linien nachfahren (Fehler)', 
    	                validators=[NumberRange(min=5, max=100)])
    DST = IntegerField('Zahlen Symbol Test (Anzahl)', 
    	                validators=[NumberRange(min=5, max=100)])
    SDOT = IntegerField('Kreise punktieren (Zeit in Sekunden)', 
                        validators=[NumberRange(min=5, max=100)])

    notizen = TextAreaField('Bemerkungen', render_kw={"rows": 5, "cols": 50})
    submit = SubmitField('Calculate Score')
