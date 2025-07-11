FROM python:3.11.13

RUN echo ls
WORKDIR /app
RUN echo ls

COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --no-deps -r requirements.txt && \
    pip cache purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



COPY . .


#CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py