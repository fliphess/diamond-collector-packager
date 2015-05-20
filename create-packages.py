#!/usr/bin/env python
import yaml
import sys
import os

control_header = """
Source: diamond-collector-builder
Maintainer: Flip Hess <flip@fliphess.com>
Homepage: http://www.fliphess.com
Section: python
Priority: extra
Standards-Version: 3.9.4
Build-Depends: debhelper (>= 7)
"""

control_package = """
Package: %(package)s
Description: downtek diamond collector 
Architecture: all
Depends: %(depends)s
"""


def log(msg):
    """ Log to stderr 
    """
    print >>sys.stderr, "%s" % msg


def read_settings_file(filename='./settings.yml'):
    """ Read yaml settings file and return dict 
    """
    with open(filename, "r") as fh:
        return yaml.load(fh.read())


def create_install_file(package, settings):
    """ Create a debian/<package>.install file with instructions where to put files on the filesystem on install
    """
    content = ''

    """ If custom collector present, add to content of install file 
    """
    if 'dir' in settings[package]:
        directory = settings[package]['dir'].rstrip('/')
        if os.path.isdir('%s' % directory):
            content += '%s    usr/share/diamond/collectors/\n' % directory

    """ Add the collector config file to the install file 
    """
    content += "config/%s.conf   etc/diamond/collectors/\n" % settings[package]['name']
    with open('debian/%s.install' % package, "w") as fh:
        fh.write(content) 


def add_package_to_control_file(package, settings):
    """ Create an entry in debian/control for a given package 
    """
    if 'deps' in settings[package]:
        depends = "diamond, " + ", ".join(settings[package]['deps'])
    else:
        depends = "diamond"
    content = control_package % {"package": package, "depends": depends}
    with open('debian/control', "a") as fh:
        fh.write(content)


def write_collector_file(package, settings):
    """ Write the actual config file to config/<Collector name>.conf
    """
    collector = settings[package]['name']
    config_file = 'config/%s.conf' % collector
    content = "\n".join(settings[package]['content']) + "\n"
    with open(config_file, "w") as fh:
        fh.write(content)


def create_package_config(package, settings):
    log("Creating package config for %s" % settings[package]['name'])
    add_package_to_control_file(package, settings)
    create_install_file(package, settings)
    write_collector_file(package, settings)


def main(): 
    if not os.path.isdir('debian/'): 
        log("No debian directory found")
        sys.exit(1)

    if not os.path.isfile('./settings.yml'):
        log("Settings file ./settings.yml not found")
        sys.exit(1)

    """ Write the header to debian/control
    """
    with open('debian/control', "w") as fh:
        fh.write(control_header)

    settings = read_settings_file()
    for package in settings:
        create_package_config(package=package, settings=settings)

    log("\nAll config created! You can now build and dput your diamond-collector packages")


if __name__ == '__main__':
    main()

