FROM python:3.11-alpine
WORKDIR /studygroup
COPY requirements.txt /studygroup/
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8002
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}

CMD ["uvicorn", "app.main:app", "--reload", "--host","0.0.0.0", "--port", "8002"]
