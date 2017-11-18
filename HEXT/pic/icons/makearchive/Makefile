#!/bin/make -f
#

ICONDIR = $(SHS)/icons
ARCHIVE = SVGIcons.index
TARGETDIR = $(HH)/config/Icons
NETTYPES = SOP COP2 CHOP VOP DOP POPO ROP OBJ

default:	install

# This cleans up after some old copying code. It should be left in for a while.
clobber:
	cd $(ICONDIR) && \
	    for i in common/*.svg; do \
		for dir in $(NETTYPES); do \
		    if [ -e "$${dir}/`basename $${i}`" ]; then \
			bn=`basename $${i}` && \
			o=`svn status $${dir}/$${bn}` && \
			if [ "`echo $${o} | tr -s ' ' | cut -d ' ' -f 1`" \
			    = "?" ]; then \
			    rm $${dir}/$${bn} ; \
			fi \
		    fi \
		done \
	    done

clean: clobber

install:
	if [ -d $(ICONDIR) ]; then \
	    $(DEVROOT)/bin/svgarchivemaker $(ICONDIR) && \
		mkdir -p $(TARGETDIR) && \
		mv $(ICONDIR)/$(ARCHIVE) $(TARGETDIR) ; \
	fi
