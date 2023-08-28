from importlib.metadata import distributions
from subprocess import call

packs = [dist.name for dist in distributions()]
call("pip install --upgrade " + ' '.join(packs), shell=True)