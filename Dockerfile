FROM python:3.6-alpine3.9

ENV PYTHONUNBUFFERED=0

#Install C Depedencies
RUN sh -c 'apk add --update curl gcc g++ bash libffi-dev libffi openssl-dev make && rm -rf /var/cache/apk/*'

#Install Python Libraries
COPY requirements.txt /home/requirements.txt
RUN pip3 install --requirement /home/requirements.txt

# Copy Files
COPY . /etc/backup/
WORKDIR /etc/backup/

CMD ["python", "run.py"]