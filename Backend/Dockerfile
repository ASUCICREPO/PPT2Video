FROM python:3.9-slim

RUN useradd -ms /bin/bash ubuntu
USER ubuntu
ENV DEBIAN_FRONTEND=noninteractive

# Downloading sys packages
USER root
RUN apt update -y && apt upgrade -y && apt install python3-pip libreoffice poppler-utils ffmpeg awscli git -y 
RUN python3 -m pip install --upgrade pip

# Installing all dependencies
USER ubuntu
RUN mkdir -p /home/ubuntu/app
WORKDIR /home/ubuntu/app
COPY app/requirements.txt .
RUN pip install -r requirements.txt && mkdir audio-vtt slides pptx output slide-videos
RUN git clone https://github.com/aws-samples/amazon-polly-closed-caption-subtitle-generator.git
WORKDIR amazon-polly-closed-caption-subtitle-generator
RUN pip install .

# Copying all the Code and necessary files
WORKDIR /home/ubuntu
RUN mkdir -p /home/ubuntu/.aws
COPY config /home/ubuntu/.aws/
#COPY entrypoint.sh ./app/
RUN export PATH=/usr/bin/libreoffice:$PATH
COPY app/PPT-MP4-Convertor-EN.py ./app/



# Modifying all permissions
USER root
RUN chmod 755 ./app/PPT-MP4-Convertor-EN.py
RUN chown -R ubuntu:ubuntu .aws && chown -R ubuntu:ubuntu ./app/PPT-MP4-Convertor-EN.py && chown -R ubuntu:ubuntu ./app/requirements.txt
# && chown -R ubuntu:ubuntu ./app/entrypoint.sh


# Running Flask Server
USER ubuntu
#RUN chmod +777 ./app/entrypoint.sh
WORKDIR /home/ubuntu/app
EXPOSE 5000
#ENTRYPOINT [ "./entrypoint.sh" ]
CMD [ "python3", "PPT-MP4-Convertor-EN.py"]