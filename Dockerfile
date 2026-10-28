FROM python:3.12-slim
WORKDIR /app
COPY req.txt .
RUN pip install -r req.txt
COPY app.py . 
EXPOSE 5000
CMD ["python","app.py"]