%global debug_package %{nil}

# compile against kerberos
%define enable_krb5	0
%{?_with_kerberos:	%global enable_krb5 1}
# enable sasl2
# note that sasl2 includes kerberos support via sasl
%define enable_sasl2	1

Name:           neomutt
Version:        20260504
Release:        1
Summary:        A command line mail reader based on Mutt
Group:          Networking/Mail
License:        GPL-2.0-or-later
URL:            https://www.neomutt.org/
Source0:        https://github.com/neomutt/neomutt/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libidn2)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(gpgme)
%if %enable_sasl2
BuildRequires:  pkgconfig(libsasl2)
%endif
%if %enable_krb5
BuildRequires:	krb5-devel
%endif
BuildRequires:  doxygen
BuildRequires:  xsltproc
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  linuxdoc-tools
BuildRequires:  db-devel >= 5.3
BuildRequires:  gettext

Requires:       urlscan
Requires:	mailcap
Requires:       sasl-plug-login
Requires:	sasl-plug-gssapi
Requires:	neomutt-doc

%description
A command line mail reader based on Mutt.

%package doc
Summary:        Documentation and examples for NeoMutt
Group:          Documentation
BuildArch:      noarch

%description doc
This package contains the documentation and examples for NeoMutt.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
#export CC=cc
./configure \
    SENDMAIL=%{_sbindir}/sendmail \
    ISPELL=%{_bindir}/hunspell \
    --lua \
    --gpgme \
    --full-doc \
    --gnutls \
    --docdir=%{_docdir}/%{name}-doc \
    --bdb \
    --pgp \
    --smime \
    --locales-fix \
    --idn2 \
    --pcre2 \
    --zstd \
    --zlib \
    --disable-idn \
    --libdir=%{_libdir} \
    --disable-maintainer-mode \
    --disable-dependency-tracking \
    --with-sqlite=%{_libdir} \
    --with-lock \
    %if %enable_krb5
        --gss \
    %else
        --disable-gss \
    %endif
    %if %enable_sasl2
        --sasl
    %else
        --disable-sasl
	%endif

# neomutt automatically adds /lib and /usr/lib regardless of arch, so this fixes it
sed -i "s|L/lib|L/%{_lib}|g" Makefile
sed -i "s|L/usr/lib|L/usr/%{_lib}|g" Makefile

%make_build

%install
# remove MacOS stuff
rm -r data/account-command/macos-keychain
%make_install
%find_lang %{name}

%files -f %{name}.lang
%license LICENSE.md AUTHORS.md
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files doc
%{_docdir}/%{name}-doc
