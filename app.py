
import os
from flask import Flask, redirect, render_template, request , send_from_directory, url_for , jsonify  
from Models.MongoDBConnection import MongoDBConnection
from bson.json_util import dumps  # Importa dumps desde bson.json_util
from flask_cors import CORS
from bson import ObjectId
 

app = Flask(__name__)


# Configura CORS para permitir solicitudes desde cualquier origen en múltiples rutas
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# Define the MongoDB URI
#mongo_uri = "mongodb+srv://oswandor26:u3w6dhSXLjZ3iN0g@cluster0.mmmsz3e.mongodb.net/?retryWrites=true&w=majority"

mongo_uri =  os.getenv("MONGO_URI")

if not mongo_uri: 
    print("Error Get Enviroment")


# Crear una conexión MongoDB persistente en la aplicación
mongo_connection = MongoDBConnection(mongo_uri)

@app.route('/definicion/<word>')
def index(word):
    try:
        # Intentar establecer la conexión a MongoDB
        mongo_connection.connect("dbdiccionario" , "diccionario")
            
        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})
            
        if results:
             # Crear un diccionario con el orden deseado
            response_data = {
                "_id" : str(results['_id']) ,
                "word": results["word"],
                "definition": results["definition"],
                "examples" : results["examples"],
              
             }


            return jsonify(response_data)
        else:
            return "No se encontraron definiciones para la palabra: " + word

    except  Exception as e:  
        return jsonify(e) 



@app.route('/sinonimos/<word>')
def sinonimos(word):
    try:
        # Intentar establecer la conexión a MongoDB
        mongo_connection.connect("dbdiccionario" , "diccionario")

        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})

        if results:
            sinonimos = results.get("synonyms", [])
            return jsonify({   "_id" : str(results['_id']) ,  "word": word, "sinonimos": sinonimos})
        else:
            return "No se encontraron definiciones para la palabra: " + word
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/antonimos/<word>')
def antonimos(word): 
    try:
        # Intentar establecer la conexión a MongoDB
        mongo_connection.connect("dbdiccionario" , "diccionario")

        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})

        if results:
            antonimos = results.get("antonyms", [])
            return jsonify({   "_id" : str(results['_id']) , "word": word, "antonimos": antonimos})
        else:
            return "No se encontraron definiciones para la palabra: " + word
    except Exception as err:
       return jsonify({"error": str(err)})


# obtener la lista de Favoritos para el usuario 
@app.route('/allUserFavorites/<uid>') 
def allUserFavorites(uid):
    try: 
        # Intentar establecer conexcion 
        mongo_connection.connect("dbdiccionario" , "userFavorites")

        # Definir el pipeline de agregación
        user_uid = str(uid)
        print(uid)
        # Definir el pipeline de agregación
        pipeline = [
            {
                "$match": {"_uid": user_uid}
            },
            {
                "$lookup": {
                    "from": "diccionario",
                    "localField": "_idDiccionary",
                    "foreignField": "_id",
                    "as": "favoritos"
                }
            },
            {
                "$unwind": "$favoritos"
            },
            {
                "$project": {
                    "_id": 1,
                    "userUID": 1,
                    "favoritos.word": 1,
                    "favoritos.definition": 1,
                    "favoritos.examples": 1,
                    "favoritos.synonyms": 1,
                    "favoritos.antonyms": 1
                }
            }
        ]
        
        result = mongo_connection.aggregate_query(pipeline)

        # Convertir ObjectId a cadena antes de serializar a JSON
        result = dumps(result)

        # Imprimir el resultado
        print(result)

        return result, 200, {'Content-Type': 'application/json'}
    except Exception as err:
        return jsonify({"error": str(err)}) 


# agregar por metodo POST  
@app.route('/addFavorite', methods=['POST']) 
def addFavorite(): 
    try: 
        # conexión a MongoDB 
        mongo_connection.connect("dbdiccionario", "userFavorites") 
        
        # Obtén los datos JSON de la solicitud
        data = request.get_json()

        # Verifica que se hayan proporcionado todos los campos necesarios
        if 'uid' not in data or 'idDiccionary' not in data:
            return jsonify({"error": "Missing uid or idDiccionary"})

        uid = data['uid']
        idDiccionary = data['idDiccionary']

        objecdiccionary  = ObjectId(idDiccionary)
        # Agrega a favoritos con el ID y la relación de la palabra 
        objectfavorites = {
            "_uid": uid, 
            "_idDiccionary": objecdiccionary
        }
        mongo_connection.add_tofavorites(objectfavorites) 

        # Desconéctate de la base de datos 
        mongo_connection.disconnect() 

        return jsonify({"message": "success"})
    except Exception as e: 
        # Enviar el error
        return jsonify({"error": str(e)})





# Eliminar favoritos por idDiccionary
@app.route('/deleteUserFavoritesByIdDiccionary/<uid>/<idDiccionary>', methods=['DELETE'])
def deleteUserFavoritesByIdDiccionary(uid, idDiccionary):
    try:
        # Intentar establecer conexión
        mongo_connection.connect("dbdiccionario", "userFavorites")

        objecdiccionary  = ObjectId(idDiccionary)
        # Eliminar registros que coincidan con el UID e idDiccionary
        delete_result = mongo_connection.delete_documents({"_uid": uid, "_idDiccionary": objecdiccionary })

        # Imprimir el resultado de la eliminación
        print(f"Deleted {delete_result} records for UID: {uid} and idDiccionary: {idDiccionary}")

        # Desconectar de la base de datos
        mongo_connection.disconnect()

        return jsonify({"message": "success"})
    except Exception as err:
        return jsonify({"error": str(err)})




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
