#!/usr/bin/python
from optparse import OptionParser
import sys
import logging
import os
import os.path
import shutil
from subprocess import call

PLUGINS_PATH = '~/.local/share/rhythmbox/plugins/'
GLIB_PATH = '/usr/share/glib-2.0/schemas/'

def uninstall(plugin):
    """
    Uninstall the plugin.
    """
    if os.path.exists(os.path.join(PLUGINS_PATH, plugin)):
        print("uninstall plugin %s" % plugin)
        shutil.rmtree(os.path.join(PLUGINS_PATH, plugin))


def install(plugin):
    """
    Install the plugin.
    """
    uninstall(plugin)
    print("install plugin %s" % plugin)
    source_path = os.path.join('.', plugin, plugin)
    install_path = os.path.expanduser(os.path.join(PLUGINS_PATH,plugin))
    shutil.copytree(source_path, install_path)
    print(source_path, install_path)
    if os.path.exists(os.path.join(PLUGINS_PATH, plugin, plugin, 'schemas')):
        print("install schemas for plugin %s" % plugin)
        source_path = os.path.join('.', plugin , 'schemas')
        call(['sudo', 'cp', source_path, GLIB_PATH])
        call(['sudo', 'glib-compile-schemas', GLIB_PATH])



if __name__ == '__main__':
    parser = OptionParser(version="%prog 0.1", usage= "usage: %prog [options] args" )
    parser.description= "installer for plugins rhythmbox"
    parser.epilog = "by Frederic Aoustin"
    parser.add_option("-u", "--uninstall",
        action="store_true",
        dest="uninstall",
        help ="uninstall plugins",
        default=False)
    (options, args) = parser.parse_args()
    if not len(args):
        print('not plugin in argument')
        exit()
    plugin = args[0]
    if not os.path.isdir(os.path.join('.',plugin)):
        print('%s not found plugin' % plugin)
        exit()
    if options.uninstall :
        uninstall(plugin)
        exit()
    install(plugin)
