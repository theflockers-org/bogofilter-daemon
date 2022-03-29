all: build
build:
	rpmbuild -ba bogofilter-daemon.spec
