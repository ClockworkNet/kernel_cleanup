#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Evaluate installed Linux kernel packages and purge any that are not the
current version or the newest version.
"""

# Standard library
from __future__ import absolute_import, division, print_function
import argparse
import os
import platform
import re
import sys

# Third-party
import apt
import apt_pkg


RE_SIMPLE_VERSION = re.compile(r"([\d.]+-\d+)")
RE_SIMPLE_NAME = re.compile(r"^([^0-9]+)-[0-9]")
LINUX_PACKAGES = ["linux-headers", "linux-image", "linux-image-extra"]


def validate_and_mark(apt_cache, data):
    """Validate and mark packages to be purged.
    """
    for linux_package in sorted(list(data.keys())):
        statuses = data[linux_package]
        if (("current" not in data[linux_package] or
                len(data[linux_package]["current"]) < 1) and
                "purge" in data[linux_package]):
            sys.stderr.write("WARNING: Skipping \"{0}\": there are entries"
                             " within \"purge\", but none within \"current\"!"
                             "\n".format(linux_package))
            del data[linux_package]
            continue
        if "purge" in statuses:
            for name in statuses["purge"]:
                package = apt_cache[name]
                package.mark_delete(purge=True)
    return apt_cache, data


def print_data(data):
    """Print linux package statuses.
    """
    for linux_package in sorted(list(data.keys())):
        statuses = data[linux_package]
        print(linux_package)
        for status in sorted(list(statuses.keys())):
            packages = statuses[status]
            print("{0:4}{1}".format("", status))
            packages.sort()
            for package in packages:
                if status == "newest":
                    print("{0:8}{1}".format("", package[0]))
                else:
                    print("{0:8}{1}".format("", package))
    print()


def compare_versions(args, apt_cache, kernel_ver):
    """Compare Linux packages to kernel version. Mark those that are neither
    the current nor the newest for purging.
    """
    data = dict()

    def prep_data(simple_name, status):
        """Prep data structure."""
        if simple_name not in data:
            data[simple_name] = dict()
        if status not in data[simple_name]:
            data[simple_name][status] = list()

    for name in apt_cache.keys():
        try:
            simple_name = RE_SIMPLE_NAME.match(name).group(1)
        except KeyboardInterrupt:
            raise
        except SystemExit:
            raise
        except:
            continue
        if simple_name not in LINUX_PACKAGES:
            continue
        package = apt_cache[name]
        if not package.is_installed:
            continue
        version = package.versions[0].version
        simple_version = RE_SIMPLE_VERSION.match(version).group(1)
        kernel_compare = apt_pkg.version_compare(kernel_ver, simple_version)
        if kernel_compare == 0:
            prep_data(simple_name, "current")
            data[simple_name]["current"].append(name)
        if kernel_compare > 0:
            prep_data(simple_name, "purge")
            data[simple_name]["purge"].append(name)
        elif kernel_compare < 0:
            prep_data(simple_name, "newest")
            if len(data[simple_name]["newest"]) == 0:
                data[simple_name]["newest"].append([name, version])
            else:
                for newest_name, newest_ver in data[simple_name]["newest"]:
                    if newest_name == name:
                        continue
                    package_compare = apt_pkg.version_compare(version,
                                                              newest_ver)
                    if package_compare == 0:
                        # append
                        data[simple_name]["newest"].append([name, version])
                    elif package_compare > 0:
                        # purge (now former) newest package
                        prep_data(simple_name, "purge")
                        data[simple_name]["purge"].append(newest_name)
                        # remove former newest from neest
                        data[simple_name]["newest"].remove([newest_name,
                                                            newest_ver])
                        # append package to newest
                        data[simple_name]["newest"].append([name, version])
                    elif package_compare < 0:
                        prep_data(simple_name, "purge")
                        data[simple_name]["purge"].append(name)
    return data


def get_kernel_version(args):
    """Get Debian/Ubuntu kernel version.
    """
    kernel_version_long = platform.uname()[2]
    try:
        kernel_version = RE_SIMPLE_VERSION.match(kernel_version_long).group(1)
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except:
        sys.stderr.write("ERROR: Unexpected (non Ubuntu?) Linux version: "
                         "%s\n" % platform.platform())
        sys.exit(1)
    if not args.quiet:
        print(platform.platform())
        print()
    return kernel_version


def parser_setup():
    """Instantiate and return an ArgumentParser instance.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    apg = ap.add_mutually_exclusive_group()
    apg.add_argument("-n", "--dryrun", action="store_true",
                     help="Don't actually delete anything; just print what "
                     "would've been deleted. Implies verbose (not quiet).")
    apg.add_argument("-q", "--quiet", action="store_true",
                     help="Run silent, run deep.")
    args = ap.parse_args()
    return args


def main():
    args = parser_setup()
    apt_cache = apt.Cache()
    apt_cache.open()
    kernel_ver = get_kernel_version(args)
    data = compare_versions(args, apt_cache, kernel_ver)
    apt_cache, data = validate_and_mark(apt_cache, data)
    if not args.quiet:
        print_data(data)
    if not args.dryrun:
        if args.quiet:
            # replace stdout and stderr with /dev/null
            # (I was unable to find a better way that worked)
            null = os.open(os.devnull, os.O_RDWR)
            os.dup2(null, sys.stdout.fileno())
            os.dup2(null, sys.stderr.fileno())
        apt_cache.commit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("(130) Halted via KeyboardInterrupt.")
        sys.exit(130)
    except SystemExit as e:
        sys.exit(e.code)
    except:
        raise
