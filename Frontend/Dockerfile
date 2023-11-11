FROM python:3.9-slim

RUN apt update && apt install python3-pip -y

WORKDIR /home/app

COPY quality.png lightning-talk-demo.mp4 ./

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
