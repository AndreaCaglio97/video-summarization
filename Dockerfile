FROM python:3.8-slim as base

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

#Install the dependencies
RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN pip install --upgrade pip

RUN pip install torch==1.13.1+cpu torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cpu
# Install the dependencies
RUN pip install waitress
RUN pip install -r requirements.txt

# Copy the application code
COPY video_to_speech.py text_to_italian.py text_to_summary.py speech_to_text.py app.py ./

# Expose the port on which the application will run
EXPOSE 5000

# Start the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
