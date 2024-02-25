FROM ubuntu:23.10

# Args
ARG EXPOSE_PORT=8000
EXPOSE $EXPOSE_PORT/tcp
ARG PYTHON_VERSION=3.10.12
ARG CONDA_DIR=/opt/conda
USER root

# install requirements libarary
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends
RUN apt-get install -y python3-dev python3-pip && apt install curl -y
# RUN apt-get update && apt-get install libgl1-mesa-glx -y 
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# install python
SHELL ["/bin/bash", "-c"]
RUN curl -o ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ${CONDA_DIR} && \
    rm ~/miniconda.sh && \
    ${CONDA_DIR}/bin/conda install -y python=${PYTHON_VERSION} && \
    ${CONDA_DIR}/bin/conda clean -ya
ENV PATH ${CONDA_DIR}/bin:${PATH}

SHELL ["/bin/bash", "-c"]
RUN mkdir /home/user
ENV HOME_PATH=/home/user
ARG APP_NAME=artapi-fastapi
ARG MODULE_PATH=${HOME_PATH}/${APP_NAME}
WORKDIR ${MODULE_PATH}

# setting src
COPY main.py ${MODULE_PATH}/main.py
COPY src ${MODULE_PATH}/src
COPY requirements.txt ${MODULE_PATH}/requirements.txt
COPY entrypoint.sh ${MODULE_PATH}/entrypoint.sh

RUN chmod 755 ${MODULE_PATH}/entrypoint.sh
RUN chmod +x ${MODULE_PATH}/entrypoint.sh

EXPOSE ${EXPOSE_PORT}
RUN cd ${MODULE_PATH}

CMD ["sh", "/home/user/artapi-fastapi/entrypoint.sh"]