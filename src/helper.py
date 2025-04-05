import subprocess
import os


def clone_MCData(version):
    if not os.path.exists(version):
        subprocess.run(
            [
                "git",
                "clone",
                "-b", f"client{version}",
                "https://github.com/extremeheat/extracted_minecraft_data.git",
                version,
                "--depth", "1"
            ],
            check=True
        )