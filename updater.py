from importlib.metadata import distributions
from subprocess import call

packs = [dist.name for dist in distributions()]
call("pip install --upgrade --no-deps " + " ".join(packs), shell=True)
