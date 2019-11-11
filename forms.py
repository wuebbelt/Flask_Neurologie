from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class StartForm(FlaskForm):
    submit = SubmitField('Start der Auswertung')

class PatientForm(FlaskForm):
    patient = StringField('Patientenidentifikation',
                        validators=[DataRequired(), 
                                    Length(min=2, max=40)])
    alter = IntegerField('Alter',
                        validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    schuljahre = IntegerField('Schuljahre',
                        validators=[DataRequired()])
    geschlecht = SelectField('Geschlecht', 
    	               choices=[('-', '--'), 
                                ('1', 'männlich'), 
                                ('0', 'weiblich')])
    submit = SubmitField('Weiter zur Erfassung der Messwerte')


class MesswerteForm(FlaskForm):
    test1 = IntegerField('Test Nr.1 - Zahlen-Symbol-Test',
                        validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    test2 = IntegerField('Test Nr.2 - ZVT-A-Testblatt', 
    	                validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    test3 = IntegerField('Test Nr.3 - ZVT-B-Testblatt', 
    	                validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    test4 = IntegerField('Test Nr.4 - Kreise punktieren', 
    	                validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    test5 = IntegerField('Test Nr.5 - Linie nachfahren', 
    	                validators=[DataRequired(),
                                    NumberRange(min=5, max=100)])
    notizen = TextAreaField('Bemerkungen', render_kw={"rows": 5, "cols": 50})
    submit = SubmitField('Calculate Score')
