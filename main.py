# PyCutils https://github.com/loudtrexx/PyCutils

import ctypes
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
import sys

def privilage_check():
    # Check if admin rights already exist
    return ctypes.windll.shell32.IsUserAnAdmin()


def adjust_privileges():
    SE_SHUTDOWN_PRIVILEGE = 19
    enable_privilege = c_uint(1)
    current_state = c_int()

    status = windll.ntdll.RtlAdjustPrivilege(
        c_uint(SE_SHUTDOWN_PRIVILEGE),
        enable_privilege,
        c_uint(0),  # Adjust privilege for the current thread
        byref(current_state)
    )

    if status == 0:
        print("Privilege adjusted successfully!")
        return True
    else:
        print("Failed to adjust privilege.")
        return False  # Indicates failure

def run_privilaged():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def BSOD_cause(code):
    code = hex(code)
    code = int(code)

    nullptr = POINTER(c_int)()


    windll.ntdll.NtRaiseHardError(
        c_ulong(code), # Error code for the blue screen
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

def getUIeffects():
    effects_enabled = ctypes.c_int()
    ctypes.windll.user32.SystemParametersInfoW(4158, 0, ctypes.byref(effects_enabled), 0)
    print(bool(effects_enabled.value))

def setUIeffects(status):
    SPI_SETUIEFFECTS = 4159
    SPIF_SENDCHANGE = 2  # Ensures the change is applied immediately

    # Disable UI effects
    if status == False:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETUIEFFECTS, 0, False, SPIF_SENDCHANGE)

    # Enable UI effects
    elif status == True:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETUIEFFECTS, 0, True, SPIF_SENDCHANGE)


