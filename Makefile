name=bogofilter-daemon
version=0.2

all: compress build
compress:
	mkdir -p SOURCES/
	tar cjf SOURCES/${name}-${version}.tar.bz2 --exclude=.git . 
build:
	rpmbuild -ba bogofilter-daemon.spec
