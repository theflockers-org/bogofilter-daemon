name=bogofilter-daemon
version=0.2
builddir=~/build

all: build

build:
	cp ./SOURCES/${name}-${version}.tar.gz ${builddir}/SOURCES/
	#rpmbuild -ba bogofilter-daemon.spec --define "_sourcedir $(shell pwd)"
