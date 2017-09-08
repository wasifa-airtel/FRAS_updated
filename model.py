# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import backref, relationship



db = SQLAlchemy()



class Shooter(db.Model):
    __tablename__ = 'tbld_shooters'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    service_id = db.Column(db.String)
    date_of_birth =db.Column(db.DATE)
    gender_id  =db.Column(db.Integer)
    cantonment_id = db.Column(db.Integer) 
    rank_id =db.Column(db.Integer)
    registration_date=db.Column(db.DATE)
  
    def __init__(self,name,service_id ,date_of_birth,gender_id ,cantonment_id,rank_id,registration_date):
        self.name = name
        self.service_id =service_id
        self.date_of_birth = date_of_birth
        self.gender_id =gender_id
        self.cantonment_id = cantonment_id
        self.rank_id = rank_id
        self.registration_date =registration_date
        
        
class image_record(db.Model):
    __tablename__ = 'tbl_image_record'
    
    
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    session_id = db.Column(db.Integer)
    detail_id=db.Column(db.Integer)
    target_no=db.Column(db.Integer)
    paper_ref=db.Column(db.Integer)
    firer_id = db.Column(db.Integer)
    image_name= db.Column(db.String)
    set_no=db.Column(db.Integer)
    def __init__(self,date,set_no,datetimestamp,session_id,detail_id,target_no,paper_ref,firer_id,image_name):
        self.date = date
        self.datetimestamp = datetimestamp
        self.firer_id=firer_id
        self.session_id=session_id
        self.detail_id=detail_id
        self.target_no=target_no
        self.paper_ref=paper_ref
        self.image_name=image_name
        self.target_no=target_no
        self.set_no=set_no
        
        
class TPaper_ref(db.Model):
     __tablename__ = 'temp_paper_ref'
     
     id = db.Column(db.Integer,primary_key = True)
     paper_ref=db.Column(db.Numeric)
     detail_no=db.Column(db.Numeric)
     session_no=db.Column(db.Numeric)
     
     def __init__(self,paper_ref,detail_no,session_no):
         self.paper_ref=paper_ref
         self.detail_no=detail_no
         self.session_no=session_no
     
    
class Gender(db.Model):
    __tablename__ = 'tbld_gender'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    
    def __init__(self,name):
        self.name = name
        
class MPI (db.Model):
    __tablename__ = 'tbl_mpi'
    
    id = db.Column(db.Integer,primary_key = True)
    spell_no = db.Column(db.Integer)
    date = db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    firer_id=db.Column(db.Integer)
    mpi_x=db.Column(db.Numeric)
    mpi_y=db.Column(db.Numeric)
    f_mpi_x=db.Column(db.Numeric)
    f_mpi_y=db.Column(db.Numeric)
    tendency=db.Column(db.Numeric)
    session_id = db.Column(db.Integer)
    detail_no=db.Column(db.Integer)
    target_no=db.Column(db.Integer)
    paper_ref=db.Column(db.Integer)
    tendency_f=db.Column(db.Numeric)
    tendency_text=db.Column(db.String)
    tendency_code=db.Column(db.String)
    
    def __init__(self,spell_no,date,tendency_text,tendency_code,tendency_f,session_id,detail_no,target_no,paper_ref,datetimestamp ,firer_id ,mpi_x,mpi_y,f_mpi_x,f_mpi_y,tendency):
        self.spell_no = spell_no
        self.date = date
        self.datetimestamp = datetimestamp
        self.firer_id=firer_id
        self.mpi_x=mpi_x
        self.mpi_y=mpi_y
        self.f_mpi_x=f_mpi_x
        self.f_mpi_y=f_mpi_y
        self.session_id=session_id
        self.tendency=tendency
        self.tendency_f=tendency_f
        self.detail_no=detail_no
        self.target_no=target_no
        self.paper_ref=paper_ref
        self.tendency_text=tendency_text
        self.tendency_code=tendency_code


class Grouping (db.Model):
    __tablename__ = 'tbl_grouping_length'
    
    id = db.Column(db.Integer,primary_key = True)
    spell_no = db.Column(db.Integer)
    date = db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    firer_id=db.Column(db.Integer)
    grouping_length=db.Column(db.Numeric)
    grouping_length_f=db.Column(db.Numeric)
    session_id = db.Column(db.Integer)
    detail_no= db.Column(db.Integer)
    target_no = db.Column(db.Integer)
    paper_ref=db.Column(db.Integer)
    result = db.Column(db.String)
    
    def __init__(self ,result,paper_ref,spell_no,date,datetimestamp ,firer_id ,grouping_length,grouping_length_f,session_id,detail_no,target_no):
        self.spell_no = spell_no
        self.date = date
        self.datetimestamp = datetimestamp
        self.firer_id=firer_id
        self.grouping_length=grouping_length
        self.grouping_length_f=grouping_length_f
        self.session_id=session_id
        self.target_no=target_no
        self.detail_no=detail_no
        self.paper_ref=paper_ref
        self.result=result
   
        
class Session_Detail(db.Model):
    __tablename__ = 'tbld_detail'
    
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    session_id=db.Column(db.Integer)
    detail_no=db.Column(db.Integer)
    target_1_id=db.Column(db.Integer)
    target_2_id=db.Column(db.Integer)
    target_3_id=db.Column(db.Integer)
    target_4_id=db.Column(db.Integer)
    target_5_id=db.Column(db.Integer)
    target_6_id=db.Column(db.Integer)
    target_7_id=db.Column(db.Integer)
    target_8_id=db.Column(db.Integer)
    paper_ref=db.Column(db.Numeric)
    set_no=db.Column(db.Integer)
    
    def __init__(self,date,datetimestamp,session_id,detail_no,target_1_id,target_2_id,target_3_id,target_4_id,target_5_id,target_6_id,target_7_id,target_8_id,paper_ref,set_no):
        self.date=date
        self.datetimestamp=datetimestamp
        self.detail_no=detail_no
        self.paper_ref=paper_ref
        self.session_id=session_id
        self.set_no=set_no
        self.target_1_id=target_1_id
        self.target_2_id=target_2_id
        self.target_3_id=target_3_id
        self.target_4_id=target_4_id
        self.target_5_id=target_5_id
        self.target_6_id=target_6_id
        self.target_7_id=target_7_id
        self.target_8_id=target_8_id
  
     
class TShooting(db.Model):
    __tablename__ = 'temp_detail'
    
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    session_id=db.Column(db.Integer)
    detail_no=db.Column(db.Integer)
    target_1_id=db.Column(db.Integer)
    target_2_id=db.Column(db.Integer)
    target_3_id=db.Column(db.Integer)
    target_4_id=db.Column(db.Integer)
    target_5_id=db.Column(db.Integer)
    target_6_id=db.Column(db.Integer)
    target_7_id=db.Column(db.Integer)
    target_8_id=db.Column(db.Integer)
    paper_ref=db.Column(db.Numeric)
    set_no=db.Column(db.Integer)
    
    def __init__(self,date,datetimestamp,session_id,detail_no,target_1_id,target_2_id,target_3_id,target_4_id,target_5_id,target_6_id,target_7_id,target_8_id,paper_ref,set_no):
        self.date=date
        self.datetimestamp=datetimestamp
        self.detail_no=detail_no
        self.paper_ref=paper_ref
        self.session_id=session_id
        self.set_no=set_no
        self.target_1_id=target_1_id
        self.target_2_id=target_2_id
        self.target_3_id=target_3_id
        self.target_4_id=target_4_id
        self.target_5_id=target_5_id
        self.target_6_id=target_6_id
        self.target_7_id=target_7_id
        self.target_8_id=target_8_id
        
        


class Shooting_Session(db.Model):
    __tablename__ = 'tbld_session'

    id = db.Column(db.Integer,primary_key = True)
    date =db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    shooting_range_id=db.Column(db.Integer)
    firearms_id=db.Column(db.Integer)
    ammunation_id =db.Column(db.Integer)
    target_distance=db.Column(db.Integer)
    weather_notes =db.Column(db.String)
    comments=db.Column(db.String)
    session_no = db.Column(db.Integer)
    
    def __init__(self,date,datetimestamp,shooting_range_id,firearms_id,ammunation_id,target_distance,weather_notes,comments,session_no):
        self.session_no = session_no
        self.date=date 
        self.datetimestamp=datetimestamp
        self.shooting_range_id=shooting_range_id
        self.firearms_id=firearms_id
        self.ammunation_id=ammunation_id
        self.target_distance=target_distance
        self.weather_notes=weather_notes
        self.comments=comments

class Range (db.Model):
    __tablename__ = 'tbld_shooting_range'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String) 
    
    def __init__(self,name):
        self.name = name
               
        
class Firearms (db.Model):
    __tablename__ = 'tbld_firearms'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String) 
    
    def __init__(self,name):
        self.name = name
        
class Ammunation (db.Model):
    __tablename__ = 'tbld_ammunation'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String) 
    
    def __init__(self,name):
        self.name = name


class T_Firer_Details(db.Model):
    __tablename__ = 'tbl_todays_firing_details'
    
    
    id = db.Column(db.Integer,primary_key = True)
    date =db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    session_id=db.Column(db.Integer)
    detail_id=db.Column(db.Integer)
    target_no=db.Column(db.Integer)
    set_no=db.Column(db.Integer)
    paper_ref=db.Column(db.Integer)
    firer_id=db.Column(db.Integer)
    x=db.Column( db.Numeric)
    y=db.Column( db.Numeric)
    final_x=db.Column( db.Numeric)
    final_y=db.Column( db.Numeric)

    def __init__(self,date,datetimestamp,session_id,detail_id,target_no,set_no,paper_ref,firer_id,x,y,final_x,final_y):
        self.date=date 
        self.datetimestamp=datetimestamp 
        self.session_id=session_id
        self.detail_id=detail_id
        self.target_no=target_no
        self.set_no=set_no
        self.paper_ref=paper_ref
        self.firer_id=firer_id
        self.x=x
        self.y=y
        self.final_x=final_x
        self.final_y=final_y
        
        
class Firer_Details(db.Model):
    __tablename__ = 'tbl_firing_details'
    
    
    id = db.Column(db.Integer,primary_key = True)
    date =db.Column(db.DATE)
    datetimestamp = db.Column(db.DateTime)
    session_id=db.Column(db.Integer)
    detail_id=db.Column(db.Integer)
    target_no=db.Column(db.Integer)
    set_no=db.Column(db.Integer)
    paper_ref=db.Column(db.Integer)
    firer_id=db.Column(db.Integer)
    x=db.Column( db.Numeric)
    y=db.Column( db.Numeric)
    final_x=db.Column( db.Numeric)
    final_y=db.Column( db.Numeric)

    def __init__(self,date,datetimestamp,session_id,detail_id,target_no,set_no,paper_ref,firer_id,x,y,final_x,final_y):
        self.date=date 
        self.datetimestamp=datetimestamp 
        self.session_id=session_id
        self.detail_id=detail_id
        self.target_no=target_no
        self.set_no=set_no
        self.paper_ref=paper_ref
        self.firer_id=firer_id
        self.x=x
        self.y=y
        self.final_x=final_x
        self.final_y=final_y
      
      
        

class Cantonment (db.Model):
    __tablename__ = 'tbld_cantonment'
    
    id = db.Column(db.Integer,primary_key = True)
    cantonment = db.Column(db.String)
    brigade = db.Column(db.String)
    unit = db.Column(db.String)
    
    def __init__(self,cantonment , brigade , unit):
        self.cantonment = cantonment
        self.brigade=brigade
        self.unit=unit


class Rank (db.Model):
    __tablename__ = 'tbld_rank'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    
    def __init__(self,name):
        self.name = namedb.Model