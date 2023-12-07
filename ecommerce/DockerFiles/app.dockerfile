# Download Base Image 
FROM python:latest

RUN apt-get update && apt-get install -y vim

# Set the Working directory in the container 

# Copy the requirements File into the container 
COPY ./ecommerce/requirements.txt .

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the django project code into the container 
COPY . .
COPY ./ecommerce/.env .

# Remove Unneeded Directories
RUN mv ecommerce/DockerFiles/app.sh .
RUN rm -r ecommerce/DockerFiles
RUN rm ecommerce/docker-compose.yml

# Expose Port 
EXPOSE 8000
WORKDIR /ecommerce

ENTRYPOINT [ "app.sh" ]

CMD [ "python", "manage.py", "runserver" ]
