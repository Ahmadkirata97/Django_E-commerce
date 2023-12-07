# Download BaseImage
FROM postgres:latest

RUN apt-get update && apt-get install -y \
    systemd\
    iputils-ping\
    vim

# Set the Env Variables for the DB
ENV POSTGRES_USER=postgre
ENV POSTGRES_PASSWORD=0938460904am
ENV POSTGRES_DB=ecommerceDB

# Copy the initialization Script into the container
# COPY init.sql docker-entrypoint-initdb.d/

# Expose Port
EXPOSE 5432

# ENTRYPOINT [ "docker-entrypoint-initdb.d/init.sql" ]