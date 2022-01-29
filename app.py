from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_file
import pandas as pd
from pandas import json_normalize
import os
import json
import pdb #debugg  pdb.set_trace()

app = Flask(__name__)

# Carpeta de subida
app.config['UPLOAD_FOLDER'] = 'v_descargar/'
ALLOWED_EXTENSIONS = set(['csv'])

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'json', 'data_in.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v_informativo',methods=['POST','GET'])
def v_informativo():
    return render_template('v_informativo.html')

@app.route('/v_pronostico',methods=['POST','GET'])
def v_pronostico():    
    data = json_input(FILE_INPUT)
    #data['canColum'] = range(len(data['col_names']))
    return render_template('v_pronostico.html',data=data)    

def request_aws():
    """
    Consultar servicio API GETGAY AWS y actuaizar el fichero JSON
    """
    pass

def json_input(file):
    """
    leer datos del json local
    """
    with open (file,'rb') as file:
        data = json.load(file)
    return data 

@app.route("/conversor_json_dataframe_", methods=['POST'])
def conversor_json_dataframe_():
    data = json_input(FILE_INPUT)    
    df = json_normalize(data)
    df.to_csv('v_descargar/data.csv', sep=',', header=True, index=False)
    return "ok"

@app.route('/v_descargar',methods=['POST','GET'])
def v_descargar():
    nomTabla = 'data'
    data = json_input(FILE_INPUT)     
    path = app.config['UPLOAD_FOLDER']+nomTabla+'.csv'
    path_descarga = app.config['UPLOAD_FOLDER']
    df = pd.DataFrame(data=data['data']) 
    v_columns = data['col_names']
    #pdb.set_trace()
    df.to_csv(path, sep=';', header=v_columns, index=False)
    return send_file(path_descarga, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True) 