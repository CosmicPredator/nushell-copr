%global debug_package %{nil}
%global __strip /bin/true

Name:           nushell
Version:        0.0.0
Release:        1%{?dist}
Summary:        A new type of shell (prebuilt upstream binary)
License:        MIT
URL:            https://www.nushell.sh
Source0:        https://github.com/nushell/nushell/releases/download/%{version}/nu-%{version}-x86_64-unknown-linux-gnu.tar.gz
Source1:        https://github.com/nushell/nushell/releases/download/%{version}/nu-%{version}-aarch64-unknown-linux-gnu.tar.gz
ExclusiveArch:  x86_64 aarch64

%description
Nushell is a modern shell that treats data as structured tables.
This package repackages the official upstream release binaries.

%prep
%setup -q -c -T
%ifarch x86_64
tar xzf %{SOURCE0} --strip-components=1
%endif
%ifarch aarch64
tar xzf %{SOURCE1} --strip-components=1
%endif

%build
# nothing to build

%install
install -Dm755 nu %{buildroot}%{_bindir}/nu
for p in nu_plugin_*; do
  [ -f "$p" ] && install -Dm755 "$p" %{buildroot}%{_bindir}/"$p"
done

%post
grep -qxF %{_bindir}/nu /etc/shells || echo %{_bindir}/nu >> /etc/shells

%postun
if [ $1 -eq 0 ]; then
  sed -i '\|^%{_bindir}/nu$|d' /etc/shells
fi

%files
%license LICENSE
%{_bindir}/nu*

%changelog
* Sun Nov 22 2026 Your Name <you@example.com> - 0.0.0-1
- Initial package
