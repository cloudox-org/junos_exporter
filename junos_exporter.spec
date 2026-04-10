%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: junos_exporter
Version: 0.15.3
Release: 1%{?dist}
Summary: Prometheus exporter for Junos device metrics.
License: MIT
URL:     https://github.com/czerwonk/junos_exporter

Source0: https://github.com/czerwonk/junos_exporter/releases/download/v%{version}/prometheus-junos-exporter_%{version}_linux_amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default
Source4: %{name}.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometheus exporter for Junos device metrics.

%prep
%setup -q -D -c prometheus-junos-exporter_%{version}_linux_amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yaml


%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service
%config(noreplace) %attr(640, -, %{group})%{_sysconfdir}/prometheus/%{name}.yaml

%changelog
* Tue Mar 31 2026 Ivan Garcia <igarcia@cloudox.org> - 0.15.3
- Initial packaging for the 0.15.3 branch
