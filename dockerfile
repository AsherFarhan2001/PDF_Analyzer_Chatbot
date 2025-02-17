# select docker image of uvicorn-gunicorn-fastapi with python 3.10
# By default this image runs gunicorn on port 80 and with uvicorn.workers.UvicornWorker
# By default max workers are unlimited
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

#Set the working directory in the container
WORKDIR /app

# copy requirements to app directory
COPY ./requirements.txt /app/requirements.txt

# install requirements with no cache
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy code
COPY ./app /app

# Expose the port your application runs on
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



#Instructions for Running the FastAPI application in a Docker container
# Build the Docker image
# 1. docker build -t chatbot-app . 

# Run the Docker container
#2. docker run -d -p 8000:8000 -e OPENAI_API_KEY="" -e PINECONE_API_KEY="" chatbot-app

#3. Make sure the container is running. Go to the following Url in browser
    #http://localhost:8000/chatbot/
