#! /usr/bin/env python
# coding: utf-8
#
# retrieve all archives in a vault. will try to save to the
# filenamed in the description, if there is one, O/W saves
# to the archive ID
#
# SVN: $Id: retrieve_all.py 43293 2014-08-18 17:40:22Z svnsync $
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
    vault_name = args.vault_name
    save_d = args.directory
    carp(verbosity > 0,"retrieving all of %s to %s" % (vault_name,save_d))

    layer2 = cci_boto.connect(args.region, 0, args.access_key, args.secret_key)

    # do an LS:
    inventory_res = cci_boto.get_inventory(layer2, vault_name)
    carp(verbosity > 0,"inventory is %s" % inventory_res)

    # get the list of archives:
    archive_list = inventory_res['ArchiveList']
    if verbosity > 0:
        dum = [ print ('retrieving %s' % a['ArchiveId']) for a in archive_list ]

    # dictionary from the requested filename to the AID
    fullfn2aid = { (a['ArchiveDescription'] or a['ArchiveId']) : a['ArchiveId'] for a in archive_list }
    # the ArchiveDescription could be a *full* path name; strip it:
    fn2aid = { os.path.basename(k) : v for k, v in fullfn2aid.iteritems() }

    # dictionary from req filename to the archive retrieval req job:
    fn2job = { k : cci_boto.init_retrieval_job(layer2, vault_name, v) for k, v in fn2aid.iteritems() }

    # now wait and get the results
    # 2FIX: add maximum timeout?
    for fname, job in fn2job.iteritems() :
        wasok = cci_boto.wait_job(layer2, vault_name, job.id)
        if wasok :
            carp(verbosity > 0,"fetching %s"%fname)
            vault = cci_boto.fetch_vault(layer2, vault_name)
            retjob = vault.get_job(job.id)
            if retjob.completed :
                filename = os.path.join(save_d,fname)
                retjob.download_to_file(filename)

# module as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="print known vaults to stdout.")
    parser.add_argument('--access_key', help='the AWS Access Key ID; defaults to the environment variable AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID'))
    parser.add_argument('--secret_key', help='the AWS Secret Access Key ID; defaults to the environment variable AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY'))
    parser.add_argument('--region', help='which AWS region; defaults to the environment variable AWS_REGION or us-east-1', default=os.getenv('AWS_REGION','us-east-1'))
    parser.add_argument('--directory','-C', help='The directory to which we save files. Defaults to cwd', default=os.getcwd())
    parser.add_argument('--verbose', '-v', help='the verbosity level.', action='count')

    parser.add_argument('vault_name', help='the name of the vault to inventory')
    args = parser.parse_args()

    main(args)
    sys.exit(0)

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
