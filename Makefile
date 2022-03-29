name=bogofilter-daemon
version=0.2

all: build

build:
	cp bogofilter-daemon.{py,conf,spec} $(shell pwd)/build/SOURCES/
	rpmbuild -ba bogofilter-daemon.spec --define "_sourcedir $(shell pwd)"
