#! /usr/bin/env python
# coding: utf-8
#
# CCI's boto convenience functions.
#
# SVN: $Id: cci_boto.py 43293 2014-08-18 17:40:22Z svnsync $
# Created: 2014.06.11
# Copyright: Steven E. Pav, 2014
# Author: Steven E. Pav
# Comments: Steven E. Pav

from boto.glacier import connect_to_region
import time
from os.path import isfile
from datetime import datetime

# copied from glacier.py distributed with boto:
def connect(region, debug_level=0, access_key=None, secret_key=None):
    """ Connect to a specific region """
    layer2 = connect_to_region(region,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               debug=debug_level)
    if layer2 is None:
        raise Exception('Invalid region %s, or bad creds' % region)
    return layer2

def fetch_vault(layer2, vault_name):
    """ Internal get_vault """
    vault = layer2.get_vault(vault_name)
    if vault is None :
        raise Exception('Unknown vault %s' % vault_name)
    return vault

def upload_files(layer2, vault_name, filenames, verbosity=1):
    my_vault = layer2.get_vault(vault_name)
    okfn = [fn for fn in filenames if isfile(fn)]
    outids = [my_vault.upload_archive(fn, description=fn) for fn in okfn]
    if verbosity > 0:
        for iii in range(len(okfn)):
            print 'Uploading %s to %s, id=%s' % (okfn[iii], vault_name, outids[iii])
    return outids

def init_inventory_job(layer2, vault_name):
    """ Initiate a request for vault_inventory """
    vault = fetch_vault(layer2, vault_name)
    job_id = vault.retrieve_inventory()
    return job_id

def init_retrieval_job(layer2, vault_name, archive_id):
    """ Initiate a request for an archive """
    vault = fetch_vault(layer2, vault_name)
    job_id = vault.retrieve_archive(archive_id)
    return job_id

# but see http://stackoverflow.com/a/14924210/164611
# for a better way to do this kind of thing ...
def wait_job(layer2, vault_name, job_id, sleepsec=60, timeout=86400):
    """ Wait for a job to terminate. """
    t0 = datetime.now()
    vault = fetch_vault(layer2, vault_name)
    while 1:
        job = vault.get_job(job_id)
        if not job.completed:
            tf = datetime.now()
            delta = tf - t0
            if (delta.seconds > timeout):
                # 2FIX: should this just return false?
                raise Exception('timed out')
            time.sleep(sleepsec)
        else:
            break
    wasok = job.completed
    return wasok

def get_inventory(layer2, vault_name):
    """ get inventory of vault, blocking on return. """
    # get inventory:
    job_id = init_inventory_job(layer2, vault_name)
    wasok = wait_job(layer2, vault_name, job_id)
    if not wasok :
        raise Exception('some problem waiting on job')
    return get_job_result(layer2, vault_name, job_id)

def get_job_result(layer2, vault_name, job_id):
    """ Get the job output """
    layer1 = layer2.layer1
    retval = layer1.get_job_output(vault_name, job_id)
    return retval

# module as script
if __name__ == "__main__":
    pass

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
