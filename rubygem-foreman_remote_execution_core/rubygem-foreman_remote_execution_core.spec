%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_remote_execution_core

Summary: Foreman remote execution - core bits
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.0
Release: 1%{?foremandist}%{?dist}
Group: Development/Libraries
License: GPLv3
URL: http://github.com/theforeman/foreman_remote_execution
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires: %{?scl_prefix}rubygem(net-scp)
Requires: %{?scl_prefix}rubygem(net-ssh)
Requires: %{?scl_prefix}rubygem(foreman_tasks_core)

BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}rubygems-devel

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Ssh remote execution provider code sharable between Foreman and Foreman-Proxy

%package proxy
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Requires:   %{?scl_prefix}rubygem(smart_proxy_dynflow_core) >= 0.1.5
Obsoletes:  %{?scl_prefix}rubygem(smart_proxy_remote_execution_ssh_core) < 0.1.4
Summary:    Foreman proxy intergration package for rubygem-%{gem_name}

%description proxy
Foreman proxy intergration package for rubygem-%{gem_name}

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} - <<EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Make /etc/foreman-proxy/dynflow/bunder.d and store our requirement there
mkdir -p %{buildroot}%{_datadir}/smart_proxy_dynflow_core/bundler.d
cat <<EOF > %{buildroot}%{_datadir}/smart_proxy_dynflow_core/bundler.d/foreman_remote_execution_core.rb
gem 'foreman_remote_execution_core'
EOF

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_spec}

%files proxy
%{_datadir}/smart_proxy_dynflow_core/bundler.d/foreman_remote_execution_core.rb

%files doc
%doc %{gem_docdir}

%changelog
