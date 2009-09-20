Summary:	An SMTP client
Name:		msmtp
Version:	1.4.18
Release:	%mkrel 1
License:	GPLv3
Group:		System/Servers
URL:		http://msmtp.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/msmtp/%{name}-%{version}.tar.bz2
Source1:	msmtprc
BuildRequires:	openssl-devel >= 0:0.9.6
BuildRequires:	libgcrypt-devel >= 0:1.2.0
Provides:	sendmail-command
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
msmtp is an SMTP client that one can use with mail user agents that 
that contain no mail transfer capability (e.g., Mutt).

Supported features:
- sendmail compatible interface (command line options and exit codes)
- SMTP AUTH methods PLAIN, LOGIN, CRAM-MD5 and EXTERNAL
  (and GSSAPI, DIGEST-MD5 and NTLM when compiled with GNU SASL support)
- TLS encrypted connections with the GnuTLS or OpenSSL libraries
  (including server certificate verification and the possibility to send
  a client certificate)
- LMTP support
- DSN (Delivery Status Notification) support
- RMQS (Remote Message Queue Starting) support (ETRN keyword)
- PIPELINING support for increased transmission speed
- IPv6 support
- support for multiple accounts

%prep
%setup -q

%build
%configure2_5x --with-ssl=openssl --disable-gsasl
%{__make}

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_sysconfdir}
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/msmtprc
chmod 644 %{buildroot}/%{_sysconfdir}/msmtprc

%find_lang %name

%post
%_install_info %{name}.info
update-alternatives \
	--install %{_sbindir}/sendmail sendmail-command %{_bindir}/msmtp 5 \
	--slave %{_libdir}/sendmail sendmail-command-in_libdir %{_bindir}/msmtp

%preun
%_remove_install_info %{name}.info
if [ $1 = 0 ]; then
        update-alternatives --remove sendmail-command %{_bindir}/msmtp
fi

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-, root, root, 0755)
%doc README THANKS NEWS COPYING AUTHORS doc/msmtp.pdf doc/msmtprc-user.example
%doc doc/msmtp.html doc/Mutt+msmtp.txt doc/msmtprc-system.example scripts/msmtpqueue
%config(noreplace) %{_sysconfdir}/msmtprc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*
