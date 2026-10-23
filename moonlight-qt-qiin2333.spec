%global debug_package       %{nil}

Name:        moonlight-qt-qiin2333
Version:     6.5.1
Release:     1%{?dist}
Summary:     Open source PC client for NVIDIA GameStream and Sunshine (qiin2333 fork with extra features)

License:     GPL-3.0-only AND GPL-3.0-or-later AND LGPL-2.1-or-later AND MIT AND Zlib
URL:         https://github.com/qiin2333/moonlight-qt
Source0:     %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: qt6-qtsvg-devel
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtmultimedia-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: openssl-devel
BuildRequires: SDL2-devel
BuildRequires: SDL2_ttf-devel
BuildRequires: (ffmpeg-devel or ffmpeg-free-devel)
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: opus-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
BuildRequires: libdrm-devel
BuildRequires: libplacebo-devel

# Wayland/EGL/XCB are only pulled in transitively today (qt6-qtbase-devel -> pkgconfig(egl)
# / pkgconfig(wayland-client), sdl2-compat-devel -> pkgconfig(x11) -> libX11-devel ->
# pkgconfig(xcb)). app/app.pro probes all of them with packagesExist() and silently drops
# the feature when the .pc file is missing, so name them explicitly to make the feature set
# deterministic instead of depending on Qt/SDL metadata of the moment.
BuildRequires: wayland-devel
BuildRequires: libxcb-devel
BuildRequires: libX11-devel
BuildRequires: libglvnd-devel

# scripts/derive-version.py is invoked by app/app.pro; without python3 the build falls back
# to the stale app/version.txt instead of failing.
BuildRequires: python3

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: git

Requires:    qt6-qtbase
Requires:    (ffmpeg or ffmpeg-free)
Requires:    libva
Requires:    libvdpau
Requires:    opus
Requires:    openssl
Requires:    SDL2
Requires:    SDL2_ttf
Requires:    (pulseaudio or pipewire-pulseaudio)
Requires:    alsa-lib
Requires:    libdrm
# Qt Quick windows (app/main.cpp loads the QML ApplicationWindow) need the Qt Wayland QPA
# plugin for a native Wayland session; libQt6WaylandClient is not linked, so nothing pulls
# qt6-qtwayland in automatically and the app would fall back to XWayland.
Requires:    qt6-qtwayland

# This package ships exactly the same files as moonlight-qt (same /usr/bin/moonlight, same
# desktop file ID, same icon and appdata).
Conflicts:   moonlight-qt

%description
Moonlight PC is an open source PC client for NVIDIA
GameStream and Sunshine. (qiin2333 fork with extra features)

%prep
%setup -q -n moonlight-qt-%{version}
# add git info to retrieve submodules
git clone --bare --depth=1 --single-branch --branch v%{version} %{url} .git
git init
git reset --hard HEAD
# skip libs since they are not needed in linux
git -c submodule."libs".update=none submodule update --init --recursive --depth=1 --single-branch

%build
# Configure and build the project
qmake6 PREFIX=/usr moonlight-qt.pro
make release

%install
# Install the built files
make INSTALL_ROOT=$RPM_BUILD_ROOT install

# COLLECT LICENSES: only files that are tracked in the upstream tarball can be marked here.
# The submodule licenses (moonlight-common-c, qmdnsengine, app/SDL_GameControllerDB) are
# fetched by %prep and are not part of the tarball, so they would break offline builds.
install -Dpm 0644 LICENSE $RPM_BUILD_ROOT%{_licensedir}/%{name}/LICENSE
install -Dpm 0644 h264bitstream/LICENSE $RPM_BUILD_ROOT%{_licensedir}/%{name}/LICENSE.h264bitstream

%files
%attr(755,root,root) %{_bindir}/moonlight
%attr(755,root,root) %{_bindir}/moonlight-clipboard-helper
%attr(644,root,root) %{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
%attr(644,root,root) %{_datadir}/icons/hicolor/scalable/apps/moonlight.svg
%attr(644,root,root) %{_datadir}/metainfo/com.moonlight_stream.Moonlight.appdata.xml
%license LICENSE
%license %{_licensedir}/%{name}/LICENSE.h264bitstream

%changelog
* Fri Oct 23 2026 Jemn853 <as853472853@gmail.com> - 6.5.1-1
- Update to 6.5.1
* Sun Oct 11 2026 Jemn853 <as853472853@gmail.com> - 6.5.0-2
- Add Requires: qt6-qtwayland and Conflicts: moonlight-qt
- Switch License to an SPDX expression and ship the GPLv3/LGPL-2.1 license texts
- Add explicit BuildRequires for the optional Wayland/EGL/XCB features and python3
* Sat Oct 10 2026 Jemn853 <as853472853@gmail.com> - 6.5.0-1
- Update to 6.5.0
* Wed Oct 07 2026 Jemn853 <as853472853@gmail.com> - 6.4.5-2
- Add BuildRequires: qt6-qtbase-private-devel for the native Wayland bridge
* Wed Oct 07 2026 Jemn853 <as853472853@gmail.com> - 6.4.5-1
- Update to 6.4.5
