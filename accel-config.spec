Summary:	Configure accelerator subsystem devices
Summary(pl.UTF-8):	Konfiguracja urządzeń podsystemu akceleracji
Name:		accel-config
Version:	4.1.8
Release:	1
License:	GPL v2
Group:		Applications/System
#Source0Download: https://github.com/intel/idxd-config/releases (accel-config- tags)
Source0:	https://github.com/intel/idxd-config/archive/%{name}-v%{version}/idxd-config-%{name}-v%{version}.tar.gz
# Source0-md5:	261d7673da88d1b14a44020ea645ce43
URL:		https://github.com/intel/idxd-config
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	json-c-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	xmlto
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utility library for controlling and configuring DSA (Intel(R) Data
Streaming Accelerator Architecture) and IAA (Intel(R) Analytics
Accelerator Architecture) sub-systems in the Linux kernel.

%description -l pl.UTF-8
Biblioteka narzędziowa do sterowania i konfiguracji podsystemów DSA
(Intel(R) Data Streaming Accelerator Architecture) and IAA (Intel(R)
Analytics Accelerator Architecture) w jądrze Linuksa.

%package libs
Summary:	Library to configure accfg subsystem devices
Summary(pl.UTF-8):	Biblioteka do konfiguracji podsystemu accfg
License:	LGPL v2.1
Group:		Libraries

%description libs
Library to configure accfg subsystem devices.

%description libs -l pl.UTF-8
Biblioteka do konfiguracji podsystemu accfg.

%package devel
Summary:	Header files for accel-config library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki accel-config
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for accel-config library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki accel-config.

%prep
%setup -q -n idxd-config-%{name}-v%{version}

%build
./git-version-gen
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-bash-completion-dir=%{bash_compdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccel-config.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc licenses/accel-config-licenses
%attr(755,root,root) %{_bindir}/accel-config
%dir %{_sysconfdir}/accel-config
%dir %{_sysconfdir}/accel-config/contrib
%dir %{_sysconfdir}/accel-config/contrib/configs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-config/contrib/configs/app_profile.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-config/contrib/configs/net_profile.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-config/contrib/configs/os_profile.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-config/contrib/configs/storage_profile.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/accel-config/contrib/configs/user_default_profile.conf
%doc %{_sysconfdir}/accel-config/contrib/configs/profilenote.txt
%{_mandir}/man1/accel-config.1*
%{_mandir}/man1/accel-config-*.1*

%files libs
%defattr(644,root,root,755)
%doc README.md SECURITY.md TODO licenses/{BSD-MIT,CC0,libaccel-config-licenses}
%attr(755,root,root) %{_libdir}/libaccel-config.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccel-config.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccel-config.so
%{_includedir}/accel-config
%{_pkgconfigdir}/libaccel-config.pc
