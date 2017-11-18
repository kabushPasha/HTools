#!/bin/make -f
#

APPNAME = svgarchivemaker
TAGNUM  = -c
LIBTYPE = ds

#-----------------------------------------------------------------------

CPPFILES	= archivemaker.C

ICONDIR = $(DEV_SUPPORT)/config/Icons

LIBRARIES = \
	$(DEV_USOLIB)/libUT.a

DEVLIBS   = \
    -lFS \
    -lUT \
    -lVM \
    -ltools \
    -lSYS

PRODLIBS = -lHoudiniUT
HUGELIBS = -lHoudiniALL

SYSLIBS = $(SYSLIBBASE)

#-----------------------------------------------------------------------

MAKEINC = $(SRCROOT)/houdini/make
include $(MAKEINC)/C++MakeApp

DEV_BIN	= $(DEVROOT)/bin
