import json
from bson.json_util import dumps
from bottle import run, request, response, Bottle, static_file
from bson import json_util

from pymongo import MongoClient

client = MongoClient('10.100.232.76', 27017)

db = client.alerta

# import pymysql.cursors
# from datetime import datetime

# connection = pymysql.connect(host='localhost',
#                              user='administrador',
#                              password='y2kalce04',
#                              db='snomed',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


config_file = open('config.json')
config_data = json.load(config_file)
pth_xml = config_data["paths"]["xml"]

app = Bottle()


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@app.route('/')
def index():
    return static_file('index.html', root='static')
    

@app.route('/examples', method=['OPTIONS', 'GET'])
def examples():
    if request.method == 'OPTIONS':
        return {'aaaa'}
    else:
        return {'examples': [{
            'id': 1,
            'name': 'Foo'}, {
            'id': 2,
            'name': 'Bar'}
        ]}


@app.route('/busqueda', method='GET')
def busqueda():
    term = request.query.term
    criterio = request.query.criterio
    if "" != term:
        # if criterio == 'partido':
        #     data = db.candidatos.find({"TXORGANIZACIONPOLITICA": {'$regex': term}},
        #                               {'TXAPELLIDOPATERNO': 1, 'TXAPELLIDOMATERNO': 1, 'TXNOMBRECOMPLETO': 1,
        #                                "TXAMBITO": 1, "TXORGANIZACIONPOLITICA": 1, "TXCARGOELECCION": 1,
        #                                "TXDOCUMENTOIDENTIDAD": 1, "TXAPELLIDOPATERNO": 1, "TXAPELLIDOMATERNO": 1,
        #                                "TXNOMBRECOMPLETO": 1, "FENACIMIENTO": 1, "TXREGIONPOSTULA": 1,
        #                                "TXPROVINCIAPOSTULA": 1, "TXDISTRITOPOSTULA": 1})
        #     for elem in data:
        #         print(elem)
        # elif criterio == 'lugar':
        #     data = db.candidatos.find({"$or": [{"TXREGIONPOSTULA": {'$regex': term}},
        #                                        {"TXPROVINCIAPOSTULA": {'$regex': term}},
        #                                        {"TXDISTRITOPOSTULA": {'$regex': term}}]},
        #                               {'TXAPELLIDOPATERNO': 1, 'TXAPELLIDOMATERNO': 1, 'TXNOMBRECOMPLETO': 1,
        #                                "TXAMBITO": 1, "TXORGANIZACIONPOLITICA": 1, "TXCARGOELECCION": 1,
        #                                "TXDOCUMENTOIDENTIDAD": 1, "TXAPELLIDOPATERNO": 1, "TXAPELLIDOMATERNO": 1,
        #                                "TXNOMBRECOMPLETO": 1, "FENACIMIENTO": 1, "TXREGIONPOSTULA": 1,
        #                                "TXPROVINCIAPOSTULA": 1, "TXDISTRITOPOSTULA": 1})
        #     for elem in data:
        #         print(elem)
        # elif criterio == 'candidato':
        #     data = db.candidatos.find({"$or": [{"TXAPELLIDOPATERNO": {'$regex': term}},
        #                                        {"TXAPELLIDOMATERNO": {'$regex': term}},
        #                                        {"TXNOMBRECOMPLETO": {'$regex': term}}]},
        #                               {'TXAPELLIDOPATERNO': 1, 'TXAPELLIDOMATERNO': 1, 'TXNOMBRECOMPLETO': 1,
        #                                "TXAMBITO": 1, "TXORGANIZACIONPOLITICA": 1, "TXCARGOELECCION": 1,
        #                                "TXDOCUMENTOIDENTIDAD": 1, "FENACIMIENTO": 1, "TXREGIONPOSTULA": 1,
        #                                "TXPROVINCIAPOSTULA": 1, "TXDISTRITOPOSTULA": 1})
        #     for elem in data:
        #         print(elem)
        #     print(term)
        html_view = '<strong>Ejemplo</strong>:Datos<br><a href="http://www.jne.gob.pe">JNE</a>'
        data = [
            {
                'id': 1,
                'name': 'Leoncio Prado',
                'location': {'lat': '-6.9902628', 'long': '-76.2359984,16'},
                'html': html_view
            }, {
                'id': 2,
                'name': 'Lince',
                'location': {'lat': '-12.078137', 'long': '-77.0445096,15'},
                'html': html_view
            }
        ]
        result = {'status': True, 'data': data}
        return result
    else:
        return {"status": False, "error": "show called without a filename"}


@app.route('/candidato/<id:int>', method='GET')
def candidato(id):
    html_view = '<strong>Manuel Perez</strong><a href="http://www.jne.gob.pe">JNE</a>'
    return html_view


@app.route('/lugar/<id:int>', method='GET')
def lugar(id):
    html_view = '<strong>Distrito:</strong>Lince<br><strong>Candidatos:</strong>Manuel Perez<br>Javier Vásquez<br><a href="http://www.jne.gob.pe">JNE</a>'
    return html_view


@app.route('/partido/<id:int>', method='GET')
def partido(id):
    html_view = '<strong>Somos Perú</strong><br><a href="http://www.jne.gob.pe">JNE</a>'
    return html_view

@app.route('/judicial', method='GET')
def judicial():
    data = db.judicial.find()
    return dumps(data)


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--host", dest="host", default="localhost",
                      help="hostname or ip address", metavar="host")
    parser.add_option("--port", dest="port", default=8080,
                      help="port number", metavar="port")
    (options, args) = parser.parse_args()
    run(app, host=options.host, port=int(options.port))
