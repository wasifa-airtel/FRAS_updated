from flask_wtf import FlaskForm
from wtforms import  FieldList ,StringField,validators, FormField, SubmitField,IntegerField,ValidationError,SelectField,TextField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from wtforms_components import DateRange
from datetime import datetime, date
from model import *
from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
    dt = DateField("Registration Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    name =StringField('Name', validators=[DataRequired()])
    service_id =StringField('Service id', validators=[DataRequired()])
    
    submit = SubmitField('Save')


class RegistrationFormBulk(FlaskForm):
    addresses = FieldList(FormField(RegistrationForm), min_entries=3)
    
class RegistrationEditForm(FlaskForm):
    date =  DateField("Registration Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
    name =StringField('Name', validators=[DataRequired()])
    service_id =StringField('Serice id', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    dob = DateField('Date', format='%Y-%m-%d')
    cantonment =StringField('Cantonment', validators=[DataRequired()])
    brigade =StringField('Brigade', validators=[DataRequired()])
    unit =StringField('Unit', validators=[DataRequired()])
    rank = StringField('Rank', validators=[DataRequired()])
    submit = SubmitField('Save')


class DetailEditForm(FlaskForm):
    date =  DateField("Date",validators=[DataRequired()])
    session_id =IntegerField('Session No', validators=[DataRequired()])
    detail_no =IntegerField('Detail No', validators=[DataRequired()])
    paper_ref =IntegerField('Paper Reference No', validators=[DataRequired()])
    set_no =IntegerField('Set No', validators=[DataRequired()])
    target_1 =StringField('Target 1 firer', validators=[DataRequired()])
    target_1_service =StringField('Target 1 service_id', validators=[DataRequired()])
    target_2 =StringField('Target 2 firer', validators=[DataRequired()])
    target_2_service =StringField('Target 2 service_id', validators=[DataRequired()])
    target_3 =StringField('Target 3 firer', validators=[DataRequired()])
    target_3_service =StringField('Target 3 service_id', validators=[DataRequired()])
    target_4 =StringField('Target 4 firer', validators=[DataRequired()])
    target_4_service =StringField('Target 4 service_id', validators=[DataRequired()])
    target_5 =StringField('Target 5 firer', validators=[DataRequired()])
    target_5_service =StringField('Target 5 service_id', validators=[DataRequired()])
    target_6 =StringField('Target 6 firer', validators=[DataRequired()])
    target_6_service =StringField('Target 6 service_id', validators=[DataRequired()])
    target_7 =StringField('Target 7 firer', validators=[DataRequired()])
    target_7_service =StringField('Target 7 service_id', validators=[DataRequired()])
    target_8 =StringField('Target 8 firer', validators=[DataRequired()])
    target_8_service =StringField('Target 8 service_id', validators=[DataRequired()])
    submit = SubmitField('Save')
    

class SessionForm(FlaskForm):
    session_no = IntegerField('Session ID', validators=[DataRequired()])
    target_distance=IntegerField('Target Distance', default =100)
    date = DateField('Date',format="%Y-%m-%d",default=datetime.today, validators=[DataRequired()]) 
    weather_notes = TextAreaField('Weather Notes' ,validators=[DataRequired()])
    comments = TextAreaField('Comments' ,validators=[DataRequired()]) 
    submit = SubmitField('Save')



class SessionEditForm(FlaskForm):
    session_no = IntegerField('Session ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d')
    target_distance = IntegerField('Target Distance' ,validators=[DataRequired()])
    ammunation_name=TextField('Ammunation' ,validators=[DataRequired()])
    firerarms_name=TextField('Firerarms' ,validators=[DataRequired()])
    range_name=TextField('Firing Range' ,validators=[DataRequired()])
    weather_notes = TextAreaField('Weather Notes' ,validators=[DataRequired()])
    comments = TextAreaField('Comments' ,validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])




    
    
        