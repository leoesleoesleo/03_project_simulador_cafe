from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_file
import requests
import pandas as pd
from pandas import json_normalize
import os
import json
import random
import logging
from os import remove
from werkzeug.utils import secure_filename
import pdb #debugg  pdb.set_trace()
import shutil

app = Flask(__name__)

# Carpeta de subida
app.config['UPLOAD_FOLDER'] = 'v_descargar/'
ALLOWED_EXTENSIONS = set(['csv'])

# Carpeta JSON
app.config['JSON_FOLDER'] = 'json/'

ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'json', 'data_in.json')
FILE_DESAGREGACION = os.path.join(ROOT_FILE, 'json', 'desagregacion.json')

FILE_GENERATED = 'data'

JSON_DATA_IN = 'data_in'
FILE_BKP = 'data_in_bkp'

logging.basicConfig(level = 10,  format   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt  = '%Y-%m-%d %H:%M:%S',  filename = 'log.log',  filemode = 'w')

log = logging.getLogger('')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v_informativo',methods=['POST','GET'])
def v_informativo():
    return render_template('v_informativo.html')

@app.route('/v_pronostico',methods=['POST','GET'])
def v_pronostico(): 
    data = 0   
    combinatoria = 'No Data'
    return render_template('v_pronostico.html',data=data,combinatoria=combinatoria)

@app.route('/v_optimizacion',methods=['POST','GET'])
def v_optimizacion(): 
    data = 0   
    combinatoria = 'No Data'
    return render_template('v_optimizacion.html',data=data,combinatoria=combinatoria)

@app.route('/traer_data',methods=['POST','GET'])
def traer_data():    
    if request.method == 'POST':
        fuente = request.form['fuente']
        marca = request.form['marca']
        categoria = request.form['categoria']
        region = request.form['region']
        canal = request.form['canal']

        data = json_input(FILE_INPUT)
        combinatoria = str(fuente + '-' + marca + '-' + categoria + '-' + region + '-' + canal)
        #data['canColum'] = range(len(data['col_names']))
    return render_template('v_pronostico.html',data=data,combinatoria=combinatoria) 

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

@app.route("/v_desagregacion", methods=['POST'])
def v_desagregacion():
    if request.method == 'POST':
        tipo = request.form['desagregacion']
        data_desagregacion = json_input(FILE_DESAGREGACION)[tipo]
        data = {
            'data_desagregacion' : data_desagregacion
        }
    return render_template('select.html',data=data)
    
@app.route("/conversor_json_dataframe_", methods=['POST'])
def conversor_json_dataframe_():
    data = json_input(FILE_INPUT)    
    df = json_normalize(data)
    df.to_csv('v_descargar/data.csv', sep=',', header=True, index=False)
    return "ok"

@app.route('/v_descargar',methods=['POST','GET'])
def v_descargar():
    data = json_input(FILE_INPUT)     
    path = app.config['UPLOAD_FOLDER']+FILE_GENERATED+'.csv'
    df = pd.DataFrame(data=data['data']) 
    v_columns = data['col_names']
    #pdb.set_trace()
    df.to_csv(path, sep=';', header=v_columns, index=False)
    return send_file(path, as_attachment=True)

@app.route("/upload", methods=['POST'])
def upload():
    log.info("Info Proceso Upload iniciado")
    response = "sinprocesar"
    if request.method == 'POST':
        archivo   = request.form['archivo']
        #print(archivo,"*****************")
        # obtenemos el archivo del input "archivo" LEER ARCHIVO
        f = request.files['inputArchivoCarga']
        filename = secure_filename(f.filename)
        # VALIDAR EXTENSION CSV
        if f and allowed_file(f.filename):
            # GUARDAR ALEATORIO
            numAleatorio = random.randrange(10, 99)
            nombreFichero = 'temp_'+str(numAleatorio)+'.csv'
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFichero))
            print("archivo guardado: ",nombreFichero)
            try:
                # VALIDAR ESTRUCTURA
                df = pd.read_csv(app.config['UPLOAD_FOLDER']+nombreFichero,delimiter=";", encoding = "ISO-8859-1", low_memory=False) #encoding = "cp1252"            
            except Exception as e:
                print("Error al leer el CSV")
                log.error("Error al leer el CSV" + str(e))
                response = "ErrorCsv"
            data = json_input(FILE_INPUT)   
            v_columns = data['col_names']
            print("Columnas fichero: ",v_columns)
            print("Columnas bd: ",df.columns.values.tolist())
            if(set(df.columns.values.tolist()) == set(v_columns)): #comparar columnas de la tabla bd vs arhivo a subir
                try:
                    print("@@comparar columnas OK")
                    df.iloc[:,1][0]
                    if f.filename == '':
                        response = "nodata"
                    log.info("Info Proceso de reemplazar archivo")
                    print("Info Proceso de reemplazar archivo")
                    # ACTUALIZAR DATA AWS, CONSUMIR ENDPOINT
                    request_aws()
                    # GENERAR BKP
                    src = app.config['JSON_FOLDER']+JSON_DATA_IN+'.json'
                    des = app.config['JSON_FOLDER']+FILE_BKP+'.json'
                    shutil.copy(src, des)
                    # ELIMINAR JSON ANTERIOR
                    remove(app.config['JSON_FOLDER']+JSON_DATA_IN+'.json')                      
                    # CREAR JSON ACTUALIZADO
                    des = app.config['JSON_FOLDER']+JSON_DATA_IN+'.json'
                    df.to_json(des, orient = 'split')                    
                    # ELIMINAR CSV GENERADO
                    remove(app.config['UPLOAD_FOLDER']+nombreFichero)
                    response = "procesoOk"
                except Exception as error:
                    log.error("Error en el proceso Upload" + str(error))    
                    response = 'Error'
            else:
                response = "noformato"      
        else:   
            response = "noextension"                        
        return response

@app.route("/v_rollback", methods=['POST'])
def v_rollback():
    # PROCESO BKP
    src = app.config['JSON_FOLDER']+FILE_BKP+'.json'
    des = app.config['JSON_FOLDER']+JSON_DATA_IN+'.json'
    shutil.copy(src, des)
    print("v_rollback --OK--")
    return "resok"    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True) 