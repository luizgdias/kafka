from kafka import KafkaConsumer
from confluent_kafka import Consumer
import os, sys, json
import settings

# ################################################################################
# Arquivo que contém consumers das bibliotecas concluente kafka-python
# O consumer confluent está configurado para cluster kerberizado.
# O consumer kafka-python está configurado para cluster padrão
# os parâmetros de cada consumer devem ser definidos no arquivo settings.py
# ################################################################################

def consumer_confluent():
    consumer = Consumer({
                        'bootstrap.servers': settings.KAFKA_HOST, 
                        'security.protocol': settings.KAFKA_SECURITY_PROTOCOL, 
                        'group.id': settings.KAFKA_CONSUMER_GROUP_ID,
                        'auto.offset.reset': settings.KAFKA_OFFSET_RESET,
                        'sasl.mechanism': settings.KAFKA_SALS_MECHANISM, 
                        'sasl.kerberos.service.name': settings.KERBEROS_SERVICE_NAME, 
                        'sasl.kerberos.keytab': settings.KAFKA_USER_KEY_TAB_PATH,
                        'sasl.kerberos.principal': settings.KAFKA_KERBEROS_USERNAME  
        })

    consumer.subscribe(settings.KAFKA_CONSUMER_TOPIC)
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        print('Received message: {}'.format(msg.value().decode('utf-8')))
    consumer.close()

def consumer_kafka_python():
    consumer = KafkaConsumer(
                                settings.KAFKA_CONSUMER_TOPIC,
                                bootstrap_servers       = settings.KAFKA_HOST,
                                auto_offset_reset       = settings.KAFKA_OFFSET_RESET,
                                enable_auto_commit      = settings.KAFKA_AUTO_COMMIT,
                                auto_commit_interval_ms = settings.KAFKA_AUTO_COMMIT_INTERVAL,
                                group_id                = settings.KAFKA_CONSUMER_GROUP_ID,
                                value_deserializer      = lambda x: json.loads(x.decode('utf-8'))
                                # consumer_timeout_ms=15000
                            )
    for message in consumer:
        print(message.value)
    consumer.close()