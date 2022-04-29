from flask import (
    Flask,
    render_template,
    request
)
from flask import send_file
import pandas as pd
from pandas import json_normalize
import os
import json
import random
import logging
from os import remove
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

logging.basicConfig(
    level=10,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='log.log',
    filemode='w'
)

log = logging.getLogger('')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route(
    '/v_informativo',
    methods=['POST', 'GET']
)
def v_informativo():
    return render_template('v_informativo.html')


@app.route(
    '/v_pronostico',
    methods=['POST', 'GET']
)
def v_pronostico():
    data = 0
    combinatoria = 'No Data'
    return render_template(
        'v_pronostico.html',
        data=data,
        combinatoria=combinatoria
    )


@app.route(
    '/v_optimizacion',
    methods=['POST', 'GET']
)
def v_optimizacion():
    data = 0
    combinatoria = 'No Data'
    return render_template(
        'v_optimizacion.html',
        data=data,
        combinatoria=combinatoria
    )


@app.route(
    '/traer_data',
    methods=['POST', 'GET']
)
def traer_data():
    if request.method == 'POST':
        fuente = request.form['fuente']
        marca = request.form['marca']
        categoria = request.form['categoria']
        region = request.form['region']
        canal = request.form['canal']
        combinatoria = str(
            fuente +
            '-' + marca +
            '-' + categoria +
            '-' + region +
            '-' + canal
        )

        data = json_input(FILE_INPUT)

        labels_kilos = [i[3] for i in data['data_pron']]
        anio_mes = [str(
            str(i[0]) + '-' + str(i[1])
            ) for i in data['data_pron']]
        labels_volumen = [i[5] for i in data['data_pron']]

        a = data['variables_notables']
        b = data['variables_notables_value']
        labels_var_notables = [i for _, i in sorted(
                zip(b, a),
                reverse=True
            )][0:14]

        value_var_notables = sorted(
                data['variables_notables_value'],
                reverse=True
            )[0:14]

        metrica = round(data["metrica"]*100)
        error = round(data["porcentaje_error"]*100)

        combinatoria = {
            'combinatoria': combinatoria,
            'fuente': fuente,
            'marca': marca,
            'categoria': categoria,
            'region': region,
            'canal': canal
        }
    return render_template(
        'v_pronostico.html',
        data=data,
        combinatoria=combinatoria,
        labels_kilos=labels_kilos,
        anio_mes=anio_mes,
        labels_volumen=labels_volumen,
        labels_var_notables=labels_var_notables,
        value_var_notables=value_var_notables,
        metrica=metrica,
        error=error
    )


def request_aws():
    """
    Consultar servicio API GETGAY AWS y actuaizar el fichero JSON
    """
    pass


def json_input(file):
    """
    leer datos del json local
    """
    with open(file, 'rb') as file:
        data = json.load(file)
    return data


@app.route("/v_listar_regiones", methods=['POST'])
def v_listar_regiones():
    if request.method == 'POST':
        data_desagregacion = json_input(FILE_DESAGREGACION)
        v_region = []
        for region in data_desagregacion['region']:
            v_region.append(region['name'])
        data = {
            'data_desagregacion': v_region
        }
    return render_template('select.html', data=data)


@app.route("/v_listar_canales", methods=['POST'])
def v_listar_canales():
    if request.method == 'POST':
        data_desagregacion = json_input(FILE_DESAGREGACION)
        param_region = request.form['region']
        v_canal = []
        for region in data_desagregacion['region']:
            if region['name'] == param_region:
                for canal in region['canal']:
                    v_canal.append(canal['name'])
        data = {
            'data_desagregacion': v_canal
        }
    return render_template(
        'select.html',
        data=data
    )


@app.route("/v_listar_categorias", methods=['POST'])
def v_listar_categorias():
    if request.method == 'POST':
        data_desagregacion = json_input(FILE_DESAGREGACION)
        param_region = request.form['region']
        param_canal = request.form['canal']
        v_categoria = []
        for region in data_desagregacion['region']:
            if region['name'] == param_region:
                for canal in region['canal']:
                    if canal['name'] == param_canal:
                        for categoria in canal['categoria']:
                            v_categoria.append(categoria['name'])
        data = {
            'data_desagregacion': v_categoria
        }
    return render_template(
        'select.html',
        data=data
    )


@app.route("/v_listar_marcas", methods=['POST'])
def v_listar_marcas():
    if request.method == 'POST':
        data_desagregacion = json_input(FILE_DESAGREGACION)
        param_region = request.form['region']
        param_canal = request.form['canal']
        param_categoria = request.form['categoria']
        v_marca = []
        for region in data_desagregacion['region']:
            if region['name'] == param_region:
                for canal in region['canal']:
                    if canal['name'] == param_canal:
                        for categoria in canal['categoria']:
                            if categoria['name'] == param_categoria:
                                for marca in categoria['marca']:
                                    v_marca.append(marca['name'])
        data = {
            'data_desagregacion': v_marca[0]
        }
    return render_template('select.html', data=data)


@app.route("/conversor_json_dataframe_", methods=['POST'])
def conversor_json_dataframe_():
    data = json_input(FILE_INPUT)
    df = json_normalize(data)
    df.to_csv('v_descargar/data.csv', sep=',', header=True, index=False)
    return "ok"


@app.route(
    '/v_descargar',
    methods=['POST', 'GET']
)
def v_descargar():
    data = json_input(FILE_INPUT)
    path = app.config['UPLOAD_FOLDER']+FILE_GENERATED+'.csv'
    df = pd.DataFrame(data=data['data_acc'])
    v_columns = data['col_names_acc']
    df.to_csv(path, sep=';', header=v_columns, index=False)
    return send_file(path, as_attachment=True)


@app.route("/upload", methods=['POST'])
def upload():
    log.info("Info Proceso Upload iniciado")
    response = "sinprocesar"
    if request.method == 'POST':
        # 01 - leer y generar CSV
        # obtenemos el archivo del input "archivo"
        f = request.files['inputArchivoCarga']

        # 02 - Validar Extensión
        if f and allowed_file(f.filename):
            # 03 - Guardar id unico
            numAleatorio = random.randrange(10, 99)
            nombreFichero = 'temp_'+str(numAleatorio)+'.csv'
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFichero))
            print("archivo guardado: ", nombreFichero)
            try:
                # 04 - Convertir y generar DF
                df = pd.read_csv(
                    app.config['UPLOAD_FOLDER'] + nombreFichero,
                    delimiter=";",
                    encoding="ISO-8859-1",
                    low_memory=False
                )
            except Exception as e:
                print("Error al leer el CSV")
                log.error("Error al leer el CSV" + str(e))
                response = "ErrorCsv"
            # 05 - Leer JSON anterior
            data = json_input(FILE_INPUT)

            # 06 - validar extructura
            v_columns = data['col_names_acc']

            # 07 - Validar columnas y campos
            # comparar columnas de la tabla bd vs arhivo a subir
            if(set(df.columns.values.tolist()) == set(v_columns)):
                try:
                    print("@@comparar columnas OK")
                    df.iloc[:, 1][0]
                    if f.filename == '':
                        response = "nodata"
                    log.info("Info Proceso de reemplazar archivo")

                    # 08 - Unificar JSON
                    data_merge = {
                        "data_acc": df.values.tolist(),
                        "col_names_acc": df.columns.tolist(),
                        "data_noacc": data["data_noacc"],
                        "col_names_noacc": data["col_names_noacc"],
                        "data_pron": data["data_pron"],
                        "col_names_pron": data["col_names_pron"],
                        "posible": data["posible"],
                        "variables_notables": data["variables_notables"],
                        "variables_notables_value": (
                            data["variables_notables_value"]
                            ),
                        "metrica": data["metrica"],
                        "porcentaje_error": data["porcentaje_error"],
                        "variables_accionables": data["variables_accionables"]
                    }

                    # 09 - Consumir API y enviar nueva data
                    request_aws()

                    # 10- Generar BKP JSON
                    src = app.config['JSON_FOLDER']+JSON_DATA_IN+'.json'
                    des = app.config['JSON_FOLDER']+FILE_BKP+'.json'
                    shutil.copy(src, des)

                    # 11 - Validar JSON respuesta

                    # 12 - Eliminar JSON anterior
                    remove(app.config['JSON_FOLDER']+JSON_DATA_IN+'.json')

                    # 13 - Eliminar CSV generado
                    remove(app.config['UPLOAD_FOLDER']+nombreFichero)

                    # 14 - Reemplazar JSON
                    des = app.config['JSON_FOLDER']+JSON_DATA_IN+'.json'

                    with open(des, 'w') as file:
                        json.dump(data_merge, file)

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
    app.run(host='0.0.0.0', port=5000, debug=True)
