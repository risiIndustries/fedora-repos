Summary:        Fedora package repositories
Name:           fedora-repos
Version:        29
Release:        0.6%{?_module_build:%{?dist}}
License:        MIT
Group:          System Environment/Base
URL:            https://pagure.io/fedora-repos/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Requires:       fedora-repos-rawhide = %{version}-%{release}
Requires:       fedora-gpg-keys = %{version}-%{release}
Obsoletes:      fedora-repos-anaconda < 22-0.3
Obsoletes:      fedora-repos-modular < 29-0.6
Provides:       fedora-repos-modular = %{version}-%{release}
BuildArch:      noarch

%description
Fedora package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3
Obsoletes:      fedora-repos-rawhide-modular < 29-0.6
Provides:       fedora-repos-rawhide-modular = %{version}-%{release}

%description rawhide
This package provides the rawhide repo definitions.


%package -n fedora-gpg-keys
Summary:        Fedora RPM keys
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description -n fedora-gpg-keys
This package provides the RPM signature keys.


%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing.repo
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing-modular.repo

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo
%config(noreplace) /etc/yum.repos.d/fedora-rawhide-modular.repo


%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*


%changelog
* Tue Jul 31 2018 Stephen Gallagher <sgallagh@redhat.com> - 29-0.6
- Merge modular repos into the main package
- Part of https://fedoraproject.org/wiki/Changes/ModulesForEveryone

* Fri May 18 2018 Mohan Boddu <mboddu@redhat.com> - 29-0.5
- Baseurl fixes

* Mon Mar 12 2018 Stephen Gallagher <sgallagh@redhat.com> - 29-0.4
- Move modular repos to a subpackage

* Sat Mar 10 2018 Dennis Gilmore <dennis@ausil.us> - 29-0.3
- fix up the baseurls in updates-testing

* Sat Feb 24 2018 Dennis Gilmore <dennis@ausil.us> - 29-0.2
- add changes for the new modular setup

* Mon Feb 19 2018 Mohan Boddu <mboddu@redhat.com> - 29-0.1
- Setup for rawhide being f29
