%global gdk_pixbuf2_version               2.36.5
%global gtk3_version                      3.3.6
%global glib2_version                     2.53.0
%global gsettings_desktop_schemas_version 3.27.0
%global po_package                        gnome-desktop-3.0

%global tarball_version %%(echo %{version} | tr '~' '.')

Name: gnome-desktop3
Version: 40.4
Release: 1%{?dist}
Summary: Library with common API for various GNOME modules

License: GPLv2+ and LGPLv2+
URL: http://www.gnome.org
Source0: http://download.gnome.org/sources/gnome-desktop/40/gnome-desktop-%{tarball_version}.tar.xz

Source1: gnome-mimeapps.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/totem/data/mime-type-list.txt | grep -v audio/flac | grep -v ^#` ; do if grep MimeType /home/hadess/Projects/jhbuild/rhythmbox/data/rhythmbox.desktop.in.in | grep -q "$i;" ; then echo "$i=org.gnome.Rhythmbox3.desktop;rhythmbox.desktop;org.gnome.Totem.desktop;" >> totem-defaults.list ; else echo "$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; fi ; done ; for i in `cat /home/hadess/Projects/jhbuild/totem/data/uri-schemes-list.txt | grep -v ^#` ; do echo "x-scheme-handler/$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; done
Source2: totem-defaults.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/file-roller/data/supported-mime-types | sed 's/;//g'` application/x-source-rpm ; do if grep MimeType /usr/share/applications/org.gnome.Nautilus.desktop | grep -q "$i;" ; then echo "$i=org.gnome.Nautilus.desktop;org.gnome.FileRoller.desktop;" >> file-roller-defaults.list ; elif ! `grep -q $i gnome-mimeapps.list` ; then echo $i=org.gnome.FileRoller.desktop\; >> file-roller-defaults.list ; fi ; done && for i in `grep MimeType= /usr/share/applications/org.gnome.Nautilus.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do if ! `grep -q $i file-roller-defaults.list || grep -q $i gnome-mimeapps.list` ; then echo "missing handler $i" ; fi ; done
Source3: file-roller-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/org.gnome.eog.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=org.gnome.eog.desktop\; >> eog-defaults.list ; done
Source4: eog-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/org.gnome.Evince.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=org.gnome.Evince.desktop\; >> evince-defaults.list ; done
Source5: evince-defaults.list

BuildRequires: gcc
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: itstool
BuildRequires: meson
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf2_version}
BuildRequires: pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(iso-codes)
BuildRequires: pkgconfig(libseccomp)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(xkeyboard-config)

Conflicts: shared-mime-info < 2.0-4
Requires: shared-mime-info

%if !0%{?flatpak}
Requires: bubblewrap
%endif
Requires: gdk-pixbuf2%{?_isa} >= %{gdk_pixbuf2_version}
Requires: glib2%{?_isa} >= %{glib2_version}
# needed for GnomeWallClock
Requires: gsettings-desktop-schemas >= %{gsettings_desktop_schemas_version}

# GnomeBGSlideShow API change breaks older gnome-shell versions
Conflicts: gnome-shell < 3.33.4

%description
gnome-desktop contains the libgnome-desktop library as well as a data
file that exports the "GNOME" version to the Settings Details panel.

The libgnome-desktop library provides API shared by several applications
on the desktop, but that cannot live in the platform for various
reasons. There is no API or ABI guarantee, although we are doing our
best to provide stability. Documentation for the API is available with
gtk-doc.

%package devel
Summary: Libraries and headers for %{name}
License: LGPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -p1 -n gnome-desktop-%{tarball_version}

%build
%meson -Dgtk_doc=true -Dinstalled_tests=true
%meson_build

%install
%meson_install

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE2 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE3 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE4 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE5 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list

%find_lang %{po_package} --all-name --with-gnome

%files -f %{po_package}.lang
%doc AUTHORS NEWS README.md
%license COPYING COPYING.LIB
%{_datadir}/gnome/gnome-version.xml
%{_datadir}/applications/gnome-mimeapps.list
# LGPL
%{_libdir}/libgnome-desktop-3.so.19{,.*}
%{_libdir}/girepository-1.0/GnomeDesktop-3.0.typelib
%{_libexecdir}/gnome-desktop-debug/

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/GnomeDesktop-3.0.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%doc %{_datadir}/gtk-doc/html/gnome-desktop3/

%files tests
%{_libexecdir}/installed-tests/gnome-desktop
%{_datadir}/installed-tests

%changelog
* Thu Aug 19 2021 Kalev Lember <klember@redhat.com> - 40.4-1
- Update to 40.4

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 40.1-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed May 05 2021 Kalev Lember <klember@redhat.com> - 40.1-1
- Update to 40.1

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 40.0-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Apr 01 2021 Bastien Nocera <bnocera@redhat.com> - 40.0-2
+ gnome-desktop3-40.0-2
- Re-add mistakenly removed debug utilities

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Thu Mar 18 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Sun Feb 21 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Wed Feb 10 2021 Kalev Lember <klember@redhat.com> - 40~alpha.0-1
- Update to 40.alpha.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kalev Lember <klember@redhat.com> - 3.38.3-1
- Update to 3.38.3

* Wed Nov 25 2020 Kalev Lember <klember@redhat.com> - 3.38.2-1
- Update to 3.38.2

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Mon Sep 07 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Wed Aug 26 2020 Kalev Lember <klember@redhat.com> - 3.37.91-1
- Update to 3.37.91

* Tue Aug 25 2020 Bastien Nocera <bnocera@redhat.com> - 3.37.90.1-2
+ gnome-desktop3-3.37.90.1-2
- Add GNOME specific defaults apps list, moved from shared-mime-info

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.37.90.1-1
- Update to 3.37.90.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 3.37.3-1
- Update to 3.37.3

* Fri Jun 05 2020 Kalev Lember <klember@redhat.com> - 3.37.2-1
- Update to 3.37.2

* Thu Apr 30 2020 Kalev Lember <klember@redhat.com> - 3.37.1-1
- Update to 3.37.1

* Wed Apr 29 2020 Kalev Lember <klember@redhat.com> - 3.36.2-1
- Update to 3.36.2

* Tue Mar 31 2020 Kalev Lember <klember@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Tue Mar 10 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Thu Feb 06 2020 Kalev Lember <klember@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.35.4-1
- Update to 3.35.4

* Thu Dec 05 2019 Benjamin Berg <bberg@redhat.com> - 3.35.2-2
- Add upstream patch adding new API that is already in stable
  https://gitlab.gnome.org/GNOME/gnome-desktop/merge_requests/58

* Mon Dec 02 2019 Kalev Lember <klember@redhat.com> - 3.35.2-1
- Update to 3.35.2

* Tue Oct 08 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 3.33.92.1-1
- Update to 3.33.92.1

* Wed Aug 21 2019 Kalev Lember <klember@redhat.com> - 3.33.91-1
- Update to 3.33.91

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Fri Jul 26 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 3.33.4-3
- Drop compat library, which might be causing problems

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Kalev Lember <klember@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Tue Jun 18 2019 Kalev Lember <klember@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Wed May 22 2019 Kalev Lember <klember@redhat.com> - 3.33.2-1
- Update to 3.33.2

* Thu May 09 2019 Kalev Lember <klember@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Wed Apr 10 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Fri Mar 08 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Wed Feb 20 2019 Kalev Lember <klember@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 3.31.90-3
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Pete Walter <pwalter@fedoraproject.org> - 3.31.90-2
- Drop gnome-themes-extra requires

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90
- Sync package description with upstream README

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 3.31.4-1
- Update to 3.31.4
- Switch to the meson build system

* Sat Oct 27 2018 Kalev Lember <klember@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Fri Sep 28 2018 Owen Taylor <otaylor@redhat.com> - 3.30.1-2
- Disable bubblewrap Requires when building for inclusion in a Flatpak

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.30.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Sun Aug 12 2018 Kalev Lember <klember@redhat.com> - 3.29.90.1-1
- Update to 3.29.90.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Kalev Lember <klember@redhat.com> - 3.28.2-1
- Update to 3.28.2

* Wed Apr 11 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92
- Remove ldconfig scriptlets

* Sat Feb 10 2018 Bastien Nocera <bnocera@redhat.com> - 3.27.90-1
+ gnome-desktop3-3.27.90-1
- Update to 3.27.90

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 3.26.2-1
- Update to 3.26.2

* Fri Oct 06 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Thu Aug 24 2017 Bastien Nocera <bnocera@redhat.com> - 3.25.91.1-1
+ gnome-desktop3-3.25.91.1-1
- Update to 3.25.91.1

* Wed Aug 09 2017 Bastien Nocera <bnocera@redhat.com> - 3.25.90-1
+ gnome-desktop3-3.25.90-1
- Update to 3.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 3.25.2-1
- Update to 3.25.2
- Set minimum required glib2 version

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 3.24.2-1
- Update to 3.24.2

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Richard Hughes <rhughes@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Kalev Lember <klember@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Sun Oct 30 2016 Kalev Lember <klember@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92
- Don't set group tags

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Mon Jun 13 2016 Kalev Lember <klember@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Wed Apr 27 2016 Owen Taylor <otaylor@redhat.com> - 3.20.1-2
- Remove dependency on system-backgrounds-gnome; this made sense when
  gnome-desktop contained the GConf schemas, but now the background
  settings live in gsettings-desktop-schemas and are overridden to
  point to a Fedora background with a file we drop in from
  desktop-backgrounds-gnome.

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Thu Mar 17 2016 Kalev Lember <klember@redhat.com> - 3.19.93-1
- Update to 3.19.93

* Mon Mar 14 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Fri Mar 04 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Tue Nov 24 2015 Kalev Lember <klember@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Tue Oct 13 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 03 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Tue Aug 18 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4
- Preserve timestamps during install

* Wed Jun 24 2015 David King <amigadave@amigadave.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.2-1
- Update to 3.17.2

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Wed Apr 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Mon Feb 16 2015 David King <amigadave@amigadave.com> - 3.15.90-1
- Update to 3.15.90
- Use license macro for COPYING and COPYING.LIB
- Use pkgconfig for BuildRequires

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Fri Dec 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2.1-1
- Update to 3.15.2.1

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-2
- Obsolete compat-gnome-desktop310 from rhughes-f20-gnome-3-12 copr

* Wed Nov 12 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Wed Nov 12 2014 Vadim Rutkovsky <vrutkovs@redhat.com> - 3.14.1-2
- Build installed tests

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Drop redhat-menus dependency

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Fri May 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Update to 3.13.1

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1
- Tighten -devel deps with %%{_isa}

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 16 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Fri Nov 01 2013 Kalev Lember <kalevlember@gmail.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Mon Sep  9 2013 Rui Matos <rmatos@redhat.com> - 3.9.91-2
- Add patch to default to ibus-kkc for Japanese

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1.1-1
- Update to 3.9.1.1
- Remove unused startup-notification dependency

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91.1-1
- Update to 3.7.91.1

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Conflict with older gnome-shell versions

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Sep 26 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0.1-1
- Update to 3.6.0.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-3
- Add missing files

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-2
- Add missing BRs

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Mon May 14 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Mon Apr 16 2012 Daniel Drake <dsd@laptop.org> - 3.4.1-2
- Add upstream patch to fix crash when the system clock is wrong
- Fixes GNOME#673551, OLPC#11714

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Mon Mar 19 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Sep 12 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-3
- Fix a gnome-screensaver crash

* Fri Sep  9 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-2
- Require gsettings-desktop-schemas

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-1
- Update to 3.1.90.1

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon May  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Prevent segfaults in gnome-rr users on randr-less displays

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-2
- Require gnome-themes-standard (#674799)

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Mar 24 2011 Christopher Aillon <caillon@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- 2.91.90
- Drop obsolete GConf dep

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6.1-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6.1-2
- Fix refcount issue in GnomeRRLabeler

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6.1-1
- Update to 2.91.6.1

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Rebuild against newer gtk

* Fri Jan 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-2
- Build with introspection support

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-2
- Rebuild against new gtk

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 2.91.3-1
- Update to 2.91.3

* Wed Nov 17 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Thu Nov 11 2010 Bill Nottingham <notting@redhat.com> 2.91.1-3
- remove some extraneous deps

* Thu Nov 11 2010 Bastien Nocera <bnocera@redhat.com> 2.91.1-2
- Fix a possible double-free crasher

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.1-1
- Update to 2.91.1

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-3
- Rebuild against newer gtk3

* Thu Oct 28 2010 Bill Nottingham <notting@redhat.com> 2.91.0-2
- flip background to match F-14

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.4-4
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-3
- Rebuild against newer gobject-introspection
- Rebuild against newer gtk

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-2
- Prevent file conflict with gnome-desktop

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-1
- Update to 2.90.4

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-1
- 2.90.2

* Thu Jun 17 2010 Richard Hughes <richard@hughsie.com> 2.90.1-1
- Initial build for review.

