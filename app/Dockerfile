FROM python:3.6.8

ENV DEBIAN_FRONTEND=noninteractive

# Set user to root, to prevent any permission problems:)
USER root
# Workdir to app folder
WORKDIR /app

# Install dependencies
RUN apt-get -y update && apt-get -y install wget && \
    apt-get install -y apt-utils && \
    apt-get install -y build-essential && \
    apt-get install -y python3-dev && \
    apt-get install -y libssl-dev && \
    apt-get install -y swig && \
    apt-get install -y ffmpeg
    
RUN pip install protobuf==3.19.5 cryptography==36.0.2
RUN pip install --user --no-warn-script-location awscli==1.16.108 boto==2.49.0 boto3==1.9.99 botocore==1.12.99 ipython

# Will be used later for storing the data.
ENV DATA_DIR=/opt/data
RUN mkdir -p ${DATA_DIR}
    
# All all code in current folder to app directory in the image
ADD  . /app

# Expose a port for testing
EXPOSE 8009

# Add bins to path
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/bento4/bin:${PATH}

# Temp command to test
CMD echo 'hello world'
