
#TODO:
#	- coexistence qt4-qsa with qsa
#	- pkgconfig for qt4-qsa

Summary:	Qt Script for Applications
Summary(pl):	Qt Script for Applications - jêzyk skryptowy dla aplikacji Qt
Name:		qt4-qsa
Version:	1.2.1
Release:	0.1
License:	GPL v2
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qsa/source/qsa-x11-opensource-%{version}.tar.gz
# Source0-md5:	46a05bb09346b04cf470dd1a3778c9a0
URL:		http://www.trolltech.com/products/qsa/index.html
BuildRequires:	QtCore-devel
BuildRequires:	qmake
Requires:	QtCore
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautocompressdoc 	*.xml

%description
QSA is a Qt extension that allows developers to make their C++
applications scriptable using an interpreted scripting language, Qt
Script (based on ECMAScript/JavaScript).

%description -l pl
QSA jest rozszerzeniem Qt, które umo¿liwia programistom tworzenie
aplikacji C++, które mog± byæ kontrolowane za pomoc± intepretowanego
jêzyka Qt Script (opartego o ECMAScript/JavaScript).

%package doc
Summary:	Documentation for QSA
Summary(pl):	Dokumentacja dla QSA
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for Qt Script in HTML format.

%description doc -l pl
Dokumentacja do Qt Script w formacie HTML.

%package devel
Summary:	QSA - header files
Summary(pl):	QSA - pliki nag³ówkowe
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt-devel

%description devel
Header files for applications using Qt Script.

%description devel -l pl
Pliki nag³ówkowe dla aplikacji wykorzystuj±cych Qt Script.

%package examples
Summary:	QSA - examples for developers
Summary(pl):	QSA - przyk³adowe programy dla programistów
Group:		X11/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	qt-devel

%description examples
Examples of Qt Script usage for developers.

%description examples -l pl
Przyk³adowe sposoby wykorzystania Qt Script dla programistów.

%prep
%setup -q -n qsa-x11-opensource-%{version}

%build
QTBINDIR=%{_libdir}/qt4/bin
export QTDIR=%{_prefix}
export PATH=$QTBINDIR:$PATH
export QTINC=%{_includedir}/qt4
export QTLIB=%{_libdir}
./configure -release -prefix %{_prefix}
%{__make} -e \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/qt4
install -d $RPM_BUILD_ROOT%{_includedir}/qt4
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/qsa

%{__make} install -e \
	INSTALL_ROOT=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_prefix}/doc/html $RPM_BUILD_ROOT%{_defaultdocdir}/qsa
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

#
# Examples
#
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#remove uneeded files
rm -f qsa.prf
find . -name "Makefile.*" | xargs rm -f
find . -name ".obj*" | xargs rm -rf
find . -name "*.o" | xargs rm -rf
find . -name ".ui*" | xargs rm -rf
find . -name ".moc*" | xargs rm -rf
find . -name ".rcc" | xargs rm -rf

#remove load entry from .pro files
find . -name "*.pro" | xargs sed -i "/..\/qsa/d"
cd -

#
# Includes
#
mv $RPM_BUILD_ROOT%{_includedir}/*.h $RPM_BUILD_ROOT%{_includedir}/qt4
install -p -m 644 src/ide/qsworkbench.h $RPM_BUILD_ROOT%{_includedir}/qt4
install -p -m 644 src/qsa/qsutilfactory.h $RPM_BUILD_ROOT%{_includedir}/qt4

#
# mkspecs
#
mv $RPM_BUILD_ROOT%{_prefix}/mkspecs $RPM_BUILD_ROOT%{_datadir}/qt4

#
# Prepare files list
#
ifecho () {
	res=`echo $2 | sed "s:$RPM_BUILD_ROOT::g"`

	if [ -d "$2" ]; then
		echo "%%dir $res" >> $1.files
	elif [ -x "$2" ] ; then
		echo "%%attr(755,root,root) $res" >> $1.files
	elif [ -f "$2" ]; then
		echo "$res" >> $1.files
	else
		echo "Error while generating files list!"
		echo "$2: no such file or direcotry!"
		return 1
	fi
}

rm -f %{name}-examples.files
FILES=`find $RPM_BUILD_ROOT%{_examplesdir}`
for file in $FILES; do ifecho %{name}-examples $file; done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files doc
%defattr(644,root,root,755)
%dir %{_defaultdocdir}/qsa
%dir %{_defaultdocdir}/qsa/html
%{_defaultdocdir}/qsa/html/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_datadir}/qt4/mkspecs/features
%{_includedir}/qt4/*.h

%files examples -f %{name}-examples.files
%defattr(644,root,root,755)
