Summary: A cross-platform multimedia library
Name: SDL
Version: 1.2.14
Release: 2%{?dist}
# Source: http://www.libsdl.org/release/%{name}-%{version}.tar.gz
# To create the repackaged archive use repackage.sh %{version}
Source: %{name}-%{version}_repackaged.tar.gz
# The license of the file src/video/fbcon/riva_mio.h is bad, but the contents
# of the file has been relicensed to MIT in 2008 by Nvidia for the 
# xf86_video-nv driver, therefore it can be considered ok.
Source1: SDL_config.h
Source2: repackage.sh
Patch0: SDL-1.2.14-byteorder.patch
Patch1: SDL-1.2.12-multilib.patch
Patch2: SDL-1.2.12-disable_yasm.patch
Patch3: SDL-1.2.14-audiodriver.patch

URL: http://www.libsdl.org/
License: LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: arts-devel audiofile-devel
BuildRequires: esound-devel alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libXext-devel libX11-devel
BuildRequires: libGL-devel libGLU-devel
BuildRequires: libXrender-devel libXrandr-devel gettext-devel
BuildRequires: automake autoconf libtool
%ifarch %{ix86}
BuildRequires: nasm
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.

%package devel
Summary: Files needed to develop Simple DirectMedia Layer applications
Group: Development/Libraries
Requires: SDL = %{version}-%{release} alsa-lib-devel
Requires: libX11-devel
Requires: libXext-devel
Requires: libGL-devel
Requires: libGLU-devel
Requires: libXrender-devel
Requires: libXrandr-devel
Requires: pkgconfig
Requires: automake

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the libraries, include files, and other
resources needed for developing SDL applications.

%package static
Summary: Files needed to develop static Simple DirectMedia Layer applications
Group: Development/Libraries
Requires: SDL-devel = %{version}-%{release}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the static libraries needed for developing
static SDL applications.

%prep
%setup -q 
%patch0 -p1 -b .byteorder
%patch1 -p1 -b .multilib
%patch2 -p1 -b .disable_yasm
%patch3 -p1 -b .audiodriver

%build
aclocal
libtoolize
autoconf
%configure \
   --disable-video-svga --disable-video-ggi --disable-video-aalib \
   --disable-debug \
   --enable-sdl-dlopen \
   --enable-dlopen \
   --enable-arts-shared \
   --enable-esd-shared \
   --enable-pulseaudio-shared \
   --enable-alsa \
   --disable-video-ps3 \
   --disable-rpath
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}/%{_includedir}/SDL/SDL_config.h %{buildroot}/%{_includedir}/SDL/SDL_config-%{_arch}.h
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/SDL/SDL_config.h

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README-SDL.txt COPYING CREDITS BUGS
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%doc README WhatsNew docs.html docs/html
%doc docs/index.html
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl.pc
%{_includedir}/SDL
%{_datadir}/aclocal/*
%{_mandir}/man3/SDL*.3*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%changelog
* Tue Aug 03 2010 Petr Pisar <ppisar@redhat.com> - 1.2.14-2
- Remove src/joystick/darwin/10.3.9-FIX/IOHIDLib.h because of license
  (bug #619907)

* Wed Mar 24 2010 Thomas Woerner <twoerner@redhat.com> 1.2.14-1
- rebase to 1.2.14
- fixed build for libtool 2.2.6 and newer
- fix from Josh Boyer <jwboyer@gmail.com>:
  - disable ps3 video support that was added in 2.14.  It fails to
    build on ppc/ppc64

* Thu Feb 25 2010 Thomas Woerner <twoerner@redhat.com> 1.2.13-13
- added repackage.sh script to remove joyos2,h and symbian.zip (really)
- added comment about riva_mmio.h license

* Mon Jan 25 2010 Thomas Woerner <twoerner@redhat.com> 1.2.13-12
- removed also symbian.zip from source archive, because of licensing issues

* Mon Dec 21 2009 Thomas Woerner <twoerner@redhat.com> 1.2.13-11
- removed joyos2.h from source archive, because of licensing issues
  Resolves: rhbz#537918
  Related: rhbz#543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.13-10.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr  7 2009 Thomas Woerner <twoerner@redhat.com> 1.2.13-9
- fixed qemu-kvm segfaults on startup in SDL_memcpyMMX/SSE (rhbz#487720)
  upstream patch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Hans de Goede <hdegoede@redhat.com> 1.2.13-7
- Rewrite pulseaudio support to stop the crackle crackle with the
  new glitch free pulseaudio, this also gives us much better latency,
  as good as with directly using alsa (rh 474745, sdl 698)
- Workaround an obscure bug in the inline-asm revcpy function (by disabling it) 
  This fixes Ri-li crashing on i386 (rh 484121, rh 484362, sdl 699)

* Tue Sep  2 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-6
- dropped pulseaudio hack (rhbz#448270)
- pulseaudio is now used by default
- simplified spec file for new architecture support (rhbz#433618)

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.13-5
- fix license tag

* Wed May 28 2008 Dennis Gilmore <dennis@ausil.us> 1.2.13-4
- fix sparc multilib handling

* Mon Apr  7 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-3
- updated PulseAudio driver (rhbz#439847)
  Thanks to Lennart Poettering for the patch

* Fri Feb  1 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-2
- new static sub package for static libraries

* Mon Jan  7 2008 Thomas Woerner <twoerner@redhat.com> 1.2.13-1
- new version 1.2.13
  - fixes i810 video overlay problem (rhbz#310841)
  - fixes c++ style comments in header files (rhbz#426475)
- review fixes: spec file cleanup, dropped static libs (rhbz#226402)
- fixed pulseaudio hack scripts from Warren for multilib systems (rhbz#426579)
- fixed pulseaudio detection in configure to enable dynamic use of pulseaudio
  libraries

* Fri Dec 21 2007 Warren Togami <wtogami@redhat.com> 1.2.12-5
- correct stupid mistake that broke SDL-devel
  RPM should error out if a SourceX is defined twice...

* Wed Dec 19 2007 Warren Togami <wtogami@redhat.com> 1.2.12-4
- Build with --enable-pulseaudio-shared for testing purposes (#343911)
  It is known to not work in some cases, so not enabled by default.
- Move pulseaudio enabler hack from SDL_mixer (#426275)
- Make pulseaudio enabler hack conditional.  It will only attempt to use it if
  alsa-plugins-pulseaudio is installed.

* Tue Nov  6 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-3
- fixed latest multiarch conflicts: dropped libdir from sdl-config completely
  (rhbz#343141)

* Tue Aug 28 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-2
- use uname -m in multilib patch instead of arch

* Mon Aug 27 2007 Thomas Woerner <twoerner@redhat.com> 1.2.12-1
- new version 1.2.12
  fixes TEXTRELs (rhbz#179407)
- added arm support (rhbz#245411)
  Thanks to Lennert Buytenhek for the patch
- added alpha support (rhbz#246463)
  Thanks to Oliver Falk for the patch
- disabled yasm for SDL (rhbz#234823)
  Thanks to Nikolay Ulyanitsky for the patch

* Tue Mar 20 2007 Thomas Woerner <twoerner@redhat.com> 1.2.11-2
- use X11 dlopen code for 64 bit architectures (rhbz#207903)

* Mon Mar 19 2007 Thomas Woerner <twoerner@redhat.com> 1.2.11-1
- new version 1.2.11
- fixed man page SDL_ListModes (rhbz#208212)
- fixed spurious esound, audiofile dependencies (rhbz#217389)
  Thanks to Ville Skyttä for the patch
- dropped requirements for imake and libXt-devel (rhbz#226402)
- made nasm arch %%{ix86} only (rhbz#226402)
- dropped O3 from options (rhbz#226402)
- dropped tagname environment variable (rhbz#226402)

* Thu Nov  2 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-9
- fixed arch order in SDL_config.h wrapper

* Fri Oct 27 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-8
- fixed multilib conflicts for SDL (#212288)

* Wed Jul 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6.2
- setting the X11 lib and include paths hard to get shared X11 support on all
  architectures

* Wed Jul 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6.1
- added build requires for automake and autoconf

* Tue Jul 25 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-6
- dropped libXt build requires, because libSDL does not need libXt at all - 
  this was an autofoo bug (fixed already)
- fixed multilib devel conflicts (#192749)
- added buidrequires for imake: AC_PATH_X needs imake currently

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.10-5
- rebuild
- use %%configure macro

* Tue Jun 20 2006 Christopher Stone <chris.stone@gmail.com> 1.2.10-4
- added missing (build) requires for libXt libXrender libXrandr
- remove %%makeinstall macro (bad practice)
- use %%{buildroot} macro consistantly

* Tue Jun  6 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-2
- added missing (build) requires for GL and GLU

* Mon May 22 2006 Thomas Woerner <twoerner@redhat.com> 1.2.10-1
- new version 1.2.10
- dropped the following patches because they are not needed anymore:
  ppc_modes, gcc4, yuv_mmx_gcc4 and no_exec_stack
- new pagesize patch (drop PAGE_SIZE, use sysconf(_SC_PAGESIZE) instead)

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-5
- added upstream no exec stack patch

* Thu Jan 26 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-4
- prefer alsa sound output, then artsd and esd

* Tue Jan 24 2006 Thomas Woerner <twoerner@redhat.com> 1.2.9-3
- dropped libtool .la files from devel package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Thomas Woerner <twoerner@redhat.com> 1.2.9-2.1
- fixed build requires

* Tue Nov 15 2005 Warren Togami <wtogami@redhat.com> 1.2.9-2
- -devel req actual X libs

* Mon Nov  7 2005 Thomas Woerner <twoerner@redhat.com> 1.2.9-1
- new version 1.2.9 with additional gcc4 fixes
- using xorg-x11-devel instead of XFree86-devel

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 1.2.8-3.2
- fix configure script for libdir so library deps are identical on all
  arches (#158346)

* Thu Apr 14 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-3.1
- new version of the gcc4 fix

* Tue Apr 12 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-3
- fixed gcc4 compile problems
- fixed x86_64 endian problem

* Wed Feb  9 2005 Thomas Woerner <twoerner@redhat.com> 1.2.8-2
- rebuild

* Fri Dec 17 2004 Thomas Woerner <twoerner@redhat.com> 1.2.8-1
- new version 1.2.8

* Thu Oct 14 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-8
- added patch from SDL CVS for arts detection/initialization problem (#113831)

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-7.1
- moved to new autofoo utils

* Fri Jul  9 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-7
- fixed resolution switching for ppc (#127254)

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-6
- fixed gcc34 build problems

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-4
- added requires for alsa-lib-devel (#123374)

* Wed Mar 31 2004 Harald Hoyer <harald@redhat.com> - 1.2.7-3
- fixed gcc34 compilation issues

* Wed Mar 10 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-2.1
- added buildrequires for alsa-lib-devel
- now using automake 1.5

* Tue Mar  9 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-2
- Fixed SDL requires for devel package

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt
- Revive SDL-ppc64.patch

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 1.2.7-1
- new version 1.2.7

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 1.2.6-3.1
- disabled several video modes, hopefuilly fixes (#113831)

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 1.2.6-3
- fix for alsa 1.0

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 1.2.6-2
- removed rpath
- using O3 instead of O2, now (SDL_RLEaccel.c compile error)
- added BuildRequires for nasm

* Tue Sep  2 2003 Thomas Woerner <twoerner@redhat.com> 1.2.6-1
- new version 1.2.6

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 1.2.5-9
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  4 2003 Than Ngo <than@redhat.com> 1.2.5-7
- fix build problem with gcc 3.3
- clean up specfile

* Mon May 19 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-5
- rebuild

* Tue Apr 15 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-4
- X11 modes fix (use more than 60 Hz, when possible)

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 1.2.5-3.5
- ppc64 fix

* Mon Feb 10 2003 Thomas Woerner  <twoerner@redhat.com> 1.2.5-3
- added -fPIC to LDFLAGS

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Thomas Woerner <twoerner@redhat.com> 1.2.5-1
- new version 1.2.5
- disabled conflicting automake16 patch
- dgavideo modes fix (#78861)

* Sun Dec 01 2002 Elliot Lee <sopwith@redhat.com> 1.2.4-7
- Fix unpackaged files by including them.
- _smp_mflags

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.2.4-6
- remove unpackaged files from the buildroot
- lib64'ize

* Sat Jul 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require nasm for mainframe

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-4
- Fix bug #67255

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-1
- 1.2.4
- Fix build with automake 1.6

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-7
- Fix AM_PATH_SDL automake macro with AC_LANG(c++) (#60533)

* Thu Feb 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-6
- Rebuild in current environment

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-5
- dlopen() aRts and esd rather than linking directly to them.
- make sure aRts and esd are actually used if they're running.

* Mon Jan 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-4
- Don't crash without xv optimization: BuildRequire a version of nasm that
  works.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Dec 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-2
- Rebuild with new aRts, require arts-devel rather than kdelibs-sound-devel
- Temporarily exclude alpha (compiler bugs)

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-1
- 1.2.3

* Sat Nov 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-5
- Add workaround for automake 1.5 asm bugs

* Tue Oct 30 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-4
- Make sure -fPIC is used on all architectures (#55039)
- Fix build with autoconf 2.5x

* Fri Aug 31 2001 Bill Nottingham <notting@redhat.com> 1.2.2-3
- rebuild (fixes #50750??)

* Thu Aug  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-2
- SDL-devel should require esound-devel and kdelibs-sound-devel (#44884)

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-1
- Update to 1.2.2; this should fix #47941
- Add build dependencies

* Tue Jul 10 2001 Elliot Lee <sopwith@redhat.com> 1.2.1-3
- Rebuild to eliminate libXv/libXxf86dga deps.

* Fri Jun 29 2001 Preston Brown <pbrown@redhat.com>
- output same libraries for sdl-config whether --libs or --static-libs 
  selected.  Fixes compilation of most SDL programs.
- properly packaged new HTML documentation

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.1-1
- 1.2.1

* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.0-2
- Add Bill's byteorder patch

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.2.0

* Tue Feb 27 2001 Karsten Hopp <karsten@redhat.de>
- SDL-devel requires SDL

* Tue Jan 16 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Require arts rather than kdelibs-sound

* Sun Jan  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.7

* Tue Oct 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.6

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- build against new DGA
- update to 1.1.4, remove patches (they're now in the base release)

* Tue Aug  1 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- %%post -p /sbin/ldconfig (Bug #14928)
- add URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- replace patch that fell out of SRPM

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths
- use 1.1 (development) version; everything even from Loki links to it!

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- autoconf fixes for ia64

* Mon Apr 24 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.8

* Tue Feb 15 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.4, fixes problems when run in 8bpp

* Tue Feb 01 2000 Tim  Powers <timp@redhat.com>
- applied patch from Hans de Goede <hans@highrise.nl> for fullscreen toggling.
- using  --enable-video-x11-dgamouse since it smoothes the mouse some.

* Sun Jan 30 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.3, bugfix update

* Fri Jan 28 2000 Tim Powers <timp@redhat.com>
- fixed group etc

* Fri Jan 21 2000 Tim Powers <timp@redhat.com>
- build for 6.2 Powertools

* Wed Jan 19 2000 Sam Lantinga <slouken@devolution.com>
- Re-integrated spec file into SDL distribution
- 'name' and 'version' come from configure 
- Some of the documentation is devel specific
- Removed SMP support from %%build - it doesn't work with libtool anyway

* Tue Jan 18 2000 Hakan Tandogan <hakan@iconsult.com>
- Hacked Mandrake sdl spec to build 1.1

* Sun Dec 19 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Sat Dec 18 1999 John Buswell <johnb@mandrakesoft.com>
- Add symlink for libSDL-1.0.so.0 required by sdlbomber
- Added docs

* Thu Dec 09 1999 Lenny Cartier <lenny@mandrakesoft.com>
- v 1.0.0

* Mon Nov  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First spec file for Mandrake distribution.

# end of file
