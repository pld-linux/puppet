# TODO
# for man - rst2man.py needed (docutils snap?)
Summary:	A network tool for managing many disparate systems
Name:		puppet
Version:	2.6.6
Release:	0.1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://puppetlabs.com/downloads/puppet/%{name}-%{version}.tar.gz
# Source0-md5:	-
URL:		http://www.puppetlabs.com/
BuildRequires:	docutils
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby >= 1:1.8.1
BuildRequires:	ruby-facter >= 1.5
Requires:	ruby >= 1:1.8.1
Requires:	ruby-facter >= 1.5
Requires:	ruby-shadow
#%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Puppet lets you centrally manage every important aspect of your system
using a cross-platform specification language that manages all the
separate elements normally aggregated in different files, like users,
cron jobs, and hosts, along with obviously discrete elements like
packages, services, and files.

%package server
Summary:	Server for the puppet system management tool
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires:	rc-scripts

%description server
Provides the central puppet server daemon which provides manifests to
clients. The server can also function as a certificate authority and
file server.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{ruby_sitelibdir}
%{__ruby} install.rb \
	--no-rdoc \
	--destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGELOG examples
%attr(755,root,root) %{_bindir}/filebucket
%attr(755,root,root) %{_bindir}/puppet
%attr(755,root,root) %{_bindir}/puppetca
%attr(755,root,root) %{_bindir}/puppetd
%attr(755,root,root) %{_bindir}/puppetdoc
%attr(755,root,root) %{_bindir}/puppetmasterd
%attr(755,root,root) %{_bindir}/puppetrun
%attr(755,root,root) %{_bindir}/ralsh
%{ruby_sitelibdir}/puppet
%{ruby_sitelibdir}/puppet.rb
%{_mandir}/man8/*.8.*
