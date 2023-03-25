import pika
import uuid
from dotenv import load_dotenv
import os

rmq_host = os.getenv('HOST_RMQ')
rmq_port = os.getenv('PORT_RMQ')
rmq_user = os.getenv('USER')
rmq_password = os.getenv('PASSWORD')
rmq_queue = os.getenv('QUEUE')
#Clase que contiene todo el codgio necesario para establecer conexion con RabbitMQ y enviar solicitudes al consumidor
class ArchivoMOM:
    #Conexion a RMQ y creacion de canal exclusiva que se utilizara por el productor para recibir respuestas del consumidor
    def __init__(self):
        self.connection =  pika.BlockingConnection(pika.ConnectionParameters(host=rmq_host, 
                                                                port=int(rmq_port),
                                                                credentials= pika.PlainCredentials(username=rmq_user,password=rmq_password)))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        #Cola para recibir respuesta del consumidor tras enviar la solicitud
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
#
    #Sera llamada cuando reciba la respuesta del consumidor. 
    # Esta función compara el identificador de correlacion de la respuesta con el identificador de correlacion de la solicitud original.
    #Si coinnciden, la respuesta se almacena en self.response

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    #Funcion para enviar solicitudes al consumidor.  Toma el archivo que se esta buscando como argumento.
    def call(self, filename):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='search_files',
            routing_key='archivo_rpc',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=filename)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode()

#file_mom = ArchivoMOM()

#filename = input("Ingrese el nombre del archivo que desea buscar: ")
#response = file_mom.call(filename)
#print(response)
