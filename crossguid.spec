#
# Conditional build:
%bcond_without	tests		# build without tests

%define rel 1
%define short_commit ca1bf4b
%define commit_date 20190529
Summary:	Lightweight cross platform C++ GUID/UUID library
Name:		crossguid
Version:	0.2.3
Release:	0.%{commit_date}.%{rel}
License:	MIT
Group:		Libraries
Source0:	https://github.com/graeme-hill/crossguid/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz
# Source0-md5:	d4a8d62f3f8d6d946be75cf5bfa92687
Patch0:		includes.patch
Patch1:		cmake-config-dir.patch
URL:		https://github.com/graeme-hill/crossguid/
BuildRequires:	cmake >= 3.5.1
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libuuid-devel
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CrossGuid is a minimal, cross platform, C++ GUID library. It uses the
best native GUID/UUID generator on the given platform and has a
generic class for parsing, stringifying, and comparing IDs.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qc
mv %{name}-*/* .
%patch -P0 -p1
%patch -P1 -p1

%build
install -d build
cd build
%cmake .. \
	-DCROSSGUID_TESTS:BOOL=%{__ON_OFF tests}
%{__make}

%if %{with tests}
./crossguid-test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_libdir}/libcrossguid.so.*.*.*
%ghost %{_libdir}/libcrossguid.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/crossguid
%{_libdir}/libcrossguid.so
%{_libdir}/cmake/crossguid
%{_pkgconfigdir}/crossguid.pc
