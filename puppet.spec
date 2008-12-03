# TODO
# for man - rst2man.py needed (docutils snap?)
Summary:	Puppet
Summary(pl.UTF-8):	Puppet
Name:		puppet
Version:	0.24.6
Release:	0.1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://reductivelabs.com/downloads/puppet/%{name}-%{version}.tgz
# Source0-md5:	dcc84cd9bc5c411536ab88589079459b
URL:		http://www.reductivelabs.com/projects/puppet/
#BuildRequires:	-devel
BuildRequires:	docutils
BuildRequires:	facter
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby
#%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Puppet.

%description -l pl.UTF-8
Puppet.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ruby_sitelibdir}

ruby install.rb \
	--no-man \
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
