%define base_name rap 
%define fileversion 096

# php dependencies extraction is utterly stupid, it consider every external 
# statement as pear dependency
%define _requires_exceptions pear(/usr/share/php-adodb/adodb.inc.php)\\|pear(config.php)

Summary:	RDF API for PHP
Name:		php-%{base_name}
Version:	0.9.6
Release:	%mkrel 9
License:	LGPL
Group:		Development/Other
URL:		http://www.wiwiss.fu-berlin.de/suhl/bizer/rdfapi
Source:		http://prdownloads.sourceforge.net/rdfapi-php/%{base_name}-v%{fileversion}.zip
Patch0:		%{name}-fhs.diff
Patch1:		%{name}-0.9.4.external-adodb.patch
Patch2:		%{name}-0.9.6.MoveNext.patch
Patch3:		%{name}-add.diff
Requires:	php-adodb >= 1:4.64-1mdk
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RAP is a software package for parsing, searching, manipulating, serializing and
serving RDF models.

Its features include:
* statement-centric methods for manipulating an RDF model as a set of RDF
  triples
* resource-centric methods for manipulating an RDF model as a set of resources
* ontology-centric methods for manipulating an RDF model through vocabulary
  specific methods
* integrated RDF/XML, N3 and N-TRIPLE and GRDDL parser
* integrated RDF/XML, N3 and N-TRIPLE serializer
* in-memory or database model storage
* support for the RDQL query language
* inference engine supporting RDF-Schema reasoning and some OWL entailments
* integrated RDF server providing similar functionality as the Joseki RDF
  server
* graphical user-interface for managing database-backed RDF models
* support for common vocabularies
* drawing graph visualizations

%prep

%setup -q -n rdfapi-php

for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p 1
%patch1 -p 1
%patch2 -p 1
%patch3 -p 0

find . -type f | perl -ne 'chomp; print "$_\n" if -T $_' | xargs perl -pi -e 'tr/\r//d'
rm -rf api/util/adodb

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
cp -pr api %{buildroot}%{_datadir}/%{name}
cp -pr netapi %{buildroot}%{_datadir}/%{name}
cp -pr test %{buildroot}%{_datadir}/%{name}
cp -pr tools %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_datadir}/%{name}/netapi/config.inc \
    %{buildroot}%{_sysconfdir}/%{name}/netapi.conf
mv %{buildroot}%{_datadir}/%{name}/tools/rdfdb-utils/config.inc.php \
    %{buildroot}%{_sysconfdir}/%{name}/rdfdb-utils.conf
rm -f %{buildroot}%{_datadir}/%{name}/netapi/.htaccess
rm -f %{buildroot}%{_datadir}/%{name}/netapi/apache.htaccess

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc doc/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}


%changelog
* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-9mdv2012.0
+ Revision: 695455
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-8
+ Revision: 646676
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Funda Wang <fwang@mandriva.org> 0.9.6-7mdv2011.0
+ Revision: 629948
- rediff movenext patch

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for php-5.3.5
    - rebuild
    - rebuilt for php-5.3.2RC1
    - rebuilt against php-5.3.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdv2009.0
+ Revision: 239181
- 0.9.6
- rediffed P0,P3

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.4-2mdv2007.0
- fix wrong pear dependency

* Thu Aug 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.4-1mdv2007.0
- new version
- rediff patch 1

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-7mdk 
- new patch for powl

* Wed Jun 29 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-6mdk 
- requires php-adodb >= 1:4.64-1mdk
- only fix encoding for text files

* Wed Jun 29 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-5mdk 
- removed .htaccess files

* Wed Jun 29 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-4mdk 
- rediff external adodb patch
- better fhs patch
- requires php-adodb

* Thu Jun 16 2005 Pascal Terjan <pterjan@mandriva.org> 0.9.1-3mdk
- fix failure when calling MoveNext (P2)
- mark /etc/php-rap.conf as config file

* Thu Jun 16 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-2mdk 
- fix external adodb patch

* Wed Jun 15 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.1-1mdk 
- first mdk release

