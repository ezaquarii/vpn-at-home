FROM ubuntu:18.04 AS builder
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes \
	apt-utils \
	build-essential \
	debhelper \
	devscripts \
	dh-virtualenv \
	make \
	python3 \
	python3-dev \
	python3-wheel \
	python3-venv \
	sudo
COPY . /build
WORKDIR /build
RUN make deb DOCKER_BUILD=true


FROM ubuntu:18.04 AS runner
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes \
	ansible \
	dialog \
	libpython3.6 \
	openssh-client \
	openssl \
	openvpn \
	python3-distutils
COPY --from=builder /vpnathome*.deb /
RUN dpkg -i /vpnathome*.deb
EXPOSE 8000
VOLUME "/srv/vpnathome/data"
