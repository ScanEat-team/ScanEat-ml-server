FROM python:3.10-slim
RUN apt-get update && apt-get install -y libzbar0
WORKDIR /app
ENV PORT 8080
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "main.py"]
