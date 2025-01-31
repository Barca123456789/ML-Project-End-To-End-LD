# Use a specific version of the Python image
FROM python:3.12.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app using gunicorn (make sure the app.py is in the correct location and contains 'app:app')
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]



