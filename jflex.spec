Summary:	Fast Scanner Generator
Summary(pl):	Szybki generator skanerów leksykalnych
Name:		jflex
Version:	1.3.5
Release:	0.1
License:	GPL
Group:		Development/Languages/Java
Source0:	http://jflex.de/%{name}-%{version}.tar.gz
# Source0-md5:	c77a9656aa20979f2268d7443995700f
Patch0:		%{name}-Makefile.patch
URL:		http://jflex.de/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JFlex is a lexical analyzer generator (also known as scanner
generator) for Java(tm), written in Java(tm). It is also a rewrite of
the very useful tool JLex which was developed by Elliot Berk at
Princeton University. As Vern Paxson states for his C/C++ tool flex:
They do not share any code though. JFlex is designed to work together
with the LALR parser generator CUP by Scott Hudson, and the Java
modification of Berkeley Yacc BYacc/J by Bob Jamison. It can also be
used together with other parser generators like ANTLR or as a
standalone tool.

%description -l pl
JFlex to generator analizatorów leksykalnych (znany tak¿e jako
generator skanerów) dla Javy, napisany w Javie. Jest odtworzeniem
bardzo przydatnego narzêdzia JLex stworzonego przez Elliota Berka w
Princetown University. Z tego, co Vern Paxson stwierdza o swoim
narzêdziu flex dla C/C++, nie dziel± one ¿adnego kodu. JFlex jest
zaprojektowany do pracy wraz z generatorem analizatorów LALR CUP
napisanym przez Scotta Hudsona i javow± modyfikacj± Berkeley Yacca
BYacc/J autorstwa Boba Jamisona. Mo¿e byæ u¿ywane tak¿e z innymi
generatorami analizatorów takimi jak ANTLR albo jako samodzielne
narzêdzie.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -n JFlex
for j in $(find . -name "*.jar"); do mv $j $j.no; done
find . -name "*.class" -exec rm {} \;
%patch0

%build
%{__make} -j1 -C src \
	all javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p lib/JFlex.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
