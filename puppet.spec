# TODO
# for man - rst2man.py needed (docutils snap?)
# - puppet user/group
# - initscripts
Summary:	A network tool for managing many disparate systems
Name:		puppet
Version:	2.7.18
Release:	0.3
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://puppetlabs.com/downloads/puppet/%{name}-%{version}.tar.gz
# Source0-md5:	210725704692a0ca7b8ffc312471796e
URL:		http://www.puppetlabs.com/
BuildRequires:	docutils
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
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

%package -n vim-syntax-puppet
Summary:	Vim syntax for puppet .pp files
Group:		Applications/Editors/Vim
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-puppet
Vim syntax for puppet .pp files

%prep
%setup -q

# puppet-queue.conf is more of an example, used for stompserver
mv conf/puppet-queue.conf examples/etc/puppet/

%install
rm -rf $RPM_BUILD_ROOT
%{__ruby} install.rb \
	--quick \
	--no-rdoc \
	--destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/modules,%{_datadir}/%{name}/modules}

# Install vim syntax files
install -d $RPM_BUILD_ROOT%{_datadir}/vim/{ftdetect,syntax}
cp -p ext/vim/ftdetect/puppet.vim $RPM_BUILD_ROOT%{_datadir}/vim/ftdetect/puppet.vim
cp -p ext/vim/syntax/puppet.vim $RPM_BUILD_ROOT%{_datadir}/vim/syntax/puppet.vim

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/auth.conf
%attr(755,root,root) %{_bindir}/filebucket
%attr(755,root,root) %{_bindir}/pi
%attr(755,root,root) %{_bindir}/puppet
%attr(755,root,root) %{_bindir}/puppetdoc
%attr(755,root,root) %{_bindir}/ralsh
%attr(755,root,root) %{_sbindir}/puppetca
%attr(755,root,root) %{_sbindir}/puppetd
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/modules
%{ruby_sitelibdir}/puppet
%{ruby_sitelibdir}/puppet.rb
%{ruby_sitelibdir}/semver.rb
%{_mandir}/man5/puppet.conf.5*
%{_mandir}/man8/filebucket.8*
%{_mandir}/man8/pi.8*
%{_mandir}/man8/puppet-agent.8*
%{_mandir}/man8/puppet-apply.8*
%{_mandir}/man8/puppet-ca.8*
%{_mandir}/man8/puppet-catalog.8*
%{_mandir}/man8/puppet-cert.8*
%{_mandir}/man8/puppet-certificate.8*
%{_mandir}/man8/puppet-certificate_request.8*
%{_mandir}/man8/puppet-certificate_revocation_list.8*
%{_mandir}/man8/puppet-config.8*
%{_mandir}/man8/puppet-describe.8*
%{_mandir}/man8/puppet-device.8*
%{_mandir}/man8/puppet-doc.8*
%{_mandir}/man8/puppet-facts.8*
%{_mandir}/man8/puppet-file.8*
%{_mandir}/man8/puppet-filebucket.8*
%{_mandir}/man8/puppet-help.8*
%{_mandir}/man8/puppet-inspect.8*
%{_mandir}/man8/puppet-instrumentation_data.8*
%{_mandir}/man8/puppet-instrumentation_listener.8*
%{_mandir}/man8/puppet-instrumentation_probe.8*
%{_mandir}/man8/puppet-key.8*
%{_mandir}/man8/puppet-kick.8*
%{_mandir}/man8/puppet-man.8*
%{_mandir}/man8/puppet-master.8*
%{_mandir}/man8/puppet-module.8*
%{_mandir}/man8/puppet-node.8*
%{_mandir}/man8/puppet-parser.8*
%{_mandir}/man8/puppet-plugin.8*
%{_mandir}/man8/puppet-queue.8*
%{_mandir}/man8/puppet-report.8*
%{_mandir}/man8/puppet-resource.8*
%{_mandir}/man8/puppet-resource_type.8*
%{_mandir}/man8/puppet-secret_agent.8*
%{_mandir}/man8/puppet-status.8*
%{_mandir}/man8/puppet.8*
%{_mandir}/man8/puppetca.8*
%{_mandir}/man8/puppetd.8*
%{_mandir}/man8/puppetdoc.8*
%{_mandir}/man8/ralsh.8*
%{_examplesdir}/%{name}-%{version}

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/puppetmasterd
%attr(755,root,root) %{_sbindir}/puppetrun
%attr(755,root,root) %{_sbindir}/puppetqd
%{_mandir}/man8/puppetmasterd.8*
%{_mandir}/man8/puppetrun.8*
%{_mandir}/man8/puppetqd.8*

%files -n vim-syntax-puppet
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/puppet.vim
%{_datadir}/vim/syntax/puppet.vim

