#! /usr/bin/env python
# coding: utf-8
#
# create a vault in glacier.
#
# SVN: $Id: list_vaults.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.05
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

import argparse
import os
import cci_boto

# module as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="print known vaults to stdout.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    args = parser.parse_args()

    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)
    vaults = layer2.list_vaults()
    for v in vaults:
        print v

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
