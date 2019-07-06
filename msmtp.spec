Summary:	An SMTP client
Name:		msmtp
Version:	1.8.4
Release:	1
License:	GPLv3
Group:		System/Servers
URL:		http://msmtp.sourceforge.net/
Source0:	https://marlam.de/msmtp/releases/%{name}-%{version}.tar.xz
#source mirror: https://github.com/marlam/msmtp-mirror
Source1:	msmtprc
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:  pkgconfig(libidn2)
BuildRequires:  pkgconfig(libsecret-1)
Provides:	sendmail-command

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
%make_install

mkdir -p %{buildroot}%{_sysconfdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/msmtprc
chmod 644 %{buildroot}%{_sysconfdir}/msmtprc

%find_lang %name

%post
%_install_info %{name}.info
update-alternatives \
	--install %{_sbindir}/sendmail sendmail-command %{_bindir}/msmtp 5 \
	--slave %_prefix/lib/sendmail sendmail-command-in_libdir %{_bindir}/msmtp

%preun
%_remove_install_info %{name}.info
if [ $1 = 0 ]; then
        update-alternatives --remove sendmail-command %{_bindir}/msmtp
fi
%files -f %name.lang
%doc README THANKS NEWS COPYING AUTHORS doc/msmtprc-user.example
%doc doc/msmtprc-system.example scripts/msmtpqueue
%config(noreplace) %{_sysconfdir}/msmtprc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*


%changelog
* Wed May 02 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.28-1
+ Revision: 795144
- version update 1.4.28

* Mon Jan 09 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.27-1
+ Revision: 759176
- version update 1.4.27

* Mon Nov 28 2011 Alexander Khrukin <akhrukin@mandriva.org> 1.4.26-1
+ Revision: 734955
- version update 1.4.26

* Wed May 11 2011 Sandro Cazzaniga <kharec@mandriva.org> 1.4.24-1
+ Revision: 673684
- update 1.4.24
- update %%doc

* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.4.23-1
+ Revision: 645308
- update to new version 1.4.23

* Sat Aug 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.4.21-1mdv2011.0
+ Revision: 567272
- update to 1.4.21
- drop patch0, fixed upstream

* Mon Apr 05 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.4.20-2mdv2010.1
+ Revision: 531865
- P0: properly handle subjectAltNames with openssl 1.0.0.
- Rebuild for new openssl

* Tue Mar 23 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.4.20-1mdv2010.1
+ Revision: 526794
- update msmtp to 1.4.20

* Tue Nov 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.19-1mdv2010.1
+ Revision: 466865
- 1.4.19 (fixes CVE-2009-3942)

* Tue Sep 22 2009 Michael Scherer <misc@mandriva.org> 1.4.18-2mdv2010.0
+ Revision: 447268
- fix link for sendmail, correct bug #53895

* Sun Sep 20 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.18-1mdv2010.0
+ Revision: 445287
- update to new version 1.4.18

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.4.17-2mdv2010.0
+ Revision: 440162
- rebuild

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 1.4.17-1mdv2009.1
+ Revision: 324877
- update to new version 1.4.17

* Mon Jul 28 2008 Funda Wang <fwang@mandriva.org> 1.4.16-1mdv2009.0
+ Revision: 250777
- update to new version 1.4.16

* Sun Jun 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.15-1mdv2009.0
+ Revision: 216818
- 1.4.15

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Aug 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.13-1mdv2008.0
+ Revision: 72093
- 1.4.13
- the license was changed to GPLv3

* Tue Jul 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.12-1mdv2008.0
+ Revision: 50934
- 1.4.12

* Thu May 03 2007 Michael Scherer <misc@mandriva.org> 1.4.11-1mdv2008.0
+ Revision: 21504
- update to 1.4.11

