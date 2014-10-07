# boto
#
# VERSION 0.1
#
# boto
#
# docker build -t dregistry:5000/boto .
#
# Created: 2014.03.10
# Copyright: Cerebellum Capital, 2014.
# Author: Steven E. Pav
# Comments: Steven E. Pav

#####################################################
# preamble# FOLDUP
FROM python:2-onbuild

MAINTAINER Steven E. Pav, steven@cerebellumcapital.com
# UNFOLD

#####################################################
# setup# FOLDUP
ENV AWS_ACCESS_KEY_ID AKOQPRSMRE237EXAMPLE
ENV AWS_SECRET_ACCESS_KEY wJaioWlr2JRat/K7MDENG/bPxRfiCYEXAMPLEKEY

ENV AWS_REGION us-west-1

RUN (mkdir -p /opt/boto/bin)
ADD bin/ /opt/boto/bin/
# UNFOLD

#####################################################
# entry and cmd# FOLDUP

# note that a VOLUME is created at *run time*, not during the
# image build. thus you probably should put VOLUME commands
# after *all* RUN commands to avoid confusion: you cannot
# interact with VOLUMES with RUN commands.
#VOLUME ["/tmp/name","/var/foo"]

# set workdir and user
WORKDIR /opt/boto/bin
USER root

# always use array syntax:
ENTRYPOINT ["/opt/boto/bin/list_vaults.py"]

# ENTRYPOINT and CMD are better together:
CMD []
# UNFOLD

#for vim modeline: (do not edit)
# vim:nu:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:syn=Dockerfile:ft=Dockerfile:fo=croql
