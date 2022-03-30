name=bogofilter-daemon
version=0.2
builddir=~/build

all: build

build:
	cp bogofilter-daemon.{py,conf,spec} ${builddir}/SOURCES/
	rpmbuild -b bogofilter-daemon.spec --define "_sourcedir $(shell pwd)"
