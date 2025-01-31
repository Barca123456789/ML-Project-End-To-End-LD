FROM python:3.12.7  # Use the correct Python version

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip  # Optionally upgrade pip to avoid any issues with older versions
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]


