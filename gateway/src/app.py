from flask import Flask, jsonify, request
import grpc
import os 
import pika
import producerRMQ
import uuid
import json


import files_pb2, files_pb2_grpc
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

host_rmq = os.getenv("HOST_RMQ")
host_grpc = os.getenv("HOST_GRPC")
#Se configura las credenciales y el puerto de RabbitMQ
rmq_port = os.getenv('PORT_RMQ')
rmq_user = os.getenv('USER')
rmq_password = os.getenv('PASSWORD')
# Se configura el puerto del servidor gRPC
grpc_port = os.getenv("PORT_GRPC")


@app.route('/search-files')
def search_files():
    query = request.args.get('query')
    producer = producerRMQ.ArchivoMOM()
    data = producer.call(query)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/files")
def list_files():
    with grpc.insecure_channel(f'{host_grpc}:{grpc_port}') as channel:
        # Cliente para el servicio de ListFiles
        list_files_client = files_pb2_grpc.FilesStub(channel)

        # Se llama al servicio de ListFiles
        response = list_files_client.GetFilesList(files_pb2.ListFilesRequest())

        # Se retorna la lista de archivos en formato JSON
        return jsonify({"files": [file.filename for file in response.files]})


if __name__ == '__main__':
    app.run(host='0.0.0.0')