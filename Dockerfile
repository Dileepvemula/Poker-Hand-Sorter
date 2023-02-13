# Use the same version of python as dev
FROM python:3.10.10-alpine

# Label the version of this image
LABEL version="1.0.0"

# Add the app dir to python path
ENV PYTHONPATH "$(PYTHONPATH) : /app"

# Install dependancies
RUN apk update && apk add gnupg nano

# Copy in the python application and install it
WORKDIR /app
COPY . .
RUN pip install -r requirements. txt

# Setup the main workdir as the config dir
WORKDIR /config

# Run the commad based on the env variables
CMD python -m poker_sorter

