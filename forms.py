# coding=utf8
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, BooleanField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class PatientForm(FlaskForm):
    Patient = StringField('Patientenidentifikation',
                        validators=[Length(min=2, max=200, message=(u'Wenigstens 2 und höchstens 200 Buchstaben'))])
    age = IntegerField('Alter',
                        validators=[DataRequired(),
                                    NumberRange(min=5, max=100, message=(u'Ungültige Altersangabe'))])
    Schuljahre = IntegerField('Schuljahre',
                        validators=[DataRequired(),
                             NumberRange(min=5, max=20, message=(u'Ungültige Angabe'))])
    gender = SelectField('Geschlecht', coerce=int,
                        choices=[(0, '--'), 
                                (1, u'männlich'), 
                                (2, 'weiblich')],
                        validators=[DataRequired(message="Bitte treffen Sie eine Auswahl")])

    submit = SubmitField('Weiter zur Erfassung der Messwerte')

    
class PatientMHHForm(FlaskForm):
    Studie = StringField('Studie',
                        validators=[Length(min=2, max=200, message=(u'Wenigstens 2 und höchstens 200 Buchstaben'))])
    Pseudonym = StringField('Pseudonym',
                        validators=[Length(min=2, max=200, message=(u'Wenigstens 2 und höchstens 200 Buchstaben'))],
                           render_kw={"placeholder": "Warnung: Dieser Wert wird in einer Cloud-Datenbank abgespeichert"})
    age = IntegerField('Alter',
                        validators=[DataRequired(),
                                    NumberRange(min=5, max=100, message=(u'Ungültige Altersangabe'))])
    Schuljahre = IntegerField('Schuljahre',
                        validators=[DataRequired(),
                             NumberRange(min=5, max=20, message=(u'Ungültige Angabe'))])
    gender = SelectField('Geschlecht', coerce=int,
                        choices=[(0, '--'), 
                                (1, u'männlich'), 
                                (2, 'weiblich')],
                        validators=[DataRequired(message="Bitte treffen Sie eine Auswahl")])

    submit = SubmitField('Weiter zur Erfassung der Messwerte')    
    
class MesswerteForm(FlaskForm):
    NCTA = IntegerField('Zahlen verbinden (A) (Zeit in Sekunden)',
                        validators=[NumberRange(min=1, message=(u'Wert muss größer als 0 sein')),
                        Optional()])
    NCTB = IntegerField('Zahlen verbinden (B) (Zeit in Sekunden)', 
    	                validators=[NumberRange(min=1, message=(u'Wert muss größer als 0 sein')), 
                      Optional()])            
    LTTTIME = IntegerField('Linien nachfahren (Zeit in Sekunden)', 
    	                validators=[NumberRange(min=1, message=(u'Wert muss größer als 0 sein')),
                      Optional()])            
    LTTERROR = IntegerField('Linien nachfahren (Fehler)', 
    	                validators=[NumberRange(min=0, message=(u'Wert muss größer oder gleich 0 sein')),
                      Optional()])      
    DST = IntegerField('Zahlen Symbol Test (Anzahl)', 
    	                validators=[NumberRange(min=1, message=(u'Wert muss größer als 0 sein')),
                      Optional()])            
    SDOT = IntegerField('Kreise punktieren (Zeit in Sekunden)', 
                        validators=[NumberRange(min=1, message=(u'Wert muss größer als 0 sein')),
                        Optional()])

    notizen = TextAreaField('Bemerkungen', render_kw={"rows": 5, "cols": 50},
                           validators=[Length(max=500, message=(u'Notizen sind auf 500 Zeichen begrenzt'))])
    submit = SubmitField('Calculate Score')
