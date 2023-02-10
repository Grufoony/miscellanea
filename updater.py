import pkg_resources
from subprocess import call

packs = [dist.project_name for dist in pkg_resources.working_set]
call("pip install --upgrade " + ' '.join(packs), shell=True)