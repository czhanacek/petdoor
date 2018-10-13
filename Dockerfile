FROM tiangolo/uwsgi-nginx:python3.6
EXPOSE 80
ENV UWSGI_INI /app/uwsgi.ini
RUN git clone https://gitlab.com/czhanacek/smart-home-security-system-backend /app
WORKDIR smart-home-security-system-backend
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=app/main.py

ENV LISTEN_PORT 80

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app/app

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/usr/bin/supervisord"]