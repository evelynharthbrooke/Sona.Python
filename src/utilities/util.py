import logging
import os
import platform
import re
import subprocess

from disnake.ext.commands import Context

if platform.system() == "Windows" | platform.system() == "win32":
    import winreg


async def retrieve_cpu_name(context: Context):
    """Retrieve the CPU name of the host system."""
    if platform.system() == "Windows" | platform.system() == "win32":
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Hardware\\Description\\System\\CentralProcessor\\0")
            processor_brand = winreg.QueryValueEx(key, "ProcessorNameString")[0]
            winreg.CloseKey(key)
            return processor_brand
        except FileNotFoundError:
            logging.error("The specified registry key could not be located in the registry.")
            await context.channel.send("Sorry, the system command occurred an error. Try again later!")
            return None
    elif platform.system() == "Darwin":
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/usr/sbin"
        return subprocess.check_output("sysctl -n machdep.cpu.brand_string").strip()
    elif platform.system() == "Linux":
        output = subprocess.check_output("cat /proc/cpuinfo", shell=True).strip()
        for line in output.decode("utf-8").split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return None
