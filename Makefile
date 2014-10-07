# basic makefile for building docker images
#
# boto project
#
# Author: Steven E. Pav
# Created: 2014.03.05
# $Id: Makefile 42312 2014-06-12 18:12:38Z steven $

.PHONY: run cid img

USERNAME 							 = docker_reg:5000
BASENAME 							?= boto

ADD_FILES 						 = $(wildcard *.py)

DNS_SERVERS 					?= 

DOCKER 								?= docker
DOCKER_DAEMON_FLAGS 	?= 
# needed to get container's clock to sync host's
DOCKER_TIME_FLAGS 		 = -v /etc/localtime:/etc/localtime:ro
DOCKER_DNS_FLAGS 			?= $(patsubst %,--dns=%,$(DNS_SERVERS))
DOCKER_MOUNT_FLAGS 		?= 
DOCKER_RUN_FLAGS 			?= $(DOCKER_DNS_FLAGS) $(DOCKER_TIME_FLAGS) $(DOCKER_MOUNT_FLAGS)
DOCKER_BUILD_FLAGS 		?= --rm

###############################

help :
	@-echo "make img         :   docker build, generating $(USERNAME)/$(BASENAME)"
	@-echo "make attach      :   docker run bash in the contaner, useful for poking around"
	@-echo "make clean       :   rm $(BASENAME).img, the sentinel for make img"

list_vaults : $(BASENAME).img
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) run \
		$(DOCKER_RUN_FLAGS) \
		-t -i --rm \
		--entrypoint="/opt/boto/bin/list_vaults.py" $(USERNAME)/$(BASENAME)

all: img

img: $(BASENAME).img

$(BASENAME).img : Dockerfile $(ADD_FILES)
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) build \
		$(DOCKER_BUILD_FLAGS) -t $(USERNAME)/$(BASENAME) .
	touch $@

attach : $(BASENAME).attach

%.attach : %.img
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) run \
		$(DOCKER_RUN_FLAGS) \
		--rm -i -t \
		--entrypoint=/bin/bash $(USERNAME)/$* "-i"

inspect : $(BASENAME).inspect

%.inspect : %.cid
	$(DOCKER) inspect `cat $<`

volumefrom : $(BASENAME).cid
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) run \
		$(DOCKER_RUN_FLAGS) \
		--rm -i -t \
		--volumes-from=`cat $<` \
		--entrypoint=/bin/bash $(USERNAME)/$(BASENAME) "-i"

push : $(BASENAME).push

%.push : %.img
	$(DOCKER) push $(USERNAME)/$*

run : cid

cid : $(BASENAME).cid

%.cid : %.img
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) run \
		$(DOCKER_RUN_FLAGS) \
		-t \
		-d --cidfile=$@ --name=$* \
		$(USERNAME)/$*
	$(DOCKER) ps | grep -e "$(USERNAME)/$*"

%.recid : %.cid
	[[ -n $$($(DOCKER) top $$(cat $<) 2>/dev/null) ]] || $(DOCKER) restart $$(cat $<)

nocid : $(BASENAME).nocid

%.nocid : %.img
	$(DOCKER) $(DOCKER_DAEMON_FLAGS) run \
		$(DOCKER_RUN_FLAGS) \
		-t -i --rm \
		--name=$* \
		$(USERNAME)/$*

stop : $(BASENAME).stop 

%.stop :
	$(DOCKER) ps --no-trunc | grep $* | awk '{print $$1}' | xargs $(DOCKER) stop

rm : $(BASENAME).rm

%.rm : %.cid
	$(DOCKER) stop `cat $<`
	$(DOCKER) rm `cat $<`
	rm $<

suggestions :
	@echo make img
	@echo make cid
	@echo make run

clean :
	-rm *.img
	-rm *.cid

realclean: clean 

#for vim modeline: (do not edit)
# vim:ts=2:sw=2:tw=79:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:tags=tags;:syn=make:ft=make:ai:si:cin:nu:fo=croql:cino=p0t0c5(0:
