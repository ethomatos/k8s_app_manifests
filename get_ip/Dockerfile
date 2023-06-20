FROM alpine:latest

RUN apk update

RUN apk add bind-tools

RUN crontab -l > /tmp/out
RUN echo "*/1 * * * * dig +short myip.opendns.com @resolver1.opendns.com" >> /tmp/out
RUN crontab - < /tmp/out

CMD ["crond", "-f" ]
