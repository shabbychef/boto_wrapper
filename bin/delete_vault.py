#! /usr/bin/env python
# coding: utf-8
#
# delete all archives in a vault. be very careful with this!
#
# SVN: $Id: delete_vault.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.05
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

from __future__ import print_function
import argparse
import os
import cci_boto
import sys

def carp(cond,str):
    """ carp if true """
    if cond:
        print(str)

def main(args):
    """ the main action """
    verbosity = args.verbose
    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)
    vault_name = args.vault_name
    carp(verbosity > 1,"deleting %s" % vault_name)

    # do an LS:
    inventory_res = cci_boto.get_inventory(layer2, vault_name)
    carp(verbosity > 1,"inventory is %s" % inventory_res)

    # get the list of archives:
    archive_list = inventory_res['ArchiveList']
    if verbosity > 1:
        dum = [ print ('deleting %s' % a['ArchiveId']) for a in archive_list ]

    # delete them all
    noret = [ layer2.layer1.delete_archive(vault_name, a['ArchiveId']) for a in archive_list ]
    carp(verbosity > 1,noret)

    # now delete the vault:
    print (layer2.layer1.delete_vault(vault_name))

# module as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="print known vaults to stdout.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    parser.add_argument('--mxyzptlk', help='you must set this flag, otherwise the code will not run, due to the extreme danger of this operation. Defaults to False (unset)', action='store_true', default=False)
    parser.add_argument('--verbose', '-v', help='the verbosity level.', action='count')
    parser.add_argument('vault_name', help='the name of the vault to inventory')
    args = parser.parse_args()

    if args.mxyzptlk :
        main(args)
    else:
        print ('this is a dangerous operation, set the proper flag')
        parser.print_help()
        sys.exit(2)

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
