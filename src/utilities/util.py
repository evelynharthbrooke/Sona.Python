import logging as log
import os
import platform
import re
import subprocess

from discord.ext.commands import Context

if platform.system() == "Windows":
    import winreg


async def retrieve_cpu_name(context: Context):
    """
    Creates a function that retrieves the CPU name for various
    operating systems, be it Windows, macOS, or Linux.
    """
    if platform.system() == "Windows":  # Windows
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"Hardware\Description\System\CentralProcessor\0")
            processor_brand = winreg.QueryValueEx(
                key, "ProcessorNameString")[0]
            winreg.CloseKey(key)
            return processor_brand
        except FileNotFoundError:
            log.error("The specified registry key could not be located in the registry.")
            await context.send("Sorry, I encountered an error getting the CPU. Try again later!")
            return
    elif platform.system() == "Darwin":  # macOS
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":  # Linux
        command = "cat /proc/cpuinfo"
        output = subprocess.check_output(command, shell=True).strip()
        for line in output.decode('utf-8').split("\n"):
            if 'model name' in line:
                return re.sub(".*model name.*:", "", line, 1)
    return ""
