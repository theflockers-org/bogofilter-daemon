name=bogofilter-daemon
version=0.2

all: build

build:
	rpmbuild -ba bogofilter-daemon.spec --define "_sourcedir $(pwd)"
