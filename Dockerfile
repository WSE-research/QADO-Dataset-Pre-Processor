FROM python:alpine
COPY requirements.txt /requirements.txt
COPY app.py /app.py
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn -b 0.0.0.0:5000 -w 4 app:app