FROM python:3.7
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5005
CMD ["sh", "start.sh"]