#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:16:47 2017

@author: wasifaahmed
"""

from flask import Flask, render_template, request, Response, redirect, url_for, send_from_directory,jsonify,session
import json as json
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image
from flask.ext.sqlalchemy import SQLAlchemy
import matplotlib.image as mpimg
from io import StringIO
from skimage import data, exposure, img_as_float ,io,color
import scipy
from scipy import ndimage
import time
import tensorflow as tf
import os , sys
import shutil
import numpy as np
import pandas as pd
from PIL import Image
from model import *
from sqlalchemy.sql import text
import sqlalchemy
from forms import *
import math
from io import StringIO
import csv
import datetime
from numpy import genfromtxt
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bootstrap import Bootstrap


graph = tf.Graph()
with graph.as_default():    
    sess = tf.Session(graph=graph)
    init_op = tf.global_variables_initializer()
    pointsarray=[]
    
    def load_model():
        sess.run(init_op)
        saver = tf.train.import_meta_graph('/Users/wasifaahmed/Documents/FRAS/Simulation/FRAS_20170726/FRAS_20170727.meta')
        print('The model is loading...')
        saver.restore(sess, "/Users/wasifaahmed/Documents/FRAS/Simulation/FRAS_20170726/FRAS_20170727")
        print('loaded...')
        
    engine = sqlalchemy.create_engine('postgresql://postgres:user@localhost/fras_production')
    Session = scoped_session(sessionmaker(bind=engine))
    mysession = Session()
    app = Flask(__name__)
    app.config.update(
    DEBUG=True,
    SECRET_KEY='\xa9\xc2\xc6\xfa|\x82\x1a\xfa\x1b#~\xd6ppR=\x1e4\xfb`-\xc0\xad\xc9')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost/fras_production'
    db.init_app(app)
    Bootstrap(app)

    
    @app.route('/',methods=['GET', 'POST']) 
    def login():
        form = LoginForm()
        return render_template('forms/login.html', form=form)
    
    
    @app.route('/home',methods=['GET', 'POST']) 
    def index():
        return render_template('pages/home.html')
    
    
    
    @app.route('/detail_setup/') 
    def Detail_Setup():
        curdate=time.strftime("%Y-%m-%d")
        selection=Shooting_Session.query.filter(Shooting_Session.date==curdate).all()
        firer_1 = [row.service_id for row in Shooter.query.all()]
        return render_template('pages/detail_setup.html',
                               data=selection,
                               firer_1=firer_1)
        
        
    
    @app.route('/generate_ref/' ,methods=['GET', 'POST'])
    def generate_ref():
        if request.method == "POST":
            data = request.get_json()
            paper_ref =data['data']
            if (paper_ref == 'New'):
                g="Null"               
            else:
                g= mysession.query(TPaper_ref.paper_ref).scalar() 
        return jsonify(gen=g)
        
           
    @app.route('/FRAS/', methods=['GET', 'POST'])
    def load ():
        ref_1=None
        if request.method == 'POST':
            detail_no = request.form['game_id_1'] 
            r=request.form['tag'] 
            r_id=mysession.query(Shooter.id).filter(Shooter.service_id==r).scalar()
            r1=request.form['tag_1']
            r1_id=mysession.query(Shooter.id).filter(Shooter.service_id==r1).scalar()
            r2=request.form['tag_2'] 
            r2_id=mysession.query(Shooter.id).filter(Shooter.service_id==r2).scalar()
            r3=request.form['tag_3'] 
            r3_id=mysession.query(Shooter.id).filter(Shooter.service_id==r3).scalar()
            r4=request.form['tag_4']
            r4_id=mysession.query(Shooter.id).filter(Shooter.service_id==r4).scalar()
            r5=request.form['tag_5']
            r5_id=mysession.query(Shooter.id).filter(Shooter.service_id==r5).scalar()
            r6=request.form['tag_6']
            r6_id=mysession.query(Shooter.id).filter(Shooter.service_id==r6).scalar()
            r7=request.form['tag_7']
            r7_id=mysession.query(Shooter.id).filter(Shooter.service_id==r7).scalar()
            ref=request.form['business']
            
            print('This is ref',file=sys.stderr)
            print(ref,file=sys.stderr)
            print(type(ref),file=sys.stderr)
            
            set_no = request.form.get('comp_select_6')
            shots = request.form['tag_8']
            sess=request.form.get('comp_select')
            if ref == None or ref =="":
                ref_1=mysession.query(TPaper_ref.paper_ref).scalar()
                
            
            else :
                ref_1=ref
                check=mysession.query(TPaper_ref.paper_ref).scalar()
                cses=mysession.query(TPaper_ref.session_no).scalar()
                det=mysession.query(TPaper_ref.detail_no).scalar()
                
                if(set_no>5):
                    return redirect(url_for('paper_duplicate_error'))
                else:
                    db.session.query(TPaper_ref).delete()
                    db.session.commit()
                    
                    ref_db = TPaper_ref(
                            paper_ref=ref_1,
                            detail_no=detail_no,
                            session_no=sess
                            )
                    db.session.add(ref_db)
                    db.session.commit()
       
            tmp_list = []
            tmp_list.append(r_id)
            tmp_list.append(r1_id)
            tmp_list.append(r2_id)
            tmp_list.append(r3_id)
            tmp_list.append(r4_id)
            tmp_list.append(r5_id)
            tmp_list.append(r6_id)
            tmp_list.append(r7_id)
            
            duplicate = False
            for i in range(len(tmp_list)):
                for j in range(len(tmp_list)):
                    if(i!=j and tmp_list[i]==tmp_list[j]):
                        duplicate = True
            
            if(duplicate):
                return redirect(url_for('duplicate_firer_error'))
            else:
                
                detail_shots =Session_Detail(
                        date=datetime.datetime.now(),
                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                        session_id=sess,
                        detail_no=detail_no,
                        target_1_id=r_id,
                        target_2_id=r1_id,
                        target_3_id=r2_id,
                        target_4_id=r3_id,
                        target_5_id=r4_id,
                        target_6_id=r5_id,
                        target_7_id=r6_id,
                        target_8_id=r7_id,
                        paper_ref=ref_1,
                        set_no=set_no
                        )
                db.session.add(detail_shots)
                db.session.commit()
                
                db.session.query(TShooting).delete()
                db.session.commit()
                
                Tdetail_shots =TShooting(
                        date=datetime.datetime.now(),
                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                        session_id=sess,
                        detail_no=detail_no,
                        target_1_id=r_id,
                        target_2_id=r1_id,
                        target_3_id=r2_id,
                        target_4_id=r3_id,
                        target_5_id=r4_id,
                        target_6_id=r5_id,
                        target_7_id=r6_id,
                        target_8_id=r7_id,
                        paper_ref=ref_1,
                        set_no=set_no
                        )
                db.session.add(Tdetail_shots)
                db.session.commit()
        return redirect(url_for('index'))
    
    @app.route('/detail_view/', methods=['GET', 'POST'])
    def detail_view():
        detail = Session_Detail.query.all()
        for details in detail:
            details.target_1=mysession.query(Shooter.name).filter(Shooter.id==details.target_1_id).first().name
            details.target_2=mysession.query(Shooter.name).filter(Shooter.id==details.target_2_id).first().name
            details.target_3=mysession.query(Shooter.name).filter(Shooter.id==details.target_3_id).first().name
            details.target_4=mysession.query(Shooter.name).filter(Shooter.id==details.target_4_id).first().name
            details.target_5=mysession.query(Shooter.name).filter(Shooter.id==details.target_5_id).first().name
            details.target_6=mysession.query(Shooter.name).filter(Shooter.id==details.target_6_id).first().name
            details.target_7=mysession.query(Shooter.name).filter(Shooter.id==details.target_7_id).first().name
            details.target_8=mysession.query(Shooter.name).filter(Shooter.id==details.target_8_id).first().name
        return render_template('pages/detail_view.html',detail=detail)
    
    @app.route('/detail_view/detail/<id>', methods=['GET', 'POST'])
    def view_detail(id):
        detail=Session_Detail.query.filter(Session_Detail.id == id)
        for details in detail:
            details.target_1=mysession.query(Shooter.name).filter(Shooter.id==details.target_1_id).first().name
            details.target_2=mysession.query(Shooter.name).filter(Shooter.id==details.target_2_id).first().name
            details.target_3=mysession.query(Shooter.name).filter(Shooter.id==details.target_3_id).first().name
            details.target_4=mysession.query(Shooter.name).filter(Shooter.id==details.target_4_id).first().name
            details.target_5=mysession.query(Shooter.name).filter(Shooter.id==details.target_5_id).first().name
            details.target_6=mysession.query(Shooter.name).filter(Shooter.id==details.target_6_id).first().name
            details.target_7=mysession.query(Shooter.name).filter(Shooter.id==details.target_7_id).first().name
            details.target_8=mysession.query(Shooter.name).filter(Shooter.id==details.target_8_id).first().name
        return render_template('pages/detail_view_id.html',data=detail)
    
    @app.route('/detail_view/edit/<id>', methods=['GET', 'POST'])
    def view_detail_edit(id):
        detail=Session_Detail.query.filter(Session_Detail.id == id).first()
        form=DetailEditForm(obj=detail)
        if form.validate_on_submit():
            tmp_list = []
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_1.data ,Shooter.service_id == form.target_1_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_2.data ,Shooter.service_id == form.target_2_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_3.data ,Shooter.service_id == form.target_3_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_4.data ,Shooter.service_id == form.target_4_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_5.data ,Shooter.service_id == form.target_5_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_6.data ,Shooter.service_id == form.target_6_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_7.data ,Shooter.service_id == form.target_7_service.data).scalar())
            tmp_list.append(mysession.query(Shooter.id).filter(Shooter.name==form.target_8.data ,Shooter.service_id == form.target_8_service.data).scalar())

            duplicate = False
            for i in range(len(tmp_list)):
                for j in range(len(tmp_list)):
                    if(i!=j and tmp_list[i]==tmp_list[j]):
                        duplicate = True
            
            if(duplicate):
                return redirect(url_for('duplicate_firer_error'))
            else:
                detail.date=form.date.data
                detail.session_id=form.session_id.data
                detail.detail_no=form.detail_no.data
                detail.paper_ref=form.paper_ref.data
                detail.set_no=form.set_no.data
                detail.target_1_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_1.data ,Shooter.service_id == form.target_1_service.data).scalar()
                detail.target_2_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_2.data ,Shooter.service_id == form.target_2_service.data).scalar()
                print(detail.target_2_id,file=sys.stderr)
                detail.target_3_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_3.data ,Shooter.service_id == form.target_3_service.data).scalar()
                detail.target_4_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_4.data ,Shooter.service_id == form.target_4_service.data).scalar()
                detail.target_5_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_5.data ,Shooter.service_id == form.target_5_service.data).scalar()
                detail.target_6_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_6.data ,Shooter.service_id == form.target_6_service.data).scalar()
                detail.target_7_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_7.data ,Shooter.service_id == form.target_7_service.data).scalar()
                detail.target_8_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_8.data ,Shooter.service_id == form.target_8_service.data).scalar()
                db.session.commit()
                
                db.session.query(TPaper_ref).delete()
                db.session.commit()
                ref_edit = TPaper_ref(
                                paper_ref=form.paper_ref.data,
                                detail_no=form.detail_no.data,
                                session_no=form.session_id.data
                                )
                db.session.add(ref_edit)
                db.session.commit()
                
                db.session.query(TShooting).delete()
                db.session.commit()
                    
                Tdetail_edit =TShooting(
                            date=form.date.data,
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=form.session_id.data,
                            detail_no=form.detail_no.data,
                            target_1_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_1.data ,Shooter.service_id == form.target_1_service.data).scalar(),
                            target_2_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_2.data ,Shooter.service_id == form.target_2_service.data).scalar(),
                            target_3_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_3.data ,Shooter.service_id == form.target_3_service.data).scalar(),
                            target_4_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_4.data ,Shooter.service_id == form.target_4_service.data).scalar(),
                            target_5_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_5.data ,Shooter.service_id == form.target_5_service.data).scalar(),
                            target_6_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_6.data ,Shooter.service_id == form.target_6_service.data).scalar(),
                            target_7_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_7.data ,Shooter.service_id == form.target_7_service.data).scalar(),
                            target_8_id=mysession.query(Shooter.id).filter(Shooter.name==form.target_8.data ,Shooter.service_id == form.target_8_service.data).scalar(),
                            paper_ref=form.paper_ref.data,
                            set_no=form.set_no.data
                            )
                db.session.add(Tdetail_edit)
                db.session.commit()
                return redirect(url_for('detail_view'))
        
        form.date.data=detail.date
        form.session_id.data=detail.session_id
        form.detail_no.data=detail.detail_no
        form.paper_ref.data=detail.paper_ref
        form.set_no.data=detail.set_no
        form.target_1.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_1_id).scalar()
        form.target_2.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_2_id).scalar()
        form.target_3.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_3_id).scalar()
        form.target_4.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_4_id).scalar()
        form.target_5.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_5_id).scalar()
        form.target_6.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_6_id).scalar()
        form.target_7.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_7_id).scalar()
        form.target_8.data=mysession.query(Shooter.name).filter(Shooter.id==detail.target_8_id).scalar()
        form.target_1_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_1_id).scalar()
        form.target_2_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_2_id).scalar()
        form.target_3_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_3_id).scalar()
        form.target_4_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_4_id).scalar()
        form.target_5_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_5_id).scalar()
        form.target_6_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_6_id).scalar()
        form.target_7_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_7_id).scalar()
        form.target_8_service.data = mysession.query(Shooter.service_id).filter(Shooter.id==detail.target_8_id).scalar()
        return render_template('pages/detail_view_edit.html' , detail=detail,form=form)
    
    @app.route('/shooter_registration/', methods=['GET', 'POST']) 
    def registration():
        cantonment=mysession.query(Cantonment).distinct(Cantonment.cantonment)
        gender =Gender.query.all()
        rank = Rank.query.all()
        ran = request.form.get('comp_select4') 
        cant = request.form.get('comp_select')
        gen = request.form.get('comp_select5')
        brig = request.form.get('comp_select1')
        uni = request.form.get('comp_select2')
        
        rank_id =  mysession.query(Rank.id).filter(Rank.name==ran).scalar()
        cant_id = mysession.query(Cantonment.id).filter(Cantonment.cantonment==cant,
                                                         Cantonment.brigade==brig,
                                                         Cantonment.unit==uni
                                                  ).scalar()
        gender_id = mysession.query(Gender.id).filter(Gender.name==gen).scalar()
        
        
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            shooter = Shooter(
                         name=form.name.data,
                         service_id = form.service_id.data,
                         date_of_birth =form.dob.data.strftime('%Y-%m-%d'),
                         registration_date = form.dt.data.strftime('%Y-%m-%d'),
                         gender_id=gender_id,
                         cantonment_id = cant_id,
                         rank_id =rank_id
                         )
            db.session.add(shooter)
            db.session.commit()
            new_form = RegistrationForm(request.form)
            
            return redirect(url_for('firer_details'))

        return render_template('forms/registration.html',
                               cantonment =  cantonment ,
                               form=form ,
                               rank = rank,
                               gender=gender)
    
    @app.route('/get_brigade/')
    def get_brigade():
        cant = request.args.get('customer')
        da = mysession.query(Cantonment.brigade).filter(Cantonment.cantonment==cant).distinct()
        data = [{"name": x.brigade} for x in da]
        return jsonify(data)
    
    @app.route('/get_unit/')
    def get_unit():
        brigade = request.args.get('customer')
        #print("the name brigade" + brigade, file=sys.stderr)
        da = mysession.query(Cantonment.unit).filter(Cantonment.brigade==brigade).distinct()
        data = [{"name": x.unit} for x in da]
        return jsonify(data)
    
    @app.route('/firer_details/', methods=['GET', 'POST'])
    def firer_details():
        firer = Shooter.query.all()
        for firers in firer:
            firers.cantonment_name = mysession.query(Cantonment.cantonment).filter(Cantonment.id==firers.cantonment_id).first().cantonment
            firers.brigade = mysession.query(Cantonment.brigade).filter(Cantonment.id==firers.cantonment_id).first().brigade
            firers.unit = mysession.query(Cantonment.unit).filter(Cantonment.id==firers.cantonment_id).first().unit
            firers.rank = mysession.query(Rank.name).filter(Rank.id==firers.rank_id).first().name
            firers.gender = mysession.query(Gender.name).filter(Gender.id==firers.gender_id).first().name
        return render_template('pages/firer_details.html' , firer = firer)
    
    @app.route('/bulk_registration')
    def bulk_registration():
        cantonment=mysession.query(Cantonment).distinct(Cantonment.cantonment)
        form=RegistrationForm(request.form)
        return render_template('pages/bulk_registration.html',cantonment=cantonment,form=form)
    

    @app.route('/upload', methods=['POST'])
    def upload():
        f = request.files['data_file']
        cant = request.form.get('comp_select')
        brig = request.form.get('comp_select1')
        uni = request.form.get('comp_select2') 
        form=RegistrationForm(request.form) 
        cant_id = mysession.query(Cantonment.id).filter(Cantonment.cantonment==cant,
                                                         Cantonment.brigade==brig,
                                                         Cantonment.unit==uni
                                                 ).scalar()
        if form.is_submitted():
            stream = StringIO(f.stream.read().decode("UTF8"))
            csv_input = csv.reader(stream)  
            lis =list(csv_input)
            
            
            for i in range(len(lis)):
                shooters = Shooter(
                        name  = lis[i][0],
                        service_id=lis[i][4],
                        registration_date=datetime.datetime.now(),
                        date_of_birth=lis[i][1],
                        gender_id=mysession.query(Gender.id).filter(Gender.name==lis[i][3]).scalar(),
                        cantonment_id = cant_id,
                        rank_id = mysession.query(Rank.id).filter(Rank.name==lis[i][2]).scalar()
                        
                        )
                db.session.add(shooters)
                db.session.commit()    
        return redirect(url_for('bulk_registration'))         
        
    
    
    @app.route('/firer_details/detail/<id>', methods=['GET', 'POST'])
    def firer_detail_view(id):
        firer = Shooter.query.filter(Shooter.service_id == id)
        for firers in firer:
            firers.cantonment_name = mysession.query(Cantonment.cantonment).filter(Cantonment.id==firers.cantonment_id).first().cantonment
            firers.brigade = mysession.query(Cantonment.brigade).filter(Cantonment.id==firers.cantonment_id).first().brigade
            firers.unit = mysession.query(Cantonment.unit).filter(Cantonment.id==firers.cantonment_id).first().unit
            firers.rank = mysession.query(Rank.name).filter(Rank.id==firers.rank_id).first().name
            firers.gender = mysession.query(Gender.name).filter(Gender.id==firers.gender_id).first().name
        return render_template('pages/firer_detail_view.html' , data = firer)
     
    @app.route('/firer_details/edit/<id>', methods=['GET', 'POST'])  
    def firer_detail_edit(id):
         firer = Shooter.query.filter(Shooter.service_id == id).first()
         form=RegistrationEditForm(obj=firer)
         
         if form.validate_on_submit():
             firer.name = form.name.data
             firer.service_id=form.service_id.data
             firer.date_of_birth=form.dob.data
             firer.registration_date=form.date.data
             firer.gender_id=mysession.query(Gender.id).filter(Gender.name==form.gender.data).scalar()
             firer.cantonment_id=mysession.query(Cantonment.id).filter(Cantonment.cantonment==form.cantonment.data,
                                                                       Cantonment.brigade==form.brigade.data,
                                                                       Cantonment.unit==form.unit.data,
                                                                         ).scalar()
             firer.rank_id=mysession.query(Rank.id).filter(Rank.name==form.rank.data).scalar()
             db.session.commit()
             return redirect(url_for('firer_details'))
         
         form.name.data=firer.name
         form.service_id.data=firer.service_id
         form.dob.data=firer.date_of_birth
         form.date.data=firer.registration_date
         form.gender.data=mysession.query(Gender.name).filter(Gender.id==firer.gender_id).scalar()
         form.cantonment.data=mysession.query(Cantonment.cantonment).filter(Cantonment.id==firer.cantonment_id).scalar()
         form.brigade.data=mysession.query(Cantonment.brigade).filter(Cantonment.id==firer.cantonment_id).scalar()
         form.unit.data=mysession.query(Cantonment.unit).filter(Cantonment.id==firer.cantonment_id).scalar()
         form.rank.data=mysession.query(Rank.name).filter(Rank.id==firer.rank_id).scalar()
         return render_template('pages/firer_detail_edit.html' , firer = firer , form=form)
     
    @app.route('/live/')
    def live():
        return render_template('pages/live.html' )
    
    @app.route('/session_setup/', methods=['GET', 'POST'])
    def session_setup():
        data = Shooter.query.all()
        rang= Range.query.all()
        firearms = Firearms.query.all()
        ammunation = Ammunation.query.all()
        rang_name = request.form.get('comp_select_4')
        fire_name = request.form.get('comp_select_5')
        ammu_name = request.form.get('comp_select_6')
        
        range_id = mysession.query(Range.id).filter(Range.name==rang_name).scalar()
        fire_id = mysession.query(Firearms.id).filter(Firearms.name==fire_name).scalar()
        ammu_id = mysession.query(Ammunation.id).filter(Ammunation.name==ammu_name).scalar()

        form=SessionForm()
        if form.validate_on_submit():
            shooting=Shooting_Session(
                            date=form.date.data.strftime('%Y-%m-%d'),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            shooting_range_id=range_id,
                            firearms_id=fire_id,
                            ammunation_id=ammu_id,
                            target_distance = form.target_distance.data,
                            weather_notes = form.weather_notes.data,
                            comments = form.comments.data,
                            session_no=form.session_no.data
                              )
            
            db.session.add(shooting)
            db.session.commit()
            return redirect(url_for('session_config'))
        return render_template('forms/shooting_form.html', form=form, data =data ,rang=rang , firearmns=firearms, ammunation = ammunation)
    
    @app.route('/configuration/', methods=['GET', 'POST'])
    def session_config():
        config = Shooting_Session.query.all()
        for con in config:
            con.range_name = mysession.query(Range.name).filter(Range.id==con.shooting_range_id).first().name
            con.firerarms_name = mysession.query(Firearms.name).filter(Firearms.id==con.firearms_id).first().name
            con.ammunation_name = mysession.query(Ammunation.name).filter(Ammunation.id==con.ammunation_id).first().name
        return render_template('pages/shooting_configuration_detail.html',con=config)
    
    @app.route('/configuration/detail/<id>', methods=['GET', 'POST'])
    def session_config_detail(id):
        config = Shooting_Session.query.filter(Shooting_Session.session_no == id)
        for con in config:
            con.range_name = mysession.query(Range.name).filter(Range.id==con.shooting_range_id).first().name
            con.firerarms_name = mysession.query(Firearms.name).filter(Firearms.id==con.firearms_id).first().name
            con.ammunation_name = mysession.query(Ammunation.name).filter(Ammunation.id==con.ammunation_id).first().name
        return render_template('pages/shooting_configuration_detail_view.html',con=config)
    
    @app.route('/configuration/edit/<id>', methods=['GET', 'POST'])
    def shooting_config_edit(id):
        edit = Shooting_Session.query.get_or_404(id)
        form = SessionEditForm(obj=edit)
        if form.validate_on_submit():
            edit.session_no = form.session_no.data
            edit.date = form.date.data
            edit.target_distance = form.target_distance.data
            edit.ammunation_id=mysession.query(Ammunation.id).filter(Ammunation.name==form.ammunation_name.data).scalar()
            edit.firearms_id=mysession.query(Firearms.id).filter(Firearms.name==form.firerarms_name.data).scalar()
            edit.shooting_range_id=mysession.query(Range.id).filter(Range.name==form.range_name.data).scalar()
            edit.weather_notes=form.weather_notes.data
            edit.comments=form.comments.data
            db.session.commit()
            return redirect(url_for('session_config'))
        
        form.session_no.data=edit.session_no
        form.date.data=edit.date
        form.ammunation_name.data=mysession.query(Ammunation.name).filter(Ammunation.id==edit.ammunation_id).scalar()
        form.firerarms_name.data=mysession.query(Firearms.name).filter(Firearms.id==edit.firearms_id).scalar()
        form.range_name.data=mysession.query(Range.name).filter(Range.id==edit.shooting_range_id).scalar()
        form.weather_notes.data=edit.weather_notes
        form.comments.data=edit.comments
        return render_template('pages/shooting_configuration_edit.html',form=form,edit=edit)
    
    @app.route('/detail_dashboard/')
    def detail_dashboard():
        T1_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_rank = mysession.query(Rank.name).filter(Rank.id==T1_r_id).scalar()
        
        T2_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_rank = mysession.query(Rank.name).filter(Rank.id==T2_r_id).scalar()
        
        
        
        T3_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_rank = mysession.query(Rank.name).filter(Rank.id==T3_r_id).scalar()
        
        T4_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_rank = mysession.query(Rank.name).filter(Rank.id==T4_r_id).scalar()
        
        T5_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_rank = mysession.query(Rank.name).filter(Rank.id==T5_r_id).scalar()
        
        T6_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_rank = mysession.query(Rank.name).filter(Rank.id==T6_r_id).scalar()
        
        T7_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_rank = mysession.query(Rank.name).filter(Rank.id==T7_r_id).scalar()
        
        T8_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_rank = mysession.query(Rank.name).filter(Rank.id==T8_r_id).scalar()
        
        return render_template('pages/detail_dashboard.html' ,
                               T1_name=T1_name,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service,
                               T5_name=T5_name,
                               T5_service=T5_service,
                               T6_name=T6_name,
                               T6_service=T6_service,
                               T7_name=T7_name,
                               T7_service=T7_service,
                               T8_name=T8_name,
                               T8_service=T8_service,
                               T1_rank=T1_rank,
                               T2_rank=T2_rank,
                               T3_rank=T3_rank,
                               T4_rank=T4_rank,
                               T5_rank=T5_rank,
                               T6_rank=T6_rank,
                               T7_rank=T7_rank,
                               T8_rank=T8_rank
                               
                               )
    
    @app.route('/individual_score/target_1', methods=['GET', 'POST'])
    def individual_score_target_1():
        firer_id =mysession.query(TShooting.target_1_id).scalar()
        detail_no =mysession.query(TShooting.detail_no).scalar()
        session_no =mysession.query(TShooting.session_id).scalar()
        target_no = 1
        service_id = mysession.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=mysession.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=mysession.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = mysession.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_1.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank)
    
    @app.route('/prediction_target_1/', methods=['GET', 'POST'])
    def prediction_target_1():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,l,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_1()
            set_2_x=mysession.query(T_Firer_Details.final_x).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==2).all()
            set_2_y=mysession.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==2).all()
            set_3_x=mysession.query(T_Firer_Details.final_x).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==3).all()
            set_3_y=mysession.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==3).all()
            
            set_4_x=mysession.query(T_Firer_Details.final_x).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==4).all()
            set_4_y=mysession.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==4).all()
            
            set_1_id = mysession.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==1).distinct().scalar()
            
            set_1_session_no=mysession.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==1).distinct().scalar()
            
            set_1_detail_no=mysession.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==1).distinct().scalar()
            
            set_1_name=mysession.query(Shooter.name).filter(Shooter.id==set_1_id).scalar()
            set_1_army=mysession.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            set_2_id = mysession.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==2).distinct().scalar()
            
            set_2_session_no=mysession.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==2).distinct().scalar()
            
            set_2_detail_no=mysession.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==2).distinct().scalar()
            
            set_2_name=mysession.query(Shooter.name).filter(Shooter.id==set_2_id).scalar()
            set_2_army=mysession.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            set_3_id = mysession.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==3).distinct().scalar()
            
            set_3_session_no=mysession.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==3).distinct().scalar()
            
            set_3_detail_no=mysession.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==3).distinct().scalar()
            
            set_3_name=mysession.query(Shooter.name).filter(Shooter.id==set_3_id).scalar()
            set_3_army=mysession.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            set_4_id = mysession.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==4).distinct().scalar()
            
            set_4_session_no=mysession.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==4).distinct().scalar()
            
            set_4_detail_no=mysession.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==1, 
                                      T_Firer_Details.set_no==4).distinct().scalar()
            
            set_4_name=mysession.query(Shooter.name).filter(Shooter.id==set_4_id).scalar()
            set_4_army=mysession.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = mysession.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = mysession.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=mysession.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=mysession.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            print(set_1_name,file=sys.stderr)
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=xmpi_j ,
                       ympi1=ympi_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_1,
                       fy1=fin_y_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x,
                       set_2_y=set_2_y,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x,
                       set_3_y=set_3_y,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x,
                       set_4_y=set_4_y,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
    
    @app.route('/previous_page_target_1/', methods=['GET', 'POST'])
    def previous_page_target_1():
        T1_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_rank = mysession.query(Rank.name).filter(Rank.id==T1_r_id).scalar()
        
        T2_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_rank = mysession.query(Rank.name).filter(Rank.id==T2_r_id).scalar()
        
        
        
        T3_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_rank = mysession.query(Rank.name).filter(Rank.id==T3_r_id).scalar()
        
        T4_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_rank = mysession.query(Rank.name).filter(Rank.id==T4_r_id).scalar()
        
        
        return render_template('pages/previous_page_target_1.html' ,
                               T1_name=T1_name,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service
                               
                               )
    
    
    def prediction_calculation_1():
        curdate=time.strftime("%Y-%m-%d")
        firer_id =mysession.query(TShooting.target_1_id).scalar()
        sess_id = mysession.query(TShooting.session_id).scalar()
        detail_id = mysession.query(TShooting.detail_no).scalar()
        target_no=1
        data_x_1=mysession.query(T_Firer_Details.final_x).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==1).all()
        data_y_1=mysession.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==1 , T_Firer_Details.set_no==1).all()
        set_no=mysession.query(TShooting.set_no).scalar()
        paper_ref=mysession.query(TShooting.paper_ref).scalar()
        image=Image.open('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/1.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        x= centroids [:, 1]
        y= 2000-centroids [:, 0]
        X_json=pd.Series(x).to_json(orient='values')
        Y_json = pd.Series(y).to_json(orient='values')
        mpit=mpi(1,centroids)
        xmpi1 = mpit [:, 1]
        ympi1 = 2000-mpit [:, 0]
        #fir_tendency ="Bottom"
        f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
        fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
        #gp_1 = grouping_length(xmpi1 , ympi1 , x , y)
        print("calling from prediction_calculation_1" ,file=sys.stderr)
        gp_1 = grouping_length(0 , 0 , x , y)
        result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
        
    
    @app.route('/save_1/', methods=['GET', 'POST'])
    def save_call_1():
        final_x=[]
        final_y=[]
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_1()           
            t1= session.get('tmpi',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x  = session.get('x1', None)
            final_y  = session.get('y1', None)
            gp_1_f=session.get('gp_u_1', None)
            res_u_1=session.get('res_u_1',None)
            tend_f = session.get('tf_u_1', None)
            tend_f_x = session.get('tfirer_x1', None)
            tend_f_y = session.get('tfirer_y1', None)
            
            x_len=len(x)
            y_len=len(y)
            x_ss=x[1:x_len-1]
            y_ss=y[1:y_len-1]
            x_split = x_ss.split(",")
            y_split = y_ss.split(",")
            x_list=[]
            y_list=[]
            for x_t in x_split:
                x_list.append(float(x_t))
                
            for y_t in y_split:
                y_list.append(float(y_t))
                
            #print('This is Split',file=sys.stderr)
            #print(x_split,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x,final_y)
            mpi=savempi_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,tendency,f_mpix_1,f_mpiy_1,tend_f,mx1,my1 ,firt_x,firt_y,tend_f_x,tend_f_y)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,result)
            image_save=save_image_1(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('detail_dashboard'))
    
    
    
    def savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,final_x,final_y):
          print("This is final_x",file=sys.stderr)
          print(final_x,file=sys.stderr)
          print("--------------",file=sys.stderr)
          if(final_x == " "):
              i = 0 
              while i <len(x):
                  detail=T_Firer_Details(
                         date=time.strftime("%x"),
                         datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                         session_id=session_id,
                         detail_id=detail_no,
                         target_no=target_no,
                         set_no=set_no,
                         paper_ref=paper_no,
                         firer_id=firer_id,
                         x=x[i],
                         y=y[i],
                         final_x=x[i],
                         final_y=y[i]
                    )
                  db.session.add(detail)
                  db.session.commit()
                  i=i+1
          else:
              if(len(final_x)<len(x)):
                  f_x_f=[]
                  f_y_f=[]
                  f_x_f ,f_y_f = making_array_del(final_x, final_y , len(x))
                  z = 0 
                  while z <len(x):
                      detail1=T_Firer_Details(
                            date=time.strftime("%x"),
                            datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                            session_id=session_id,
                            detail_id=detail_no,
                            target_no=target_no,
                            set_no=set_no,
                            paper_ref=paper_no,
                            firer_id=firer_id,
                            x=x[z],
                            y=y[z],
                            final_x=f_x_f[z],
                            final_y=f_y_f[z]
                         ) 
                      db.session.add(detail1)
                      db.session.commit()
                      z=z+1
                      
              elif(len(x)<len(final_x)):
                  firer_x=[]
                  firer_y=[]
                  firer_x,firer_y =making_array_add(x,y ,len(final_x))
                  z=0
                  f_x_f1=[]
                  f_y_f1=[]
                  for h in range(len(final_x)):
                      f_x_f1.append(final_x[h][0])
                      f_y_f1.append(final_y[h][0])
                      
                  while z <len(f_y_f1):
                      detail2=T_Firer_Details(
                            date=time.strftime("%x"),
                            datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                            session_id=session_id,
                            detail_id=detail_no,
                            target_no=target_no,
                            set_no=set_no,
                            paper_ref=paper_no,
                            firer_id=firer_id,
                            x=firer_x[z],
                            y=firer_y[z],
                            final_x=f_x_f1[z],
                            final_y=f_y_f1[z]
                         ) 
                      db.session.add(detail2)
                      db.session.commit()
                      z=z+1       
              else:
                  z=0
                  f_x_f1=[]
                  f_y_f1=[]
                  for h in range(len(final_x)):
                      f_x_f1.append(final_x[h][0])
                      f_y_f1.append(final_y[h][0])
                      
                  print(type(f_x_f1),f_x_f1[0],file=sys.stderr)
                  while z <len(x):
                          detail3=T_Firer_Details(
                            date=time.strftime("%x"),
                            datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                            session_id=session_id,
                            detail_id=detail_no,
                            target_no=target_no,
                            set_no=set_no,
                            paper_ref=paper_no,
                            firer_id=firer_id,
                            x=x[z],
                            y=y[z],
                            final_x=int(f_x_f1[z]),
                            final_y=int(f_y_f1[z])
                           ) 
                          db.session.add(detail3)
                          db.session.commit()
                          z=z+1


          return True

    
    def save_image_1(firer_id):
        srcfile = '/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/1.png'
        dstdir = '/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/image_db/'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/image_db/", "1.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/image_db/", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    
    def savempi_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,tendency,fmpix,fmpiy,tend_f,mpix,mpiy,firt_x,firt_y,tend_f_x,tend_f_y):
        if(fmpix is None):
            u_fir_txt,u_fir_code=getfiringtendencytext(tendency,firt_x,firt_y)
            mpi= MPI (
                  date=time.strftime("%x"),  
                  datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                  session_id=session_id,
                  detail_no=detail_no,
                  target_no=target_no,
                  spell_no=set_no,
                  paper_ref=paper_no,
                  firer_id=firer_id,
                  mpi_x=int(mpix[0]),
                  mpi_y=int(mpiy[0]),
                  f_mpi_x=int(mpix[0]),
                  f_mpi_y=int(mpiy[0]),
                  tendency=int(tendency),
                  tendency_f=int(tendency),
                  tendency_text=u_fir_txt,
                  tendency_code=u_fir_code
                  
                 )
            db.session.add(mpi)
            db.session.commit()
             
        else:
            print(fmpix,file=sys.stderr)
            print(fmpiy,file=sys.stderr)
            u_fir_txt,u_fir_code=getfiringtendencytext(tend_f,tend_f_x,tend_f_y)
            mpi= MPI (
                  date=time.strftime("%x"),  
                  datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                  session_id=session_id,
                  detail_no=detail_no,
                  target_no=target_no,
                  spell_no=set_no,
                  paper_ref=paper_no,
                  firer_id=firer_id,
                  mpi_x=int(mpix[0]),
                  mpi_y=int(mpiy[0]),
                  f_mpi_x=int(fmpix[0][0]),
                  f_mpi_y=int(fmpix[0][1]),
                  tendency=tendency,
                  tendency_f=int(tend_f),
                  tendency_text=u_fir_txt,
                  tendency_code=u_fir_code
                 )
            db.session.add(mpi)
            db.session.commit()
             
        return True
    
    
    
    def savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,gp_l,gp_f,result):
        if(gp_f is None):
            gp=Grouping(
                  date=time.strftime("%x"),  
                  datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                  session_id=session_id,
                  detail_no=detail_no,
                  target_no=target_no,
                  spell_no=set_no,
                  paper_ref=paper_no,
                  firer_id=firer_id,
                  grouping_length=gp_l,
                  grouping_length_f=gp_l,
                  result = result
                  )
            
            db.session.add(gp)
            db.session.commit()
            
        else:
            gp=Grouping(
                  date=time.strftime("%x"),  
                  datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                  session_id=session_id,
                  detail_no=detail_no,
                  target_no=target_no,
                  spell_no=set_no,
                  paper_ref=paper_no,
                  firer_id=firer_id,
                  grouping_length=gp_l,
                  grouping_length_f=gp_f,
                  result = result
                  )
            
            db.session.add(gp)
            db.session.commit()
        return True
    
    
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.route('/duplicate_firer_error/')
    def duplicate_firer_error():
        return render_template('errors/duplicate.html')
    
    @app.route('/paper_duplicate/')
    def paper_duplicate_error():
        return render_template('errors/paper_dup.html')
    
   
        
    
    
    def making_array_del(x , y , l):
        x_f=[]
        y_f=[]
        for i in range(len(x)):
            x_f.append(x[i][0])
            y_f.append(y[i][0])
            
        for j in range(l-len(x)):
            x_f.append(-1)
            y_f.append(-1)
        return x_f , y_f
    
    def making_array_add(x , y , l):
        x_1=[]
        y_1=[]
        for i in range(len(x)):
            x_1.append(x[i])
            y_1.append(y[i])
            
            
        for j in range(l-len(x)):
            x_1.append(-1)
            y_1.append(-1)
        
        return x_1 , y_1
        
        
        

        
    def firing_tendancy(origin_x, origin_y , x, y):
        
        x1 = origin_x-x
        y1 = origin_y-y
        xfirt=None
        yfirt=None
        deg = 0 
        h = math.sqrt(x1**2 + y1**2)
        x_dis = x-origin_x
        y_dis = y-origin_y
        theta = math.degrees(y_dis/h)
        if( x_dis > 0 and y_dis < 0 ):
            deg = 360 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
            
            
        elif (x_dis < 0 and y_dis < 0 ):
            deg = 270 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
            
        elif(x_dis < 0 and y_dis > 0 ):
            deg = 180 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
        else :
           deg = theta
           xfirt=pixeltoinch(x_dis)
           yfirt=pixeltoinch(y_dis)
        return (np.round(deg,0) ,xfirt ,yfirt )
    
    def getfiringtendencytext(f1 ,firt_x,firt_y):
        fttext=""
        ftcode=""
        
        t1=""
        t2=""
        t1code=""
        t2code=""
        
        if f1 >=0 and f1 < 90:
            t1="Top"
            t2="Right"
            t1code="T"
            t2code="R"
        elif f1 >=90 and f1 < 180:
            t1="Top"
            t2="Left"
            t1code="T"
            t2code="L"
        elif f1 >=180 and f1 < 270:
            t1="Bottom"
            t2="Left"
            t1code="B"
            t2code="L"
        else:
            t1="Bottom"
            t2="Right"
            t1code="B"
            t2code="R"
            
        ftcode=t1code+t2code
        fttext = t1+"("+str(firt_y)+") "+t2+"("+str(firt_x)+")"
            
        return fttext,ftcode
    
    
    def grouping_length(xt,yt,x ,y):
        d = {}
        counter=0
        
        #print('Hello',file=sys.stderr)
        #print(xt,file=sys.stderr)
        #print(yt,file=sys.stderr)
        #print(x,file=sys.stderr)
        #print(y,file=sys.stderr)
        for i in range(len(x)):
            for j in range(len(x)):
                #print(x[j],y[j],x[i],y[i],file=sys.stderr)
                d[counter]=distance(x[j],y[j],x[i],y[i])
                counter+=1
        #print('bye',file=sys.stderr)        
        maxdist = 0
        
        for key in d.keys():
            if(maxdist<d[key]):
                maxdist= d[key]
        
        maxdist_inch = pixeltoinch(maxdist)
        return maxdist_inch
            
        
        
    def distance (x1,y1,x,y):
        dist = 0 
        xdist = x1 - x
        ydist = y1 - y
        dist = math.sqrt(xdist**2 + ydist**2)
        return dist
    
    def pixeltoinch(maxdist):
        inch = (36/2000 *1.0)*maxdist
        return np.round(inch,1)
    
    def getresulttext(gpinch):
        print(type(gpinch),file=sys.stderr)
        print(gpinch,file=sys.stderr)
        if gpinch <=10:
            return "Pass"
        else:
            return "W/O"
       
    

    @app.route('/test', methods=['GET', 'POST'])       
    def update():
         mp=0
         gp_1=0
         tyf=0
         txf=0
         f_1=0
         xmpi_1=0
         ympi_1=0
         j_x=None
         j_y=None
         j_mp=None
         up_res_1=None
         mp_inch = []
         x1=[]
         y1=[]
         u_fir_tendency_txt=None
         u_fir_tendency_code=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx1 =data1['x1'] 

             for le in tx1:
                 x1.append(le[0])
                 
             ty1 = data1['y1']
             for le in ty1:
                 y1.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch.append(pixeltoinch(mp[0][0]))
             mp_inch.append(pixeltoinch(mp[0][1]))
             tmpi=mpi(1,points)
             xmpi_1 = tmpi[:, 1]
             ympi_1 = tmpi [:, 0]
             
             session['tmpi']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
             txf=txf_list[0]
             tyf=tyf_list[0]
             j_x=pd.Series(txf).to_json(orient='values')
             j_y=pd.Series(tyf).to_json(orient='values')
             
             #print("calling from update" ,file=sys.stderr)
             gp_1 = grouping_length(0 , 0 , x1 , y1)
             up_res_1=getresulttext(gp_1)
             u_fir_tendency_txt,u_fir_tendency_code = getfiringtendencytext(f_1,txf_list[0],tyf_list[0])
             session['x1'] = data1['x1']
             session ['y1'] = data1['y1']
             session['tf_u_1']=f_1
             session['gp_u_1']=gp_1
             session ['res_u_1']=up_res_1
             session ['tfirer_x1']=txf_list[0]
             session ['tfirer_y1']=tyf_list[0]

             
         return jsonify(mp = mp_inch ,
                        gp_1=gp_1,
                        ten_yu=j_y,
                        ten_xu=j_x,
                        result=up_res_1,
                        u_fir_tendency=u_fir_tendency_txt
                        )
        
         
     

    @app.route('/test2', methods=['GET', 'POST'])       
    def update2():
         if request.method == "POST":
             data2 = request.get_json()
             session['x2'] = data2['x2']
             session ['y2'] = data2['y2']
             points = data2['points2']
             x2 =data2['x2']
             y2 = data2['y2']
             mp2 = mpi(1,points).tolist()
             tmpi2 = mpi(1,points)
             xmpi_2 = tmpi2[:, 1]
             ympi_2 = tmpi2[:, 0]
             f_2  =firing_tendancy(1000, 1000 , xmpi_2, ympi_2)
             #gp_2 = grouping_length(xmpi_2 , ympi_2 , x2 , y2)
             print("calling from update2" ,file=sys.stderr)
             gp_2 = grouping_length(0, 0 , x2 , y2)
             #session['xmpi_2']=xmpi_2
             #session['ympi_2']=ympi_2
             #session['f_2']=f_2
             #session['gp_2']=gp_2
             
         return jsonify(mp2 = mp2 , 
                        gp_2=gp_2,
                        f_2=f_2)
     
    @app.route('/test3', methods=['GET', 'POST'])       
    def update3():
         if request.method == "POST":
             data3 = request.get_json()
             session['x3'] = data3['x3']
             session ['y3'] = data3['y3']
             points = data3['points3']
             x3 =data3['x3']
             y3 = data3['y3']
             mpi_3 = mpi(1,points).tolist()
             tmpi3 = mpi(1,points)
            # session['xmpi_3']=xmpi_3
             #session['ympi_3']=ympi_3
             xmpi_3 = tmpi3[:, 1]
             ympi_3 = tmpi3[:, 0]
             f_3  =firing_tendancy(1000, 1000 , xmpi_3, ympi_3)
             #session['f_3']=f_3
             #gp_3 = grouping_length(xmpi_3 , ympi_3 , x3 , y3)
             print("calling from update3" ,file=sys.stderr)
             gp_3 = grouping_length(0 , 0 , x3 , y3)
             #session['gp_3']=gp_3
         return jsonify(mpi_3 = mpi_3 , 
                        gp_3=gp_3,
                        f_3=f_3)
     
        
    @app.route('/test4', methods=['GET', 'POST'])       
    def update4():
         if request.method == "POST":
             data4 = request.get_json()
             session['x4'] = data4['x4']
             session ['y4'] = data4['y4']
             points = data4['points4']
             x4 =data4['x4']
             y4 = data4['y4']
             mp4 = mpi(1,points).tolist()
             tmpi4 = mpi(1,points)
             xmpi_4 = tmpi4[:, 1]
             ympi_4 = tmpi4[:, 0]
             f_4  =firing_tendancy(1000, 1000 , xmpi_4, ympi_4)
             #gp_4= grouping_length(xmpi_4 , ympi_4 , x4 , y4)
             print("calling from update4" ,file=sys.stderr)
             gp_4= grouping_length(0, 0, x4 , y4)
             #session['xmpi_4']=xmpi_4
             #session['ympi_4']=ympi_4
             #session['f_4']=f_4
             # session['gp_4']=gp_4
         return jsonify(mp4 = mp4 , gp_4 = gp_4 ,f_4 =f_4)
        
        
    def predictAsMatrix(image,width,height):
        step=25
        i=0
        resized_array =np.zeros(shape=(width//25,height//25))   
        while i<=height-25:
            j=0 
            while j<=height-25:
                patch = image.crop((i, j, i+25, j+25))
                img1=np.array(patch)
                image_data=color.rgb2gray(img1)
                img_data=merge_datasets(image_data)
                test_data = reformat(img_data)
                patchp=patchIdentification(test_data)
                resized_array[j//25][i//25]=patchp
                j=j+step
            i=i+step
        return resized_array
    

    def merge_datasets(img1):
        predict_dataset = make_arrays(1, 25, 25)
        predict_dataset[0:1, :, :] = img1
        return predict_dataset
    
    def make_arrays(nb_rows, image_height, image_width):
        if nb_rows:
            dataset = np.ndarray((nb_rows, image_height, image_width), dtype=np.float32)
        else:
            dataset = None
        return dataset
    
    
    def reformat(dataset):
        dataset = dataset.reshape((-1, 25*25)).astype(np.float32)
        return dataset
    
    
    def patchIdentification(data):
        w1 = graph.get_tensor_by_name("tf_test_image:0")
        feed_dict ={w1:data}
        op_to_restore = graph.get_tensor_by_name("test_prediction_image:0")
        predict= sess.run([op_to_restore],feed_dict=feed_dict)
        array=predict[0][0]
        if(array[0]>array[1]):
            return 0
        else :
            return 1
    
    
    class Graph:
        def __init__(self, row, col, g):
            self.ROW = row
            self.COL = col
            self.graph = g
        
        def isSafe(self, i, j, visited):
            return (i >= 0 and i < self.ROW and
                    j >= 0 and j < self.COL and
                    not visited[i][j] and self.graph[i][j])
             

        def DFS(self, i, j, visited):
            rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1];
            colNbr = [-1,  0,  1, -1, 1, -1, 0, 1];
            visited[i][j] = True
        
            for k in range(8):
                if self.isSafe(i + rowNbr[k], j + colNbr[k], visited):
                    self.DFS(i + rowNbr[k], j + colNbr[k], visited)
                
        def countIslands(self):
            visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
            count = 0
            for i in range(self.ROW):
                for j in range(self.COL):
                    if visited[i][j] == False and self.graph[i][j] ==1:
                        self.DFS(i, j, visited)
                        count += 1
            return count
        
        
    def points(data,h,w):
        i=0
        while (i<h):
            j=0
            while (j<w):
                if(data[i][j]==1):
                    pointsarray.append([i,j])
                j=j+1
            i=i+1
            
    def kmean(N,pointsarray):
        n=0
        while (n<=100):
            kmeans = KMeans(n_clusters=N, random_state=0).fit(pointsarray)
            center=kmeans.cluster_centers_ 
            centroid=((kmeans.cluster_centers_)*25)+12
            n=n+1
            return centroid 
        
    def mpi(N,pointsarray):
        n=0
        while (n<=100): 
            kmeans = KMeans(n_clusters=N, random_state=0).fit(pointsarray)
            center=kmeans.cluster_centers_ 
            centroid=(kmeans.cluster_centers_)
            cen_int = centroid.astype(int)
            n=n+1
            return cen_int
        
        
    if __name__ == "__main__":
        load_model()
        app.run()
        
        
    

    
    



    