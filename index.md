## Instruções para Execução - Apache Kafka

Este hands-on tem a finalidade de explicar conceitos e demonstrar o funcionamento do Apache Kafka e Zookeeper, em sua forma nativa e via containers docker.

### O que é o Apache Kafka?
O Apache Kafka é uma aplicação utilizada no desenvolvimento de pipelines de tempo real e streamming. Suas principais caractersticas são: escalabilidade, tolerância a falhas, e velocidade na troca de mensagens entre os módulos que o compõe.
O Kafka é executado em forma de cluster, que pode ser executado em uma ou mais máquinas, armazenando os dados em categorias denominadas tópicos. As mensagens armazenadas são compostas por:

1. Uma chave (key); 
2. Um valor (value);
3. Um timestamp; 

O cluster pode ser composto por um ou mais tópicos, o que dependerá do contexto ao qual é aplicado.

Sua arquitetura é pode ser definida por três módulos básicos, sendo eles:

1. Produtores (producers): Responsáveis por enviar mensagens ao cluster;
2. Tópicos (topics): Responsáveis por categorizar as mensagens dentro do cluster;
3. Consumidores (consumers): Responsáveis por receber as mensagens que estão clusterizadas.

É possível definir um tópico específico para que um determinado consumer acesse e consuma os dados armazenados nele. Os tês módulos citados possuiem atributos específicos para configurações especiais, como o autocommit no consumer, que faz com que o consumer marque qual foi a última mensagem consumida. O autocommit permite que em execuções futuras, o consumer não consuma  os dados processados em execuçes anteriores.

### Executando Kafka em sua forma nativa:

Inicialmente, acesse a página de [Download](https://kafka.apache.org/downloads) e baixe os binários da versão estável do Apache Kafka. Salve o pacote .tgz em um diretório de sua preferência, acesse-o e extraia o conteúdo.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/luizgdias/kafka/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
