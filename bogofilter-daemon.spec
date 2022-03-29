Name:           bogofilter-daemon 
Version:        0.2
Release:        1
Summary:        Python Bogofilter Daemon
Group:          System Environment/Base
License:        GPLv2+
Source0:        bogofilter-daemon.py 
Source1:        bogofilter-daemon.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:       python2.6 >= 2.6.4-5.yos
Requires:       bogofilter >= 1.2.1

%description
Bogofilter Daemon is a daemon wrapper to bogofilter in STDIN mode.

It opens max_procs instances of bogofilter in STDIN mode and escales 
the inputs for each instance.

%prep
#%setup -c -n %{name}-%{version} -T 

%install
%{__rm} -fr $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/usr/sbin
%{__mkdir} -p $RPM_BUILD_ROOT/etc
%{__install} -Dp -m0755 %{SOURCE0} $RPM_BUILD_ROOT/usr/sbin
%{__install} -Dp -m0644 %{SOURCE1} $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/sbin/bogofilter-daemon.py
/etc/bogofilter-daemon.conf

%changelog
* Thu Nov 01 2010 Leandro Mendes <leandro.mendes@locaweb.com.br> 0.2-1
- Adding config file support 

* Thu Jul 22 2010 Leandro Mendes <leandro.mendes@locaweb.com.br> 0.1-1
- first release
