FROM python:latest

WORKDIR ./
COPY token token
COPY gcpNestRead.py nestRead.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
#COPY . .

CMD ["python", "nestRead.py", "-i" , "token"]
#CMD ["sleep", "infinity"]
