%define base_name rap 
%define fileversion 096

# php dependencies extraction is utterly stupid, it consider every external 
# statement as pear dependency
%define _requires_exceptions pear(/usr/share/php-adodb/adodb.inc.php)\\|pear(config.php)

Summary:	RDF API for PHP
Name:		php-%{base_name}
Version:	0.9.6
Release:	%mkrel 6
License:	LGPL
Group:		Development/Other
URL:		http://www.wiwiss.fu-berlin.de/suhl/bizer/rdfapi
Source:		http://prdownloads.sourceforge.net/rdfapi-php/%{base_name}-v%{fileversion}.zip
Patch0:		%{name}-fhs.diff
Patch1:		%{name}-0.9.4.external-adodb.patch
Patch2:		%{name}-0.9.1.MoveNext.patch
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
