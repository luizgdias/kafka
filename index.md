# Instruções para Execução - Apache Kafka

Este hands-on tem a finalidade de conceituar e demonstrar o funcionamento do Apache Kafka e Zookeeper, em sua forma nativa e via containers docker.

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
zookeeper-server-start.sh ../config/zookeeper.properties
```
Este comando é responsável por iniciar o servidor zookeeper, responsável por gerenciar os nós dentro do cluster, partições, tópicos e afins. Após executá-lo, uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/img_1.png) será mostrada.

Feito isso, ainda na pasta bin, em uma nova aba ou janela do terminal, é necessário iniciar os serviços Kafka:
```
kafka-server-start.sh ..config/server.properties
```

Uma imagem semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/img_2.png) será exibida.

O próximo passo é criar o tópico que receberá as mensagens enviadas pelo producer. Análogo ao passo anterior, em outra aba ou janela do terminal,  necessário executar:
 ```
 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic <topic_name>
 ```
 
 É importante ressaltar que:
 1. localhost:9092 é referente ao ip da máquina onde o kafka está sendo executado, e 9092 é a porta utilizada pela aplicação;
 2. <topic_name> é o identificador do tópico e será utilizado por producers e consumers.

Após a execução do comando anterior, uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/img_3_topic.png) será exibida.

Caso seja necessário criar vários tópicos, para listá-los use o comando:
```
kafka-topics.sh --list --bootstrap-server localhost:9092
```

obs.: As janelas/abas relacionadas a criação e listagem dos tópicos são estáticas, dessa forma, não é necessário deixá-las abertas. Assim, após criar um tópico, você pode reusar a mesma janela/aba nos passos seguintes.

Por fim, para testar a configuração, é necessário iniciar o producer e o consumer. Em outra aba ou janela, é necessário executar o seguinte código:
```
kafka-console-producer.sh --broker-list localhost:9092 --topic <topic_name>
```

Uma tela semelhante a [essa](https://github.com/luizgdias/kafka/blob/master/img_4_producer.png) será mostrada. Como percebido, o producer está a espera de mensagens para enviar ao cluster/tópico criado anteriormente. Já é possvel enviar mensagens, entretanto, não é possível visualizá-las pois o consumer ainda não foi iniciado, como visto na [imagem](https://github.com/luizgdias/kafka/blob/master/img_4_1_producer.png).

O último passo é relacionado a criação do consumer para a visualização das mensagens enviadas via consumer. Para iniciar uma instância de consumer, em uma nova aba ou janela do terminal, é necessário executar o seguinte código:
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic_name> --from-beginning
```

Essa linha de cdigo mostrará todas as mensagens (do início do tópico até o fim), que estejam armazenadas no tópico <topic_name>, criado em passos iniciais. Como percebido nessa [imagem](https://github.com/luizgdias/kafka/blob/master/img_5_consumer.png), a mensagem enviada ao tópico <topic_name>, foi acessada pelo consumer e continua disponível no tópico por um período padrão de sete dias (esse intervalo pode ser alterado), após esse intervalo, as mensagens do tópico são excluídas.

## Executando Kafka via containers docker

O processo de execução do Kafka via container é mais simplificada (pelo isolamento proporcionado pela conteinerização), mas segue os mesmos passos da versão nativa.

O primeiro passo é executar os container zookeeper e kafka:

```
docker run -d --name zookeeper jplock/zookeeper:3.4.6
docker run -d --name kafka --link zookeeper:zookeeper ches/kafka

```
Após executá-los, é necessário exportar os ips dos containers:
obs: note que os próximos comandos utilizam os conteúdos das variáveis $ZK_IP e $KAFKA_IP, então antes de executar o comando que faz uso de uma das variáveis, exporte seus respectivos valores.

```
export ZK_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" zookeeper)
export KAFKA_IP=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" kafka)

```
Opcional: Para visualizar o conteúdo dos ips:
```
echo $ZK_IP
echo $KAFKA_IP
```

Para criar tópicos:
```
docker run --rm ches/kafka kafka-topics.sh --create --topic <topic_name> --replication-factor 1 --partitions 1 --zookeeper $ZK_IP:2181

```


Para listar os tópicos do cluster:
```
docker run --rm ches/kafka kafka-topics.sh --list --zookeeper $ZK_IP:2181
```

Para criar o consumer, executar:
```
docker run --rm --interactive ches/kafka kafka-console-producer.sh --topic <topic_name> --broker-list $KAFKA_IP:9092

```

Para criar o consumer executar (em aba/janela diferentes):
```
docker run --rm ches/kafka kafka-console-consumer.sh --topic <topic_name> --from-beginning --zookeeper $ZK_IP:2181
```

