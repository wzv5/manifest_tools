import pathlib
import platform
import sys
import winreg
from typing import Tuple


def find_windows_sdk() -> Tuple[pathlib.Path, str]:
    vers = [
        "v10.0", "v8.1A", "v8.1", "v8.0A", "v8.0", "v7.1A", "v7.1", "v7.0a",
        "v7.0", "v6.1a", "v6.1", "v6.0a", "v6.0"
    ]
    root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          r"SOFTWARE\Microsoft\Microsoft SDKs\Windows", 0,
                          winreg.KEY_QUERY_VALUE | winreg.KEY_WOW64_32KEY)
    for v in vers:
        try:
            k = winreg.OpenKey(root, v)
            folder, _ = winreg.QueryValueEx(k, "InstallationFolder")
            version, _ = winreg.QueryValueEx(k, "ProductVersion")
            return pathlib.Path(folder), version
        except:
            pass
    raise Exception("找不到 Windows SDK")


def find_mt_exe() -> pathlib.Path:
    p = pathlib.Path(sys.argv[0]).absolute().with_name("mt.exe")
    if p.exists():
        return p
    sdk, ver = find_windows_sdk()
    arch = "x64" if platform.architecture()[0] == "64bit" else "x86"
    p = sdk.joinpath("bin", f"{ver}.0", arch, "mt.exe")
    return p


def main():
    print(find_mt_exe())


if __name__ == "__main__":
    main()
