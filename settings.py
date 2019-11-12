from os.path import dirname, join
import os

####################################################################
# Um tutorial de uso kafka está disponível em:
# https://github.com/luizgdias/kafka/blob/master/index.md 
# 
####################################################################

KAFKA_HOST                  = "localhost:9092"
KAFKA_SECURITY_PROTOCOL     = "SASL_PLAINTEXT"
KAFKA_PRODUCER_TOPIC        = "test-topic"
KAFKA_CONSUMER_TOPIC        = "test-topic"
KAFKA_SALS_MECHANISM        = "GSSAPI"
SASL_PLAINTEXT              = ""
GSSAPI                      = ""
KAFKA_USER_KEY_TAB_PATH     = "confs/app-secrets/kafka-client.beytab"
KAFKA_KERBEROS_USERNAME     = ""
KAFKA_CONSUMER_GROUP_ID     = "group1"
KAFKA_OFFSET_RESET          = "earliest"
KAFKA_AUTO_COMMIT           = "True"
KAFKA_AUTO_COMMIT_INTERVAL  = 1000
KERBEROS_SERVICE_NAME       = "kafka"
KAFKA_API_VERSION           = (0,10,1)