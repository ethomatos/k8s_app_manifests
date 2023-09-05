/usr/bin/sensors -j | /usr/bin/tr -d '\n' | sed 's/\}$//' > /tmp/out

/usr/bin/echo ", \"ddsource\":\"crontab\", \"ddtags\":\"env:dev,version:0\", \"hostname\":\"elitedesk\", \"service\":\"cputemp\" }" >> /tmp/out

curl -X POST "https://http-intake.logs.datadoghq.eu/api/v2/logs" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-d @- < /tmp/out

