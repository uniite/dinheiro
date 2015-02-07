FROM debian:7

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y build-essential curl git gnupg libffi-dev libmysqlclient-dev python2.7-dev python-pip

# Install libsodium
RUN mkdir build
RUN cd build && curl -O https://download.libsodium.org/libsodium/releases/libsodium-1.0.2.tar.gz
RUN cd build && sha256sum libsodium-1.0.2.tar.gz | grep 961d8f10047f545ae658bcc73b8ab0bf2c312ac945968dd579d87c768e5baa19
RUN cd build && tar xzfv libsodium-1.0.2.tar.gz
RUN cd build/libsodium-1.0.2 && ./configure && make && make check && make install
RUN rm -rf build

# Install tedious compiled libs for python
RUN apt-get install -y python-numpy python-pandas-lib

# Copy the requirements file early so we have a cached copy of the python libs
ADD requirements/ /requirements
RUN pip install -r requirements/production.txt

# Copy the app, and remove extra files (.pyc, etc.)
ADD . /app
RUN cd app && git clean -xfd && rm -rf .git

ENV DJANGO_SETTINGS_MODULE dinheiro.settings.production

EXPOSE 9090
WORKDIR /app
CMD uwsgi --http :9090 --uid nobody --gid nogroup --wsgi-file dinheiro/wsgi.py --master --processes 4 --threads 1
