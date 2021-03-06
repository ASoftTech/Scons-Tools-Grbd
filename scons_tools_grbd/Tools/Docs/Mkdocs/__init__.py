"""
If the user requests "Docs.Mkdocs" then this will call this script as a tool
In which case we include all the Mkdocs related builders
"""

from . import MkdocsServer, MkdocsBuild, MkdocsJsonBuild, MkdocsPublish, MkdocsCombiner

def generate(env):
    MkdocsServer.generate(env)
    MkdocsBuild.generate(env)
    MkdocsPublish.generate(env)
    MkdocsJsonBuild.generate(env)
    MkdocsCombiner.generate(env)

def exists(env):
    if (MkdocsServer.exists(env) == False): return False
    if (MkdocsBuild.exists(env) == False): return False
    if (MkdocsPublish.exists(env) == False): return False
    if (MkdocsJsonBuild.exists(env) == False): return False
    if (MkdocsCombiner.exists(env) == False): return False
    return True
