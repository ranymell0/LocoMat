FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY locomat ./locomat
ENV LOCOMAT_DB=/data/locomat.db
VOLUME /data
EXPOSE 5000
CMD ["flask", "--app", "locomat", "run", "--host", "0.0.0.0", "--port", "5000"]
