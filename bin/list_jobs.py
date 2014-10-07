#! /usr/bin/env python
# coding: utf-8
#
# get list of jobs on a given vault.
#
# see also:
# http://oksoft.blogspot.com/2013/04/glacier-and-boto.html
#
# SVN: $Id: list_jobs.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.05
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

import argparse
import os
import cci_boto

# module as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get vault inventory to stdout.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    parser.add_argument('--completed', help='show completed jobs; default false.', dest='completed', action='store_true')
    parser.add_argument('--no-completed', help='do not show completed jobs; default true.', dest='completed', action='store_false')
    parser.add_argument('vault_name', help='the name of the vault to query')
    parser.set_defaults(completed=False)
    args = parser.parse_args()

    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)
    layer1 = layer2.layer1

    print layer1.list_jobs(args.vault_name, completed=args.completed)

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
