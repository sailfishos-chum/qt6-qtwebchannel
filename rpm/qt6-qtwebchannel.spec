%global qt_version 6.8.3

Summary: Qt6 - WebChannel component
Name:    qt6-qtwebchannel
Version: 6.8.3
Release: 2%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
#libQt6Core.so.6(Qt_5_PRIVATE_API)(64bit)
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtwebsockets-devel

BuildRequires: pkgconfig(xkbcommon) >= 0.5.0
BuildRequires: openssl-devel

%description
The Qt WebChannel module provides a library for seamless integration of C++
and QML applications with HTML/JavaScript clients. Any QObject can be
published to remote clients, where its public API becomes available.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtwebchannel-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSES/*
%{_qt6_libdir}/libQt6WebChannel.so.6*
%{_qt6_libdir}/libQt6WebChannelQuick.so.6*
%{_qt6_archdatadir}/qml/QtWebChannel/

%files devel
%{_qt6_headerdir}/QtWebChannel/
%{_qt6_headerdir}/QtWebChannelQuick/
%{_qt6_libdir}/libQt6WebChannel.so
%{_qt6_libdir}/libQt6WebChannel.prl
%{_qt6_libdir}/libQt6WebChannelQuick.so
%{_qt6_libdir}/libQt6WebChannelQuick.prl
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebChannelTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebChannel/
%{_qt6_libdir}/cmake/Qt6WebChannel/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WebChannelQuick/
%{_qt6_libdir}/cmake/Qt6WebChannelQuick/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_webchannel*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif
