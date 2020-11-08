FROM node:12.13.0

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN npm install -g @angular/cli@latest

COPY . /usr/src/app

RUN cd /usr/src/app

RUN ls -l

CMD ng update --all --force

CMD ng serve --host 0.0.0.0 --port 4500
