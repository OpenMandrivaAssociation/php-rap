%define base_name   rap 
%define name        php-%{base_name}
%define version     0.9.4
%define fileversion 094
%define release     %mkrel 2

# php dependencies extraction is utterly stupid, it consider every external 
# statement as pear dependency
%define _requires_exceptions pear(/usr/share/php-adodb/adodb.inc.php)

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    RDF API for PHP
License:    LGPL
Group:      Development/Other
URL:        http://www.wiwiss.fu-berlin.de/suhl/bizer/rdfapi
Source:     http://prdownloads.sourceforge.net/rdfapi-php/%{base_name}-v%{fileversion}.tar.bz2
Patch0:     %{name}-0.9.1.fhs.patch
Patch1:     %{name}-0.9.4.external-adodb.patch
Patch2:     %{name}-0.9.1.MoveNext.patch
Patch3:     %{name}-0.9.1.add.patch
Requires:   php-adodb >= 1:4.64-1mdk
BuildArch:  noarch

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
%patch0 -p 1
%patch1 -p 1
%patch2 -p 1
%patch3 -p 0
find . -type d -name CVS | xargs rm -rf
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

