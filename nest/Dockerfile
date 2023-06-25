FROM python:latest

WORKDIR ./
COPY token token
COPY nestRead.py nestRead.py
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
#COPY . .

CMD ["python", "nestRead.py", "-i" , "token"]
#CMD ["ddtrace-run", "python", "nestRead.py", "token"]
#CMD ["sleep", "infinity"]
