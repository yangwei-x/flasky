FROM python:3.12-alpine

ENV FLASK_APP=flasky.py
ENV FLASK_CONFIG=production

# Install Python dependencies as root first
WORKDIR /home/flasky
COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements/docker.txt

# Now create user and switch
RUN adduser -D flasky

# Copy application files as root and set permissions
COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# Make boot.sh executable and set ownership
RUN chmod +x boot.sh
RUN chown -R flasky:flasky /home/flasky

USER flasky

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
