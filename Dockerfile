FROM tiangolo/uwsgi-nginx-flask:python3.6
EXPOSE 80
RUN git clone https://github.com/czhanacek/alexa-spelling
RUN pip install pipenv
RUN pipenv install --skip-lock 
RUN export FLASK_APP=app.py
CMD ["flask", "run"]