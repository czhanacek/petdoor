FROM python:3.6
EXPOSE 5000
RUN git clone https://gitlab.com/czhanacek/smart-home-security-system-backend /smartsec
WORKDIR /smartsec
RUN pip install pipenv
RUN pipenv install
ENV FLASK_APP=/smartsec/app/main.py
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=80"]