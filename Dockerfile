FROM tiangolo/uwsgi-nginx-flask:python3.6
EXPOSE 80
RUN git clone https://gitlab.com/czhanacek/smart-home-security-system-backend
COPY smart-home-security-system-backend/app/* /app/*
WORKDIR /app
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=app/main.py