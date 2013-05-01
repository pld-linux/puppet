# TODO
# for man - rst2man.py needed (docutils snap?)
# - puppet user/group
# - initscripts
Summary:	A network tool for managing many disparate systems
Name:		puppet
Version:	3.1.1
Release:	0.4
License:	Apache v2.0
Group:		Networking/Admin
Source0:	http://puppetlabs.com/downloads/puppet/%{name}-%{version}.tar.gz
# Source0-md5:	e942079612703a460a9fdb52e6bcae4a
Patch0:		install-p.patch
Patch1:		ruby19.patch
URL:		http://www.puppetlabs.com/
BuildRequires:	docutils
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-facter >= 1.6
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildConflicts:	ruby-ftools
Requires:	ruby-facter < 2
Requires:	ruby-facter >= 1.6
Requires:	ruby-hiera < 2
Requires:	ruby-hiera >= 1.0
BuildArch:	noarch
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
#%patch0 -p1
#%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
%{__ruby} install.rb \
	--quick \
	--no-rdoc \
	--sitelibdir=%{ruby_vendorlibdir} \
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
%doc README.md
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/auth.conf
%attr(755,root,root) %{_bindir}/extlookup2hiera
%attr(755,root,root) %{_bindir}/puppet
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/modules
%{ruby_vendorlibdir}/puppet
%{ruby_vendorlibdir}/puppet.rb
%{ruby_vendorlibdir}/semver.rb
%{_mandir}/man5/puppet.conf.5*
%{_mandir}/man8/extlookup2hiera.8*
%{_mandir}/man8/puppet*.8*
%{_examplesdir}/%{name}-%{version}

# hiera addons
%{ruby_vendorlibdir}/hiera/backend/puppet_backend.rb
%{ruby_vendorlibdir}/hiera/scope.rb
%{ruby_vendorlibdir}/hiera_puppet.rb

%if 0
%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/puppetmasterd
%attr(755,root,root) %{_sbindir}/puppetrun
%attr(755,root,root) %{_sbindir}/puppetqd
%{_mandir}/man8/puppetmasterd.8*
%{_mandir}/man8/puppetrun.8*
%{_mandir}/man8/puppetqd.8*
%endif

%files -n vim-syntax-puppet
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/puppet.vim
%{_datadir}/vim/syntax/puppet.vim

