FROM coady/pylucene:9.12.0
WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py", "/app/store/page", "--limit", "10"]