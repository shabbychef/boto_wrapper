#! /usr/bin/env python
# coding: utf-8
#
# get the vault inventory.
#
# see also:
# http://oksoft.blogspot.com/2013/04/glacier-and-boto.html
#
# SVN: $Id: inventory_vault.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.05
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

import argparse
import os
import cci_boto
import sys

# module as script
if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="get vault inventory to stdout.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    parser.add_argument('--block', '-b', help='whether to block on job completion, before printing. This can can take 4 hours. Defaults to False', action='store_true', default=False)
    parser.add_argument('vault_name', help='the name of the vault to inventory')
    parser.add_argument('job_id', help='the job ID produced by a previous request to inventory this vault; if none given, we initiate an inventory request', nargs='?', default='')
    args = parser.parse_args()

    # connect
    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)
    vault_name = args.vault_name

    # get or initiate job request
    if args.job_id :
        job_id = args.job_id
    else :
        job_id = cci_boto.init_inventory_job(layer2, vault_name)
        print(job_id)

    # now possibly block :
    if args.block :
        wasok = cci_boto.wait_job(layer2, vault_name, job_id)
        if wasok :
            print(cci_boto.get_job_result(layer2, vault_name, job_id))
            sys.exit(0)
        else :
            print 'Some problem waiting on job'
            sys.exit(2)
    elif args.job_id :
        # previously initiated request
        print(cci_boto.get_job_result(layer2, vault_name, job_id))

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
