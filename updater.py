from importlib.metadata import distributions
import os
import subprocess
from tqdm import tqdm

packs = [dist.name for dist in distributions()]
cmd = ["pip", "install", "--upgrade", "--no-deps"] + packs

env = os.environ.copy()
env["FORCE_COLOR"] = "1"

uptodate_counts = 0
progress = tqdm(total=len(packs), desc="Updating packages", unit="pkg")
processed = 0
if packs:
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env
    )
    if process.stdout is not None:
        for line in process.stdout:
            if line.startswith("Requirement already satisfied"):
                uptodate_counts += 1
                processed += 1
                progress.update(1)
            elif (
                line.startswith("Collecting")
                or line.startswith("Downloading")
                or line.startswith("Installing")
                or line.startswith("Successfully installed")
                or line.startswith("Successfully uninstalled")
            ):
                processed += 1
                progress.update(1)
                progress.write(line, end="")
            else:
                progress.write(line, end="")
    process.wait()
    progress.close()
print(f"Number of packages already up to date: {uptodate_counts}")
