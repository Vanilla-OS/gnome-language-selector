import subprocess
import tempfile
import shutil


class ABRootTransaction():
    
    def __init__(self):
        self.__binary = shutil.which("abroot")
        if not self.__binary:
            raise RuntimeError("abroot not found")

    def commit_packages(self, install: list, remove: list) -> bool:
        if not install and not remove:
            return

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("#!/bin/bash\n")
            f.write("apt update\n")

            if install:
                f.write("apt install -y {}\n".format(" ".join(install)))

            if remove:
                f.write("apt remove -y {}\n".format(" ".join(remove)))

            f.flush()
            f.close()

            cmd = ["pkexec", self.__binary, "exec", "-y", "sh", f.name]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                print(res.stdout)
                print(res.stderr)
                return False

            return True
