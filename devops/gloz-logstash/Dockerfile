FROM docker.elastic.co/logstash/logstash:8.1.0
# RUN apt-get update & apt-get install -y vim
RUN rm -f /usr/share/logstash/config/pipelines.yml
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN rm -f /usr/share/logstash/config/logstash.yml
ADD postgresql-42.3.3.jar /usr/share/logstash/logstash-core/lib/jars/
ADD ./pipeline/ /usr/share/logstash/pipeline/
ADD ./config/ /usr/share/logstash/config/