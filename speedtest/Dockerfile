FROM alpine:latest

WORKDIR ./
COPY resolv.conf /etc/resolv.conf

RUN apk update
RUN apk add bind-tools
RUN apk add speedtest-cli

RUN crontab -l > /tmp/out
RUN echo "*/5 * * * * speedtest-cli --json" >> /tmp/out
RUN crontab - < /tmp/out

CMD ["crond", "-f" ]
