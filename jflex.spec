# TODO
# - compile Source1, Source2 in spec (sources in src/)
%include	/usr/lib/rpm/macros.java
Summary:	Fast Scanner Generator
Summary(pl.UTF-8):	Szybki generator skanerów leksykalnych
Name:		jflex
Version:	1.4.1
Release:	0.2
License:	GPL v2
Group:		Development/Languages/Java
# Source0Download: http://jflex.de/download.html
Source0:	http://jflex.de/%{name}-%{version}.tar.gz
# Source0-md5:	9e4be6e826e6b344e84c0434d6fd4b46
Source1:	http://jflex.sourceforge.net/jar/stable/JFlex-%{version}.jar
# Source1-md5:	626c0c66135a48c042d3b35af95d274d
Patch0:		%{name}-anttask.patch
Patch1:		%{name}-notarget.patch
URL:		http://jflex.de/
BuildRequires:	java_cup >= 0.11a
BuildRequires:	java-gcj-compat-devel
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Obsoletes:	jflex-javadoc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# referenced from html
%define		_noautocompressdoc	COPYRIGHT

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

%description -l pl.UTF-8
JFlex to generator analizatorów leksykalnych (znany także jako
generator skanerów) dla Javy, napisany w Javie. Jest odtworzeniem
bardzo przydatnego narzędzia JLex stworzonego przez Elliota Berka w
Princetown University. Z tego, co Vern Paxson stwierdza o swoim
narzędziu flex dla C/C++, nie dzielą one żadnego kodu. JFlex jest
zaprojektowany do pracy wraz z generatorem analizatorów LALR CUP
napisanym przez Scotta Hudsona i javową modyfikacją Berkeley Yacca
BYacc/J autorstwa Boba Jamisona. Może być używane także z innymi
generatorami analizatorów takimi jak ANTLR albo jako samodzielne
narzędzie.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
# use -c because of top-level symlink
%setup -qc

%patch0 -p1
%patch1 -p1

install -d jflex/tools
ln -s %{SOURCE1} jflex/tools/JFlex.jar

%build
export LC_ALL=en_US # source code not US-ASCII
JAVACUPJAR=$(find-jar java_cup)
cd jflex/src
%ant -Dbuild.compiler=extJavac \
	-Dcup.jar=$JAVACUPJAR \
	realclean jar

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a jflex/lib/JFlex.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
# COPYRIGHT contains note about generated code license
%doc jflex/doc/COPYRIGHT jflex/doc/*.{html,css,gif,png}
%{_javadir}/*.jar
