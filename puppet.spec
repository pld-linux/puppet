# TODO
# for man - rst2man.py needed (docutils snap?)
Summary:	A network tool for managing many disparate systems
Name:		puppet
Version:	3.7.3
Release:	0.1
License:	Apache v2.0
Group:		Networking/Admin
Source0:	http://puppetlabs.com/downloads/puppet/%{name}-%{version}.tar.gz
# Source0-md5:	cc294da1d51df07bcc7f6cf78bd90ce0
Patch0:		install-p.patch
Patch1:		ruby19.patch
URL:		http://www.puppetlabs.com/
BuildRequires:	docutils
BuildRequires:	hiera
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-facter >= 1.6
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildConflicts:	ruby-ftools
Provides:	group(puppet)
Provides:	user(puppet)
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	hiera < 2
Requires:	hiera >= 1.0
Requires:	ruby-facter < 2
Requires:	ruby-facter >= 1.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

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
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description server
Provides the central puppet server daemon which provides manifests to
clients. The server can also function as a certificate authority and
file server.

%package -n openldap-schema-%{name}
Summary:	Puppet LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla Puppet
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-schema-rfc2739
Requires:	openldap-servers
Requires:	sed >= 4.0

%description -n openldap-schema-%{name}
This package contains puppet.schema for openldap.

%description -n openldap-schema-%{name} -l pl.UTF-8
Ten pakiet zawiera puppet.schema dla pakietu openldap.

%package -n vim-syntax-%{name}
Summary:	Vim syntax for puppet .pp files
Group:		Applications/Editors/Vim
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-%{name}
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

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/{manifests,modules},%{_datadir}/%{name}/modules} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d} \
	$RPM_BUILD_ROOT%{_localstatedir}/{lib,log,run}/%{name}

cp -p ext/redhat/client.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/puppet
cp -p ext/redhat/client.init $RPM_BUILD_ROOT/etc/rc.d/init.d/puppet
cp -p ext/redhat/server.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/puppetmaster
cp -p ext/redhat/server.init $RPM_BUILD_ROOT/etc/rc.d/init.d/puppetmaster
cp -p ext/redhat/queue.init $RPM_BUILD_ROOT/etc/rc.d/init.d/puppetqueue

cp -p ext/redhat/fileserver.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/fileserver.conf
cp -p ext/redhat/puppet.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/puppet.conf
cp -p ext/redhat/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/puppet

# Install the ext/ directory to %{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a ext $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d $RPM_BUILD_ROOT%{schemadir}
cp -p ext/ldap/puppet.schema $RPM_BUILD_ROOT%{schemadir}

# Install vim syntax files
install -d $RPM_BUILD_ROOT%{_datadir}/vim/{ftdetect,syntax}
mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/ext/vim/ftdetect/puppet.vim,%{_datadir}/vim/ftdetect}
mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/ext/vim/syntax/puppet.vim,%{_datadir}/vim/syntax}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# emacs and vim bits are installed elsewhere
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/{emacs,vim}

# remove misc packaging artifacts not applicable to rpms or other cruft
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/{gentoo,freebsd,solaris,suse,windows,osx,ips,debian}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/{redhat,ldap,systemd}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/{build_defaults.yaml,project_data.yaml,envpuppet*}

# Rpmlint fixup
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/regexp_nodes/regexp_nodes.rb
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/ext/puppet-load.rb

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
echo "D /var/run/%{name} 0755 %{name} %{name} -" > \
    $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 292 puppet
%useradd -u 292 -g puppet -c "Puppet" -d %{_localstatedir}/lib/%{name} puppet

%postun
if [ "$1" = "0" ]; then
	%userremove puppet
	%groupremove puppet
fi

%post
/sbin/chkconfig --add puppet
%service puppet restart

%preun
if [ "$1" = "0" ]; then
	%service -q puppet stop
	/sbin/chkconfig --del puppet
fi

%post server
/sbin/chkconfig --add puppetmaster
/sbin/chkconfig --add puppetqueue
%service puppetmaster restart
%service puppetqueue restart

%preun server
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del puppetmaster
	/sbin/chkconfig --del puppetqueue
	%service -q puppetmaster stop
	%service -q puppetqueue stop
fi

%post -n openldap-schema-%{name}
%openldap_schema_register %{schemadir}/%{name}.schema -d core
%service -q ldap restart

%postun -n openldap-schema-%{name}
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/%{name}.schema
	%service -q ldap restart
fi


%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/auth.conf
%attr(755,root,root) %{_bindir}/extlookup2hiera
%attr(755,root,root) %{_bindir}/puppet
%{ruby_vendorlibdir}/puppet
%{ruby_vendorlibdir}/puppet.rb
%{ruby_vendorlibdir}/semver.rb
%{ruby_vendorlibdir}/puppetx.rb
%{ruby_vendorlibdir}/puppetx
%{_mandir}/man5/puppet.conf.5*
%{_mandir}/man8/extlookup2hiera.8*
%{_mandir}/man8/puppet*.8*
%exclude %{_mandir}/man8/puppet-ca.8*
%exclude %{_mandir}/man8/puppet-master.8*
%{_examplesdir}/%{name}-%{version}

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/ext

# hiera addons
%{ruby_vendorlibdir}/hiera/backend/puppet_backend.rb
%{ruby_vendorlibdir}/hiera/scope.rb
%{ruby_vendorlibdir}/hiera_puppet.rb

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/puppet
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/puppet
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/puppet.conf
%attr(754,root,root) /etc/rc.d/init.d/puppet
%{systemdtmpfilesdir}/puppet.conf

# These need to be owned by puppet so the server can write to them.
%dir %attr(755,puppet,puppet) %{_localstatedir}/run/%{name}
%dir %attr(750,puppet,puppet) %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/lib/%{name}

%files server
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/manifests
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/fileserver.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/puppetmaster
%attr(754,root,root) /etc/rc.d/init.d/puppetmaster
%attr(754,root,root) /etc/rc.d/init.d/puppetqueue
%{_mandir}/man8/puppet-ca.8*
%{_mandir}/man8/puppet-master.8*

%files -n openldap-schema-%{name}
%defattr(644,root,root,755)
%{schemadir}/*.schema

%files -n vim-syntax-%{name}
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/puppet.vim
%{_datadir}/vim/syntax/puppet.vim
