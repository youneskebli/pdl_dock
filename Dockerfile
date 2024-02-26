FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libgl1-mesa-glx libgomp1 libxrender1 libxext-dev

RUN pip install --no-cache-dir protobuf==3.20.0 paddlepaddle -U openai==0.28

RUN pip install --no-cache-dir pinecone-client
RUN pip install --no-cache-dir python-dotenv
RUN pip install transformers torch
RUN pip install --no-cache-dir opencv-python \
    paddleocr \
    flask \
    flask-cors \
    paddleclas \
    faiss-cpu  # Use CPU version of faiss, appropriate for the Docker container environment.

RUN pip install --no-cache-dir sentence_transformers

# Install Langchain
RUN pip install --no-cache-dir  langchain tiktoken
RUN pip install transformers torch unstructured unstructured[local-inference]
RUN pip install detectron2@git+https://github.com/facebookresearch/detectron2.git@v0.6#egg=detectron2
RUN apt-get install -y poppler-utils
RUN pip install Pillow==8.2.0 streamlit
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

WORKDIR /app

COPY . /app

EXPOSE 5000

CMD ["python","app.py"]