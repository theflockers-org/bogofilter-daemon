name=bogofilter-daemon
version=0.2
builddir=~/build

all: build

build:
	rpmbuild -ba bogofilter-daemon.spec --define "_sourcedir $(shell pwd)"
