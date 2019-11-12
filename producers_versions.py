from confluent_kafka import Producer
from kafka import KafkaProducer
from kafka import TopicPartition
from json import loads
import os, sys, json
import settings

# ################################################################################
# Arquivo que contém producer das bibliotecas concluente kafka-python
# O producer confluent está configurado para cluster kerberizado.
# O producer kafka-python está configurado para cluster padrão
# os parâmetros de cada producer devem ser definidos no arquivo settings.py
# ################################################################################

def producer_confluent(data_to_send):
        os.environ['KRB5_CONFIG'] = os.environ['KAFKA_KRB5-CONF-PATH']
        producer_conf = {   
                            'bootstrap.servers': settings.KAFKA_HOST, 
                            'security.protocol': settings.SASL_PLAINTEXT, 
                            'sasl.mechanism': settings.GSSAPI, 
                            'sasl.kerberos.service.name': settings.KERBEROS_SERVICE_NAME, 
                            'sasl.kerberos.keytab': settings.KAFKA_USER_KEY_TAB_PATH,
                            'sasl.kerberos.principal': settings.KAFKA_KERBEROS_USERNAME  
                        }     
        if(('KAFKA_DEBUG' in os.environ) and (os.environ['KAFKA_DEBUG'].lower() == 'true')):
            producer_conf['debug'] = 'security,broker'

        producer = Producer(producer_conf)
        conv = str(data_to_send)
        try:
            producer.produce(settings.KAFKA_PRODUCER_TOPIC, conv.encode('utf8'))
            producer.flush()
        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(producer))

def producer_kafka_python(data_to_send):
    json_str = json.dumps(str(data_to_send), indent=4, sort_keys=True)
    print(json_str)
    producer = KafkaProducer(   
                                bootstrap_servers= [settings.KAFKA_HOST],
                                api_version= settings.KAFKA_API_VERSION, 
                                value_serializer=lambda v: json.dumps(v).encode('utf-8')
                            )   
    producer.send(settings.KAFKA_PRODUCER_TOPIC, json_str)
    producer.flush()