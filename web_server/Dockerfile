# Use the official Python image as base
FROM python:3.9-slim

# Install fluidsynth
RUN apt-get update && apt-get install -y fluidsynth

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask server using Waitress
CMD ["waitress-serve", "--host", "0.0.0.0", "--port=5000", "--call", "app_server:create_app"]
