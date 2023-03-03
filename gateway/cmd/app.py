from flask import Flask, jsonify
import grpc
import os 

import files_pb2, files_pb2_grpc
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Se configura la dirección y puerto del servidor gRPC
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PORT = os.getenv("PORT")

@app.route("/files")
def list_files():
    with grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}') as channel:
        # Cliente para el servicio de ListFiles
        list_files_client = files_pb2_grpc.FilesStub(channel)

        # Se llama al servicio de ListFiles
        response = list_files_client.GetFilesList(files_pb2.ListFilesRequest())

        # Se retorna la lista de archivos en formato JSON
        return jsonify({"files": [file.filename for file in response.files]})
