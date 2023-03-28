# Base image
FROM pytorch/pytorch:latest

# Set the working directory
WORKDIR /app

#Install the dependencies
RUN apt-get -y update
RUN apt-get install -y ffmpeg

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install waitress
RUN pip install -r requirements.txt

# Copy the application code
COPY video_to_speech.py text_to_italian.py text_to_summary.py speech_to_text.py app.py ./

# Expose the port on which the application will run
EXPOSE 5000

# Start the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
