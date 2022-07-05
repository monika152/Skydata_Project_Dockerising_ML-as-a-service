from copyreg import pickle
from turtle import st
from numpy import float64
import pandas as pd 
from flask import Flask, jsonify, request
import pickle
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import sqlite3
from pathlib import Path
import datetime



app = Flask(__name__)
model = pickle.load(open('model.pickle','rb'))



@app.route('/')
def home():
    return "Welcome to Stellar Objects Classification"


@app.route('/predict', methods=['GET'])
def predict():
    objid = request.args.get('objid')
    ra = request.args.get('ra')
    dec = request.args.get('dec')
    u = request.args.get('u')
    g = request.args.get('g')
    r = request.args.get('r')
    i = request.args.get('i')
    z = request.args.get('z')
    run = request.args.get('run')
    camcol = request.args.get('camcol')
    field = request.args.get('field')
    specobjid = request.args.get('specobjid')
    redshift = request.args.get('redshift')
    plate = request.args.get('plate')
    mjd = request.args.get('mjd')
    fiberid = request.args.get('fiberid')
    
    

    makeprediction = model.predict([[objid,ra,dec,u,g,r,i,z,run,camcol,field,specobjid,redshift,plate,mjd,fiberid]])
    makepredictionstr = str(makeprediction[0])


    os.chdir(Path(__file__).parent)

    DB_FILE_PATH = Path(__file__).parent / "predictiondatabase.db"

    conn = sqlite3.connect(DB_FILE_PATH)

    c = conn.cursor()


    my_datetime = str(datetime.datetime.now())
    sql_statement = "INSERT INTO inputs_and_prediction(objid, ra, dec, u, g, r, i, z, run, camcol, field, specobjid, redshift, plate, mjd, fiberid, makepredictionstr, my_datetime) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

    data = (objid, ra, dec, u, g, r, i, z, run, camcol, field, specobjid, redshift, plate, mjd, fiberid, makepredictionstr, my_datetime)


    c.execute(sql_statement,data)
    # 5 commit changes
    conn.commit()

    # 6 close the connection
    conn.close()



    return jsonify({'Steller Object is':(str(makeprediction[0]))})


@app.route('/inputs')
def inputsdata():

    os.chdir(Path(__file__).parent)

    DB_FILE_PATH = Path(__file__).parent / "predictiondatabase.db"

    conn = sqlite3.connect(DB_FILE_PATH)

    c = conn.cursor()

    sql_statement = 'SELECT * FROM inputs_and_prediction;'

    c.execute(sql_statement)

    result = c.fetchall()
    resultsstr = str(result)

    conn.close()
    
    
    
    return resultsstr


    
if __name__=='__main__':
    app.run(host="0.0.0.0")