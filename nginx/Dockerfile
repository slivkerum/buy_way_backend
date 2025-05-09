FROM nginx:1.16.0
ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8080

COPY ./ ./

ARG CONFIG_FILE
ARG actually_conf_file=${CONFIG_FILE:-'nginx.conf'}
RUN cp $actually_conf_file /etc/nginx/nginx.conf
