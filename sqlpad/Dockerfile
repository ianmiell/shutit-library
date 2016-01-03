FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y -qq git python-pip
RUN pip install shutit

EXPOSE 9010:3000

WORKDIR /opt
# Change the next two lines to build your ShutIt module.
RUN git clone https://github.com/ianmiell/shutit-library
WORKDIR /opt/shutit-library/sqlpad
RUN shutit build --delivery dockerfile -m ../nodejs

VOLUME /var/land_registry/var/lib/sqlpad:/var/lib/sqlpad

CMD ["sqlpad","--port","3000","--dir","/var/lib/sqlpad"]
