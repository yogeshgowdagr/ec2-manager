FROM python:3.9.18-slim

RUN pip install Flask boto3


COPY  app.py /app/.
COPY  templates/index.html /app/templates/. 
COPY  static/style.css /app/static/. 

WORKDIR /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"] 
