FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
ENV APP_COLOR=blue
CMD ["python", "app.py"]
