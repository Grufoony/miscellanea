from importlib.metadata import distributions
import os
import subprocess
from tqdm import tqdm

packs = [dist.name for dist in distributions()]
cmd = ["pip", "install", "--upgrade", "--no-deps"] + packs

env = os.environ.copy()

uptodate_counts = 0
progress = tqdm(
    total=len(packs),
    desc="Updating packages",
    unit="pkg",
    dynamic_ncols=True,
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
)

if packs:
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env
    )
    if process.stdout is not None:
        for line in process.stdout:
            if line.startswith("Requirement already satisfied"):
                uptodate_counts += 1
                if progress.n < progress.total:
                    progress.update(1)
            elif line.startswith("Collecting") or line.startswith("Processing"):
                if progress.n < progress.total:
                    progress.update(1)
                parts = line.split()
                if len(parts) > 1:
                    progress.set_description(f"Updating {parts[1]}")
            elif line.startswith("ERROR"):
                progress.write(line, end="")
    process.wait()
    progress.close()
print(f"Number of packages already up to date: {uptodate_counts}")
