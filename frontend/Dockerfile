FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . . 

EXPOSE 8501
ENV STR_PUB_WEB_PORT='8888'

CMD python3 -m streamlit run main.py --server.port 8501 --server.address '0.0.0.0' --browser.serverAddress 'localhost' --browser.serverPort ${STR_PUB_WEB_PORT}
