#!/usr/bin/env python

import argparse
import os
import inspect
import sys
import json
import ldap
from datetime import datetime


class FileNotFoundException(Exception):
    pass


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

verbose = False
everbose = False

config_file_default ='/etc/gosa-sieve-vacancies/sync-vacancies.conf.json'
sieve_template_default = '/etc/gosa-sieve-vacancies/sieve-template.tpl'
def parse_args():

    parser = argparse.ArgumentParser(
        description='reads vacancies from ldap and produces sieve-vacancies rules for any found user ')

    parser.add_argument('-c', '--config-file', dest='config_file', nargs='?',
                        default=config_file_default,
                        metavar='config-file',
                        help='Path to configfile defining ldap and sieve settings. Defaults to: ' + config_file_default)

    parser.add_argument('-s', '--sieve-template', dest='sieveTemplate', nargs='?',
                        default=sieve_template_default,
                        metavar='sieve-template',
                        help='Path to sieve-template file defining ldap attributes ')

    parser.add_argument('-d', '--dry-run', dest='dryRun', action='store_true',
                    help='do not write files. Just print resulting sieve file')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='Display  messages')

    parser.add_argument('-ev', '--extra-verbose', dest='everbose', action='store_true',
                        help='Display debugging messages')

    args = parser.parse_args()

    return args


def read_json_conf(filename):
    if verbose:
        print "reading config file " + filename
    content = file_get_contents(filename)
    return json.loads(content, encoding='utf-8')


def read_vacancies_user():
    if ldap_cfg("useTLS"):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

    con = ldap.initialize(ldap_cfg("url"))

    con.simple_bind_s(ldap_cfg("binddn"), ldap_cfg("bindpw"))

    attribs = [s.encode('ascii') for s in ldap_cfg("searchAttributes")]
    results = con.search_s(ldap_cfg("basedn"), ldap.SCOPE_SUBTREE, ldap_cfg("userfilter"), attribs)

    if verbose:
        print "found " + str(len(results)) + " entries"
    return results


def file_get_contents(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundException("Couldn't read " + str(filename))

    with open(filename, mode="r") as f:
            content = f.read()
            return content


def ldap_cfg(key):
    return config["ldap"][key]


def sync_sieve_file(data):
    user = data[1]
    if verbose:
        print "processing user " + str(user["uid"][0])

    # create a map of our search attributes
    attribs = [s.encode('ascii') for s in ldap_cfg("searchAttributes")]
    new_user = {}
    for attrib in attribs:
        new_user[attrib] = user[attrib][0]

    # enrich with proper formatted dates
    start_ts = float(new_user[ldap_cfg("startTsAttribute")])
    end_ts = float(new_user[ldap_cfg("endTsAttribute")])
    new_user["gosaVacationStartDate"] = datetime.utcfromtimestamp(start_ts).strftime('%Y-%m-%d')
    new_user["gosaVacationStopDate"] = datetime.utcfromtimestamp(end_ts).strftime('%Y-%m-%d')

    if everbose:
        print "The Instance that is available in sieve template and userHomePathTemplate config variable"
        print new_user

    # make target paths
    target_directory = str(config["sieve"]["userHomePathTemplate"]).format(**new_user)
    filename = str(config["sieve"]["outFilenameTemplate"]).format(new_user)

    if verbose:
        print "# " + target_directory + filename

    if not args.dryRun:

        if not os.path.isdir(target_directory):
            print "Warn: Sieve user-directory for user "+str(new_user["uid"])+" does not yet exist at " + str(target_directory) + ". Do nothing!"
            return

        # check isActive
        isActive = ldap_cfg("activeWhenMatches") not in ldap_cfg("gosaMailDeliveryMode")

        with open(target_directory + filename, "w") as outfile:
            if isActive:
                outfile.write(sieve_template.format(**new_user))
            else:
                outfile.write("# currently inactive")
    else:
        print "would safe to " + str(target_directory + filename)
        print sieve_template.format(**new_user)


# parse args
args = parse_args()


# enable logging
verbose = args.verbose
everbose = args.everbose
if everbose:
    verbose = True

# read config
config = read_json_conf(args.config_file)
if everbose:
    print str(json.dumps(config, sort_keys=True, indent=4))

# read sieve_template
sieve_template = file_get_contents(args.sieveTemplate)

# read LDAP users
users = read_vacancies_user()
for user in users:
    sync_sieve_file(user),


