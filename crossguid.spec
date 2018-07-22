# TODO
# - missing SONAME
# - missing make install from cmake
#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Lightweight cross platform C++ GUID/UUID library
Name:		crossguid
Version:	0.2.2
# if you rel 1, be ready to port kodi
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	https://github.com/graeme-hill/crossguid/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9fe9554b0dbe2ffe590f759b7e3287cb
URL:		https://github.com/graeme-hill/crossguid/
BuildRequires:	libstdc++-devel
BuildRequires:	cmake
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
%setup -q

%build
install -d build
cd build
%cmake \
	-DXG_TESTS=%{!?with_tests:ON}%{?with_tests:OFF} \
	..
%{__make}

%if %{with tests}
./xgtest
%endif

%install
rm -rf $RPM_BUILD_ROOT
# no install target in cmake, install manually
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}
cp -p Guid.hpp $RPM_BUILD_ROOT%{_includedir}
install -p build/libxg.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_libdir}/libxg.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/Guid.hpp
