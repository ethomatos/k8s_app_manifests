FROM alpine:latest

RUN apk update
RUN apk add lm-sensors

RUN crontab -l > /tmp/out
RUN echo "*/1 * * * * /usr/bin/sensors -j | /usr/bin/tr -d '\n'" >> /tmp/out
RUN crontab - < /tmp/out

CMD ["crond", "-f" ]
