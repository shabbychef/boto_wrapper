#! /usr/bin/env python
# coding: utf-8
#
# create a vault in glacier.
#
# SVN: $Id: upload_file.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.05
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

import cci_boto
import argparse
import os
import sys

# module as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="upload a file to a vault.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    parser.add_argument('--verbose', '-v', help='the verbosity level.', action='count')
    parser.add_argument('vault_name', help='the name of the vault to be created')
    parser.add_argument('filename', nargs='+', help='the name of the file(s) to be uploaded')
    args = parser.parse_args()

    # connect
    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)
    print cci_boto.upload_files(layer2, args.vault_name, args.filename, args.verbose)
    sys.exit(0)

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
