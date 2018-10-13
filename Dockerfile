FROM tiangolo/uwsgi-nginx-flask:python3.6
EXPOSE 80
RUN git clone https://gitlab.com/czhanacek/smart-home-security-system-backend
RUN pip install pipenv
RUN pipenv install --skip-lock 
ENV FLASK_APP=app/app.py
CMD ["flask", "run"]