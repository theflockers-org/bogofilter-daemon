name=bogofilter-daemon
version=0.2

all: compress build
compress:
	mkdir -p rpmbuild/ SOURCES/
	tar cjf SOURCES/${name}-${version}.tar.bz2 --exclude=.git . 
build:
	ls
	pwd
	rpmbuild -ba bogofilter-daemon.spec --define "_topdir ./rpmbuild" --define "_sourcedir ./SOURCES"
