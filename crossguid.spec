#
# Conditional build:
%bcond_without	tests		# build without tests

%define rel 1
%define short_commit 8f399e8
%define commit_date 20150803
Summary:	Lightweight cross platform C++ GUID/UUID library
Name:		crossguid
# 0.2.2 is being prepated on "dev-0.2" branch
Version:	0
Release:	0.%{rel}.%{commit_date}
License:	MIT
Group:		Libraries
Source0:	https://github.com/graeme-hill/crossguid/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz
# Source0-md5:	696a6573286d6fdbfde18686aa9f6489
URL:		https://github.com/graeme-hill/crossguid/
Source1:	Makefile
BuildRequires:	libstdc++-devel
BuildRequires:	libuuid-devel
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

cp -p %{SOURCE1} Makefile

%build
%{__make} \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags}" \
	CXXFLAGS="%{rpmcxxflags}"

%if %{with tests}
%{__make} test \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags}" \
	CXXFLAGS="%{rpmcxxflags}"
./test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir} \
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
%{_includedir}/guid.h
%{_libdir}/libcrossguid.so
