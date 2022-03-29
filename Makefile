name=bogofilter-daemon
version=0.2
rpmbuilddir=~/build

all: compress build
compress:
	tar cjf ${rpmbuilddir}/SOURCES/${name}-${version}.tar.bz2 --exclude=.git .
build:
	rpmbuild -ba bogofilter-daemon.spec
