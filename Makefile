name=bogofilter-daemon
version=0.2
rpmbuilddir=~/rpmbuild

all: compress build
compress:
	mkdir ${rpmbuilddir}/SOURCES
	tar cjf ${rpmbuilddir}/SOURCES/${name}-${version}.tar.bz2 --exclude=.git .
build:
	rpmbuild -ba bogofilter-daemon.spec
