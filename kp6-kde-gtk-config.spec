#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.4.1
%define		qtver		5.15.2
%define		kpname		kde-gtk-config
Summary:	GTK2 and GTK3 Configurator for KDE
Name:		kp6-%{kpname}
Version:	6.4.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	72fe125aae60549f8b688b3f15ed5d14
#Patch0: x32.patch
%define		specflags	-I/usr/include/harfbuzz
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gsettings-desktop-schemas
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kbookmarks-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kp6-kdecoration-devel >= 5.23.0
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GTK2 and GTK3 Configurator for KDE.

%prep
%setup -q -n %{kpname}-%{version}
#%%patch0 -p1

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

sed -i -e 's|/usr/bin/env sh|/bin/bash|' $RPM_BUILD_ROOT/usr/share/kconf_update/remove_window_decorations_from_gtk_css.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/libexec/gtk3_preview
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/gtkconfig.so
%attr(755,root,root) %{_libdir}/kconf_update_bin/gtk_theme
%{_datadir}/kconf_update/gtkconfig.upd
%attr(755,root,root) %{_libdir}/gtk-3.0/modules/libcolorreload-gtk-module.so
%attr(755,root,root) %{_libdir}/gtk-3.0/modules/libwindow-decorations-gtk-module.so
%attr(755,root,root) %{_datadir}/kconf_update/remove_window_decorations_from_gtk_css.sh
%{_datadir}/themes/Breeze/window_decorations.css
%dir %{_datadir}/kcm-gtk-module
%{_datadir}/kcm-gtk-module/preview.ui
%attr(755,root,root) %{_libdir}/kconf_update_bin/remove_deprecated_gtk4_option
%{_datadir}/qlogging-categories6/kde-gtk-config.categories
