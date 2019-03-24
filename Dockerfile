FROM python:3.6
EXPOSE 80
COPY . .
WORKDIR app
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=/app/main.py
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=80"]
