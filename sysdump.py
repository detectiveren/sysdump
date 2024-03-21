# This python script collects information on the user's system
import platform
import socket

import psutil
import GPUtil
from datetime import datetime
from tabulate import tabulate


def getOSInfo():
    OS_Name = platform.system()
    OS_Release = platform.release()
    OS_System_Architecture = platform.machine()
    OS_System_Detail = platform.platform()
    OS_Username = platform.node()
    #OS_Check_For_IOT = platform.win32_is_iot()
    OS_Boot_Time = psutil.boot_time()
    return (OS_Name, OS_Release, OS_System_Architecture, OS_System_Detail, OS_Username,
            OS_Boot_Time)


def get_size(bytes, suffix="B"):
    # Scale bytes to its proper format
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def getHardwareInfo():
    # Grab CPU Platform and Architecture
    cpuPlatform = platform.processor()
    cpuArchitecture = platform.machine()
    # Grab CPU Physical Cores and Total Cores
    cpuPhysicalCores = psutil.cpu_count(logical=False)
    cpuTotalCores = psutil.cpu_count(logical=True)
    # Grab CPU Frequencies
    cpuFreq = psutil.cpu_freq()
    maxCPUFreq = f"{cpuFreq.max:.2f}MHz"
    minCPUFreq = f"{cpuFreq.min:.2f}MHz"
    currentCPUFreq = f"{cpuFreq.current:.2f}MHz"
    # Grab Memory Info
    virtualMemory = psutil.virtual_memory()
    TotalMemory = f"{get_size(virtualMemory.total)}"
    AvailableMemory = f"{get_size(virtualMemory.available)}"
    UsedMemory = f"{get_size(virtualMemory.used)}"
    MemoryPercentage = f"{get_size(virtualMemory.percent)}%"
    return (cpuPlatform, cpuArchitecture, cpuPhysicalCores, cpuTotalCores, maxCPUFreq, minCPUFreq,
            currentCPUFreq, TotalMemory, AvailableMemory, UsedMemory, MemoryPercentage)


def convertBootTime(boot_time):
    bootTime = datetime.fromtimestamp(boot_time)
    return bootTime


def getNetInfo():
    interface_details = psutil.net_if_addrs()
    for interfaceName, interfaceAddress in interface_details.items():
        for address in interfaceAddress:
            if address.family == socket.AF_INET:
                print("Interface Name:", interfaceName)
                print(f"    IP Address: {address.address}")
                print(f"    Netmask: {address.netmask}")
                print(f"    Broadcast IP: {address.broadcast}")
            elif address.family == psutil.AF_LINK:
                print(f"    MAC Address: {address.address}")
            elif address.family == socket.AF_INET6:
                print(f"    IP Address (IPv6): {address.address}")


def GPUInfo():
    getGPUs = GPUtil.getGPUs()
    list_gpus = []
    for gpu in getGPUs:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load * 100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))

    print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                       "temperature", "uuid")))


def getSysDump():
    operatingSystem = getOSInfo()
    hardwareInfo = getHardwareInfo()
    systemBootTime = convertBootTime(operatingSystem[5])
    print("Operating System Info")
    print("OS Name:", operatingSystem[0])
    print("OS Version:", operatingSystem[1])
    print("OS Architecture:", operatingSystem[2])
    print("OS System Aliases:", operatingSystem[3])
    print("OS Username:", operatingSystem[4])
    print("System Boot Time:", systemBootTime)
    print("\nHardware Info")
    print("Processor:", hardwareInfo[0])
    print("Architecture:", hardwareInfo[1])
    print("CPU Physical Cores:", hardwareInfo[2])
    print("CPU Total Cores:", hardwareInfo[3])
    print("CPU Max Frequency:", hardwareInfo[4])
    print("CPU Min Frequency:", hardwareInfo[5])
    print("CPU Current Frequency:", hardwareInfo[6])
    print("Total Memory:", hardwareInfo[7])
    print("Available Memory:", hardwareInfo[8])
    print("Memory in Use:", hardwareInfo[9])
    print("Memory Percentage:", hardwareInfo[10])
    print("\nNetwork Info")
    getNetInfo()
    print("\nGPU Info")
    GPUInfo()
    print("To save the output to a file run the following command and customize it if you want")
    print("python sysdump.py > filename.txt")


getSysDump()