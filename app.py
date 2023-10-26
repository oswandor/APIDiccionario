import os
from flask import Flask, redirect, render_template, request , send_from_directory, url_for , jsonify  
from Models.MongoDBConnection import MongoDBConnection
from bson.json_util import dumps  # Importa dumps desde bson.json_util

app = Flask(__name__)

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
        mongo_connection.connect()
            
        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})
            
        if results:
             # Crear un diccionario con el orden deseado
            response_data = {
                "word": results["word"],
                "definition": results["definition"]
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
        mongo_connection.connect()

        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})

        if results:
            sinonimos = results.get("synonyms", [])
            return jsonify({"word": word, "sinonimos": sinonimos})
        else:
            return "No se encontraron definiciones para la palabra: " + word
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/antonimos/<word>')
def antonimos(word): 
    try:
        # Intentar establecer la conexión a MongoDB
        mongo_connection.connect()

        # Realizar consultas a la base de datos usando el método perform_query
        results = mongo_connection.perform_query({"word": word})

        if results:
            antonimos = results.get("antonyms", [])
            return jsonify({"word": word, "antonimos": antonimos})
        else:
            return "No se encontraron definiciones para la palabra: " + word
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
    app.run(debug=True)
