FROM python:3.7-alpine
COPY . /src
WORKDIR /src

# Because pycurl is fussy.

ENV PYCURL_SSL_LIBRARY=openssl

# Loads all dependencies

RUN apk add --no-cache --virtual .build-dependencies
RUN apk add --update py-pip
RUN apk add --no-cache libcurl
RUN apk --no-cache add curl
# urlLib3 and requests are not used in assignment.
# left them in because I am currently playing around with them
RUN apk add --no-cache --virtual .build-dependencies build-base curl-dev \
    && pip install pycurl \
    && pip install urllib3 \    
    && pip install requests \
    && apk del .build-dependencies

#Uncomment just the next 2  lines to run your application in Docker container
EXPOSE 8080
CMD python server3.py 8080


#Uncomment just the next line when you want to deploy your container on Heroku
# CMD python server3.py $PORT