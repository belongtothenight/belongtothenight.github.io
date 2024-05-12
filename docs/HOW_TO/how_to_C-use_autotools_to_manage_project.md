# Use Autotools to Manage Project

This guide will show you how to use [Autotools](https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html) to create makefiles and manage your project.

## Problem

When developing C or C++(CXX) projects, often times it is necessary to worry about how the program is built, how to support the same code base for different platforms and OS, how to make sure all the requirements and dependencies are met, and how everything is installed.

## Background

Compilers like [GCC](https://gcc.gnu.org/), [G++](https://directory.fsf.org/wiki/G%2B%2B), [clang](https://clang.llvm.org/) are used to compile C and C++ code. However, when multiple files presents in a project, it can be troublesome to type in all of the files and flags for each and every files. With the help of [Make](https://www.gnu.org/software/make/), developers can code up how project should be compiled, enabling more stable reproducibility. Most personal project should only requires this level of scripting to manage the entire code base. If on the other hand, you have more requirements like what I mentioned in the [Problem](#problem) section, tools like [Autotools](https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html) and [CMake](https://cmake.org/) can greatly help with managing complex project and achieve even more stable reproducibility.

## Solution

### Step 1: Install Requirements

Install git, make, libtool, and automake.

```bash title="Debian OS"
sudo apt update
sudo apt install -y git make libtool automake
```

If newer versions are needed, you can install them from source.

### Step 2: Create Project

Create a new project directory like the following. It is recommended to use git to perform version control along side with the project.

```bash title="Debian OS"
.
├── .gitignore
├── Makefile.am
├── configure.ac
├── m4
│   └── .keepdir
├── readme.md
└── src
    ├── Makefile.am
    ├── lib.c
    ├── lib.h
    └── main.c

2 directories, 9 files
```

One `configure.ac` and `Makefile.am` file is required at the root of the project. The `./configure.ac` file is responsible for finding required dependencies and generating `./configure` script, which generate makefiles for this project. `./Makefile.am` file is responsible for setting up project structure, sort of like `Makefile`. Each subdirectory containing source code requires coreesponding Makefile.am like `./src/Makefile.am`. `./m4` directory is responsible to handle generated intermediate auxiliary files.

### Step 3: Write `configure.ac`

Following is a sample of `configure.ac` file. You can modify it to fit your project.

```m4 title="configure.ac" linenums="1"
AC_PREREQ([2.71])
AC_INIT([hello], [0.0.1], [dachuan516@gmail.com])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE([-Wall -Werror foreign subdir-objects]) # Display all errors, treat warning as error, following minimum GNU policy, enable automake to look into subdirectories
AC_CONFIG_SRCDIR([src])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
AM_PROG_AR

# Checks for programs.
AC_PROG_CC
LT_INIT([disable-static])

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([arpa/inet.h stdio.h stdlib.h string.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_TYPE_SIZE_T
AC_TYPE_INT8_T
AC_TYPE_INT16_T
AC_TYPE_INT32_T
AC_TYPE_INT64_T
AC_TYPE_UINT8_T
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_REALLOC
AC_CHECK_FUNCS([gethostbyname memmove memset socket strerror strtoul])

AC_CONFIG_FILES([Makefile
                 src/Makefile])
AC_OUTPUT
```

- `Line 2`: Set basic information for the project.
- `Line 3`: Set auxiliary directory to hold generated files.
- `Line 4`: Set automake flags. This is not GCC flags.
- `Line 5`: Set source directory. Can have multiple source directories.
- `Line 7`: Set macro holding directory.
- `Line 12`: Set libtool settings.
- `Line 15`: Check for libraries. Not used in this example.
- `Line 17`: Check for header files.
- `Line 20-28`: Check for typedefs, structures, and compiler characteristics.
- `Line 31-33`: Check for library functions.
- `Line 35-36`: Write out all of the `Makefile.am` files.

### Step 4: Write `Makefile.am`

```m4 title="configure.ac" linenums="1"
SUBDIRS = src

EXTRA_DIST = m4/.keepdir
ACLOCAL_AMFLAGS = -I m4 --install

clean-local:
	rm -rf \
		autoscan.log \
		aclocal.m4 \
		autom4te.cache \
		build-aux \
		config.h \
		config.h.in \
		config.h.in~ \
		config.log \
		config.status \
		configure \
		libtool \
		m4/* \
		.deps \
		Makefile.in \
		Makefile \
		stamp-h1 \
		src/*.in \
		src/*.o \
		src/*.la \
		src/*.lo \
		src/main \
		src/.deps \
		src/.libs \
		src/Makefile
	mkdir -p m4
	touch m4/.keepdir
	rm -rf \
		configure~ \
		*.tar.gz
```

- `Line 1`: Set subdirectories to look into.
- `Line 4`: Set extra flags for aclocal.
- `Line 6-36`: Clean up all the generated files. This extends the `make clean` command. Really helpful when you want to clean up everything but the source code.

### Step 5: Write `./src/Makefile.am`

```m4 title="configure.ac" linenums="1"
project = autotools_init_setup_type2
common_cflag = -Wno-implicit-function-declaration -Wextra -Wall -Wfloat-equal -Wundef -Wshadow -Wpointer-arith -Wcast-align -Wstrict-prototypes -Wstrict-overflow=5 -Wwrite-strings -Waggregate-return -Wcast-qual -Wswitch-default -Wswitch-enum -Wconversion -Wunreachable-code -Wformat=2 -O3
common_cxxflag = -Wextra -Wall -Wfloat-equal -Wundef -Wshadow -Wpointer-arith -Wcast-align -Wstrict-overflow=5 -Wwrite-strings -Waggregate-return -Wcast-qual -Wswitch-default -Wswitch-enum -Wconversion -Wunreachable-code -Wformat=2 -O3

# ====================================
# install directory of public:
# - plugins         (.so, .a, .la)
# - libtool library (.so, .a, .la)
# - header          (.h)
# - binary
# NOTE: comment out if not needed of individual install
# NOTE: created directory won't be removed by uninstall
# NOTE: header ladir need to use the library name as prefix
# ====================================
#plugindir 	= $(prefix)/lib/${project}
libdir 		= $(prefix)/lib/${project}
lib_ladir 	= $(prefix)/include/${project}
bindir 		= $(prefix)/bin/${project}

# ====================================
# add library to install as plugin
# NOTE: can't be used with plugin_LTLIBRARIES
# ====================================
lib_LTLIBRARIES = lib.la
# lib_LTLIBRARIES += lib2.la

# ====================================
# add library to install as libtool library
# NOTE: can't be used with lib_LTLIBRARIES
# ====================================
# plugin_LTLIBRARIES = lib.la
# plugin_LTLIBRARIES += lib2.la

# ====================================
# add source to build library
# NOTE: need to use the library name as prefix
# ====================================
lib_la_SOURCES = lib.c
# lib_la_SOURCES += lib2.c
lib_la_HEADERS = lib.h
# lib_la_HEADERS += lib2.h
lib_la_CFLAGS = $(common_cflag)
# lib_la_CFLAGS += -I$(lib_ladir)

# ====================================
# add executable to build
# ====================================
bin_PROGRAMS = main
# bin_PROGRAMS += main2

# ====================================
# add source to build executable
# NOTE: need to use the executable name as prefix
# ====================================
main_SOURCES = main.c
main_CFLAGS = $(common_cflag)
main_LDADD = lib.la
```

- `Line 1-3`: Set variables for later use.
- `Line 15-18`: Set install directories for binaries, libraries, headers, and plugins.
- `Line 24`: Create a library to build named `lib`. If you have multiple libraries, you can add them like `Line 25`.
- `Line 38-43`: Add sources, headers, and compiling flags for the library. Their names should be prefixed with the library name.
- `Line 48`: Create an executable to build named `main`. If you have multiple executables, you can add them like `Line 49`.
- `Line 55-57`: Add sources, compiling flags, and libraries to link for the executable. Their names should be prefixed with the executable name.

### Step 6: Build Project

Execute the following commands to build the project.

```bash linenums="1"
autoreconf -iv
./configure
make
sudo make install
```

`Line 1` can actually be split into multiple steps, but for simplicity, this command is used instead. Also, if you prefer to do with multiple steps, people usually code them into a script `./bootstrap.sh` and execute it instead.

The world of autotools can be a lot more complex than this. However, the following example should give you a good start.

- The entire project to start with can be found in [https://github.com/belongtothenight/autotools_init_setup/tree/main](https://github.com/belongtothenight/autotools_init_setup/tree/main).
- More complex project based on this can be found in [https://github.com/belongtothenight/ACN_Code/tree/main/hw5_c_trace_analyze](https://github.com/belongtothenight/ACN_Code/tree/main/hw5_c_trace_analyze).

Open-sourced and mature projects managed by autotools:

- [https://github.com/LibtraceTeam/wandio](https://github.com/LibtraceTeam/wandio)
- [https://github.com/LibtraceTeam/libtrace](https://github.com/LibtraceTeam/libtrace)
- [https://github.com/kgoldman/ibmtss](https://github.com/kgoldman/ibmtss)
- [https://github.com/tpm2-software/tpm2-tss](https://github.com/tpm2-software/tpm2-tss)

## Reference

1. [How to use autotools (automake, autoconf, aclocal, autoheader) by Daniel Persson](https://youtu.be/3XO0d9Qyc34?si=vo2eT0Znm8kdLPgs)
2. [Introduction to the Autotools, part 1 by David A. Wheeler](https://youtu.be/4q_inV9M_us?si=zBfY6WSWCrLH87ss)

## Error Correction

If you find any mistakes in the document, please create an [Issue](https://github.com/belongtothenight/belongtothenight.github.io/issues) or a [Pull request](https://github.com/belongtothenight/belongtothenight.github.io/pulls) or leave a message in [Discussions](https://github.com/belongtothenight/belongtothenight.github.io/discussions) or send me a mail directly with the mail icon at the bottom right. Thank you!
