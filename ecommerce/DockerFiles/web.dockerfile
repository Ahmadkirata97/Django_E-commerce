# Download The Base Image 
FROM  nginx:latest

# Update Repos and install vim 
RUN apt-get update && apt install -y vim 

# Remove Default files
# RUN rm /etc/nginx/nginx.conf
# RUN rm /etc/nginx/conf.d/default.conf

# Copy Nginx Configuration File Into Container
# COPY ./DockerFiles/nginx.conf /etc/nginx/
# COPY ./DockerFiles/default.conf /etc/nginx/conf.d/default.conf
# COPY --from=app /Static /usr/share/nginx/html

# Expose Port
EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]