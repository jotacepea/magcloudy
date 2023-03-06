FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . . 

EXPOSE 8501

CMD python3 -m streamlit run main.py
