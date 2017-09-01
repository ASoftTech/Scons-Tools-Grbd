"""
MkdocsJsonBuild
  This tool will generate the documentation output as json using markdown files as an input
  via mkdocs to an output directory
"""

import os, sys
import os.path as path
from SCons.Script import *

def exists(env):
    """return True if this tool is valid in this environment"""
    return True

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    env.SetDefault(Mkdocs_WorkingDir = env.Dir('.').abspath)
    # Available Options - These override those within the yaml configuration file
    # If to Remove old files from the site_dir before building (the default).
    env.SetDefault(Mkdocs_CleanBuild = None)
    # If to enable Strict mode
    env.SetDefault(Mkdocs_Strict = False)
    # Directory to output the build to - default is 'site'
    env.SetDefault(Mkdocs_SiteDir = None)
    # If to silence warnings
    env.SetDefault(Mkdocs_Quiet = False)
    # Show verbose messages
    env.SetDefault(Mkdocs_Verbose = False)
    # Additional Arguments
    env.SetDefault(Mkdocs_ExtraArgs = [])

    # Register the builder
    bld = Builder(action = __MkdocsJsonBuild_func, emitter = __MkdocsJsonBuild_modify_targets)
    env.Append(BUILDERS = {'__MkdocsJsonBuild' : bld})
    env.AddMethod(MkdocsJsonBuild, 'MkdocsJsonBuild')


def MkdocsJsonBuild(env, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if source:
        return env.__MkdocsJsonBuild(source)
    else:
        return env.__MkdocsJsonBuild('mkdocs.yml')


def __MkdocsJsonBuild_modify_targets(target, source, env):
    del target[:]
    if env['Mkdocs_SiteDir']:
        dirnode = Dir(env['Mkdocs_SiteDir'])
    else:
        dirnode = Dir('site')
    target.append(dirnode)
    env.Clean(target, dirnode)
    return target, source


def __MkdocsJsonBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['mkdocs', 'json']

    for srcitem in source:
        cfgfile = srcitem.abspath

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if env['Mkdocs_CleanBuild'] == True:
            cmdopts.append('--clean')
        elif env['Mkdocs_CleanBuild'] == False:
            cmdopts.append('--dirty')

        if env['Mkdocs_Strict']:
            cmdopts.append('--strict')

        if env['Mkdocs_SiteDir']:
            cmdopts.append('--site-dir=' + env['Mkdocs_SiteDir'])

        if env['Mkdocs_Quiet']:
            cmdopts.append('--quiet')

        if env['Mkdocs_Verbose']:
            cmdopts.append('--verbose')

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Building MkDocs Documentation as Json:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))