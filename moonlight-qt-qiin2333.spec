%global debug_package       %{nil}
%define major_version       6.2.70
%define release_version     1

Name:        moonlight-qt-qiin2333
Version:     %{major_version}
Release:     %{release_version}%{?dist}
Summary:     Open source PC client for NVIDIA GameStream and Sunshine (qiin2333 fork with extra features)

License:     GPL-3.0
URL:         https://github.com/qiin2333/moonlight-qt
Source0:     %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: qt6-qtsvg-devel
BuildRequires: qt6-qtdeclarative-devel
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

%files
%attr(755,root,root) %{_bindir}/moonlight
%attr(644,root,root) %{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
%attr(644,root,root) %{_datadir}/icons/hicolor/scalable/apps/moonlight.svg
%attr(644,root,root) %{_datadir}/metainfo/com.moonlight_stream.Moonlight.appdata.xml
