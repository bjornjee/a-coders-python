FROM python:3.8.5
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
COPY Scrapper.py /app
COPY Server.py /app
COPY ticker.csv /app
RUN pip install -r requirements.txt --trusted-host pypi.python.org
EXPOSE 5000
ENTRYPOINT ["python","Server.py", "./ticker.csv"]
