# Instruções para Execução - Apache Kafka

Este hands-on tem a finalidade de conceituar e demonstrar o funcionamento do Apache Kafka e Zookeeper, em sua forma nativa, via containers docker, e como configurar o cluster para funcionar em ambiente distribudo com o kafka sendo executado em um servidor isolado, sendo acessado por diferentes nós.

### O que é o Apache Kafka?
O Apache Kafka é uma aplicação utilizada no desenvolvimento de pipelines de tempo real e streamming. Suas principais caractersticas são: escalabilidade, tolerância a falhas, e velocidade na troca de mensagens entre os módulos que o compõe.
O Kafka é executado em forma de cluster, que pode ser executado em uma ou mais máquinas, armazenando os dados em categorias denominadas tópicos. As mensagens armazenadas são compostas por:

1. Uma chave (key); 
2. Um valor (value);
3. Um timestamp; 

O cluster pode ser composto por um ou mais tópicos, o que dependerá do contexto ao qual é aplicado.

Sua arquitetura pode ser definida por três módulos básicos, sendo eles:

1. Produtores (producers): Responsáveis por enviar mensagens ao cluster;
2. Tópicos (topics): Responsáveis por categorizar as mensagens dentro do cluster;
3. Consumidores (consumers): Responsáveis por receber as mensagens que estão clusterizadas.

É possível definir que apenas um consumer (ou um conjunto de consumers) acesse um topico (ou conjunto de tópicos) para consumir dados. Isso faz com que apenas partes interessadas acessem dados específicos, sem que todos os consumers tenham que acessar apenas um tópico e procurar por determinados dados. Os tês módulos citados possuem atributos específicos para configurações especiais, como o autocommit no consumer, que faz com que o consumer marque qual foi a última mensagem consumida. O autocommit permite que em execuções futuras, o consumer não consuma  os dados processados em execuçes anteriores.

## Executando Kafka em sua forma nativa:
Obs.: Este tutorial foi executado com a versão kafka_2.11-2.2.0

Inicialmente, acesse a página de [Download](https://kafka.apache.org/downloads) e baixe os binários da versão estável do Apache Kafka. Salve o pacote .tgz em um diretório de sua preferência, acesse-o e extraia o conteúdo.

Após o download e extração do conteúdo, acesse a pasta bin e execute:
```
./zookeeper-server-start.sh ../config/zookeeper.properties
```
(Obs.: caso dê erro do tipo "endereço já em uso", execute o comando ./zookeeper-server-stop.sh e reexecute o comando de start server.)

Este comando é responsável por iniciar o servidor zookeeper, responsável por gerenciar os nós dentro do cluster, partições, tópicos e afins. Após executá-lo, uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/prints/img_1.png) será mostrada.

Feito isso, ainda na pasta bin, em uma nova aba ou janela do terminal, é necessário iniciar os serviços Kafka:
```
./kafka-server-start.sh ../config/server.properties
```

Uma imagem semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/prints/img_2.png) será exibida.

O próximo passo é criar o tópico que receberá as mensagens enviadas pelo producer. Análogo ao passo anterior, em outra aba ou janela do terminal,  necessário executar:
 ```
 ./kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic <topic_name>
 ```
 
 É importante ressaltar que:
 1. localhost:9092 é referente ao ip da máquina onde o kafka está sendo executado, e 9092 é a porta utilizada pela aplicação;
 2. <topic_name> é o identificador do tópico e será utilizado por producers e consumers.

Após a execução do comando anterior, uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/prints/img_3_topic.png) será exibida.

Caso seja necessário criar vários tópicos, para listá-los use o comando:
```
./kafka-topics.sh --list --bootstrap-server localhost:9092
```

obs.: As janelas/abas relacionadas a criação e listagem dos tópicos são estáticas, dessa forma, não é necessário deixá-las abertas. Assim, após criar um tópico, você pode reusar a mesma janela/aba nos passos seguintes.

Por fim, para testar a configuração, é necessário iniciar o producer e o consumer. Em outra aba ou janela, é necessário executar o seguinte código:
```
./kafka-console-producer.sh --broker-list localhost:9092 --topic <topic_name>
```

Uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/prints/img_4_producer.png) será mostrada. Como percebido, o producer está a espera de mensagens para enviar ao cluster/tópico criado anteriormente. Já é possvel enviar mensagens, entretanto, não é possível visualizá-las pois o consumer ainda não foi iniciado, como visto na [imagem](https://github.com/luizgdias/kafka/blob/master/img_4_1_producer.png).

O último passo é relacionado a criação do consumer para a visualização das mensagens enviadas via consumer. Para iniciar uma instância de consumer, em uma nova aba ou janela do terminal, é necessário executar o seguinte código:
```
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic_name> --from-beginning
```

Essa linha de código mostrará todas as mensagens (do início do tópico até o fim), que estejam armazenadas no tópico <topic_name>, criado em passos iniciais. Como percebido nessa [imagem](https://github.com/luizgdias/kafka/blob/master/prints/img_5_consumer.png), a mensagem enviada ao tópico <topic_name>, foi acessada pelo consumer e continua disponível no tópico por um período padrão de sete dias (esse intervalo pode ser alterado), após esse intervalo, as mensagens do tópico são excluídas.

## Executando Kafka via containers docker

O processo de execução do Kafka via container é mais simplificada (pelo isolamento proporcionado pela conteinerização), mas segue os mesmos passos da versão nativa. O resultado dessa etapa são duas janelas/abas de terminal que se comunicam, uma janela/aba faz o papel de producer, e a outra de consumer. Para que isso seja possível são inicializados dois containers (zookeeper e kafka), e um tópico é criado, servindo de repositório.

O primeiro passo é executar os container zookeeper e kafka:
```
docker run -d --name zookeeper jplock/zookeeper:3.4.6
docker run -d --name kafka --link zookeeper:zookeeper ches/kafka

```

Se os comandos já foram executados antes, é provável que a tela seja semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/prints/img_1_container.png) imagem. Caso contrário o sistema realizará o download dos containers e suas dependências.

Após executá-los, é necessário exportar os ips dos containers:
obs: note que os próximos comandos utilizam os conteúdos das variáveis $ZK_IP e $KAFKA_IP, então antes de executar o comando que faz uso de uma das variáveis, exporte seus respectivos valores executando os comandos a seguir:
```
export ZK_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" zookeeper)
export KAFKA_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" kafka)

```

Opcional: Para visualizar o conteúdo das variáveis execute:
```
echo $ZK_IP
echo $KAFKA_IP
```

[Essa](https://github.com/luizgdias/kafka/blob/master/prints/img_2_container.png) imagem exemplifica a exportação e print dos ips dos containers.

Para criar tópicos:
```
docker run --rm ches/kafka kafka-topics.sh --create --topic <topic_name> --replication-factor 1 --partitions 1 --zookeeper $ZK_IP:2181

```

Para listar os tópicos do cluster:
```
docker run --rm ches/kafka kafka-topics.sh --list --zookeeper $ZK_IP:2181
```

Para criar o producer, executar:
```
docker run --rm --interactive ches/kafka kafka-console-producer.sh --topic <topic_name> --broker-list $KAFKA_IP:9092

```

O funcionamento do producer via container é o mesmo do producer nativo. O producer fica pronto para enviar a mensagem ao cluster/tópico, como visto [nessa](https://github.com/luizgdias/kafka/blob/master/prints/img_3_container_producer.png) imagem.

Para criar o consumer executar (em aba/janela diferentes dos containers em execução):
```
docker run --rm ches/kafka kafka-console-consumer.sh --topic <topic_name> --from-beginning --zookeeper $ZK_IP:2181
```
Da mesma forma que o consumer nativo, o consumer container permanece ouvindo o tópico e processando as mensagens de acordo com sua chegada, como mostrado [nessa](https://github.com/luizgdias/kafka/blob/master/prints/img_4_container_cons.png) imagem.

## Kafka-python API
Até agora vimos como realizar a troca de mensagens de forma simples, digitando mensagens no console do producer e enviado-as ao tópico. Percebemos que o tópico possui função de repositório, enquanto o producer é o agente ativo que envia as mensagens. Já o consumer é um agente passivo-reativo, que escuta as mensagens que chegam no tópico e as processa. 
Nessa seção será apresentada a API do kafka para a linguagem python. A API proporciona criar producers, tópicos e consumers de forma dinâmica com melhor nível de configuração, por meio da linguagem de programaço python.

O primeiro passo é instalar a API via pip ou pip3 install :
```bash
pip install kafka-python
```

Após a instalação, devem ser feitos alguns includes no arquivo .py que receberá o(s) producer(s) e/ou consumer(s):
```python
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from json import loads
```

(Obs: Assim como nos exemplos anteriores, é necessário primeiro, criar o(s) tópico(s) que receberão os dados dos producers presentes no script, logo o cluster deve ser configurado antes de enviar/receber dados.)

Após realizar a inserção dos includes no script, deve-se criar o producer (que é responsável por enviar os dados relevantes ao tópico):
```python
def send_to_kafka_topic(detections, topic_name):
        producer = KafkaProducer(   bootstrap_servers=[os.environ['kafka_host_url']], 
                                    api_version=(0,10,1), 
                                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                                )   
        producer.send(topic_name, detections)
        producer.flush()
```

O bloco de código anterior é um exemplo básico de uma função que recebe dois atributos e envia um deles via producer a um tópico. O primeiro parâmetro do construtor do producer é referente ao endereço do servidor, que deve ser correspondente ao ip:porta onde está sendo executado. O segundo parâmetro é a versão da api que está sendo utilizada, e por fim o terceiro serealiza o conteúdo a ser enviado em conteúdo json.

A linha producer.send() envia o conteúdo de 'detections' para o tópico 'topic_name', enquanto producer.flush() bloqueia qualquer requisição ao conteudo que está sendo enviado, até que ele seja de fato enviado ao tópico. A invocação desse método torna todos os registros armazenados em buffer imediatamente disponíveis para envio.

Até agora foi visto como enviar dados ao tópico via API, agora será mostrado como consumir dados de um tópico. O código abaixo exemplifica um modelo de consumer, que pode variar de acordo com os parâmetros configurados.

```python
def consumer_kafka_topic_messages(topic_name):
    consumer = KafkaConsumer(
                                topic_name,
                                bootstrap_servers=[os.environ['kafka_host_url']],
                                auto_offset_reset='earliest',
                                enable_auto_commit=True,
                                auto_commit_interval_ms=1000,
                                group_id = 'group_data_science'
                                value_deserializer=lambda x: loads(x.decode('utf-8'))
                            )

    for message in consumer:
        print(message.value)
    consumer.close()
```
A estrutura do consumer é similar a estrutura do producer, diferindo nos parâmetros recebidos na instanciação. Enquanto o producer prepara a mensagem para ser armazenada no tópico (convertendo-a em json), o consumer prepara a mensagem para ser consumida para processamento. A seguir são definidos alguns parâmetros:

- auto_offset_reset é relacionado a como as mensagens serão buscadas (earliest ou latest), ou seja, do início do tópico ao final, ou do final do tópico ao início; 
- enable_auto_commit é referente a sinalizar ou não as mensagens já consumidas (evitando que em execuçes futuras mensagens já processadas sejam reprocessadas);
- auto_commit_interval_ms é sobre o tempo de realização do auto commit;
- group_id está relacionado ao auto_commit e ao não consumo de dados processados. Dessa forma os apenas os consumidores que tiverem o mesmo group_id terão acesso ao conteúdo daquele tópico, e só consumirão os dados uma vez. Essa caracterstica é muito importante porque sem esses parâmetros, sempre que o consumer for invocado, todos os dados do tópico são reprocessados, tanto os novos dados quanto os antigos.

## Configurando .yml do container para enviar dados ao Kafka externo
Como visto no trecho de código do producer e do consumer, é utilizada uma variável não definida nas funções, a variável kafka_host_url:
```python
bootstrap_servers=[os.environ['kafka_host_url']]
```

Para que a função funcione normalmente, é necessário defini-la no arquivo .yml do container, utilizando o environment, como mostrado a seguir
```python
volumes:
      - '/path'
    image: 'name'
    extra_hosts:
      - 'host information'
    environment:
      kafka_host_url: xx.xxx.xxxx.xx:9092
```

O valor recebido pela variável kafka_host_url é referente ao ip e porta da máquina que receberá os dados enviados pelos producers definido dentro do container, bem como servirá os dados do tópico para os consumers.

## Instruções para comunicação de máquinas diferentes ao kafka isolado em um servidor
Para comunicação de diferentes máquinas, e o kafka isolado em um servidor, é necessário definir as portas da máquina que roda o kafka como portas públicas. Para isso execute:
```
sudo ufw allow 9092
sudo ufw allow 2181
```

Feito isso é necessário configurar no arquivo config/server.properties na linha 36, o endereço de adversed.listeners, para que os outros nós encontrem o cluster, produzam e consumam mensagens:
```
advertised.listeners=PLAINTEXT://<ip da maquina que roda o kafka>:9092
```

Após essas configurações, reiniciar o cluster.
Para mais informações sobre parâmetros de producer e consumer, consultar a documentação do Apache Kafka [neste](https://kafka.apache.org/) link.

## Instruções para configurar o Kafka em ambiente Kerberizado
O processo de configuração do Apache Kafka em ambiente que faz uso do protocolo de autenticação Kerberos (voltado a sistemas distribudos), é similar a configuração do Kafka em máquinas distintas, entretanto com arquivos adicionais. Neste exemplo ser demonstrado o passo a passo para a configuração de um container docker que envia dados a um servidor remoto kerberizado. Para que a comunicação nesse cenário seja possível, ambas as partes devem estar configuradas com o protocolo em questão. 

No processo de configuração é utilizada a biblioteca kafka-confluent disponível [neste](https://github.com/confluentinc/confluent-kafka-python) link que possui exemplos de producer e consumer, e pode ser instalada via pip:

```
pip install confluent-kafka
```

Após instalar a biblioteca confluent, é necessário realizar o download de uma segunda biblioteca responsável por realizar a comunicação entre o kafka e o kerberos, a biblioteca librdkafka disponível [neste](https://github.com/edenhill/librdkafka) link. Para este exemplo foi utilizada a versão 1.2.1.
