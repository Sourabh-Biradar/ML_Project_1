FROM python:3.13.0-slim

WORKDIR /app

COPY . /app

RUN apt update -y
RUN apt install awscli -y

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# from streamlit