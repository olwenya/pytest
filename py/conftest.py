pytest_plugins = 'pytest_doctest', 'pytest_pytester', 'pytest_restdoc'
rsyncignore = ['c-extension/greenlet/build']

import py
class PylibTestconfigPlugin:
    def pytest_pyfuncarg_specssh(self, pyfuncitem):
        return getspecssh(pyfuncitem.config)
    def pytest_pyfuncarg_specsocket(self, pyfuncitem):
        return getsocketspec(pyfuncitem.config)

    def pytest_addoption(self, parser):
        group = parser.addgroup("pylib", "py lib testing options")
        group.addoption('--sshhost', 
               action="store", dest="sshhost", default=None,
               help=("target to run tests requiring ssh, e.g. "
                     "user@codespeak.net"))
        group.addoption('--gx', 
               action="append", dest="gspecs", default=None,
               help=("add a global test environment, XSpec-syntax. ")), 
        group.addoption('--runslowtests',
               action="store_true", dest="runslowtests", default=False,
               help=("run slow tests"))

ConftestPlugin = PylibTestconfigPlugin

# configuration information for tests 
def getgspecs(config=None):
    if config is None:
        config = py.test.config
    return [py.execnet.XSpec(spec) 
                for spec in config.getvalueorskip("gspecs")]

def getspecssh(config=None):
    xspecs = getgspecs(config)
    for spec in xspecs:
        if spec.ssh:
            if not py.path.local.sysfind("ssh"):
                py.test.skip("command not found: ssh")
            return spec

def getsocketspec(config=None):
    xspecs = getgspecs(config)
    for spec in xspecs:
        if spec.socket:
            return spec
