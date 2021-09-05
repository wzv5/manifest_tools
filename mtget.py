import ctypes
import pathlib
import sys
from typing import Union

FindResource = ctypes.windll.kernel32.FindResourceA
FindResource.restype = ctypes.c_void_p
FindResource.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

LoadLibraryEx = ctypes.windll.kernel32.LoadLibraryExW
LoadLibraryEx.restype = ctypes.c_void_p
LoadLibraryEx.argtypes = [ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int]

LoadResource = ctypes.windll.kernel32.LoadResource
LoadResource.restype = ctypes.c_void_p
LoadResource.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

LockResource = ctypes.windll.kernel32.LockResource
LockResource.restype = ctypes.c_void_p
LockResource.argtypes = [ctypes.c_void_p]

SizeofResource = ctypes.windll.kernel32.SizeofResource
SizeofResource.restype = ctypes.c_void_p
SizeofResource.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

FreeResource = ctypes.windll.kernel32.FreeResource
FreeResource.restype = ctypes.c_bool
FreeResource.argtypes = [ctypes.c_void_p]

FreeLibrary = ctypes.windll.kernel32.FreeLibrary
FreeLibrary.restype = ctypes.c_bool
FreeLibrary.argtypes = [ctypes.c_void_p]

LOAD_LIBRARY_AS_DATAFILE = 2


def read_manifest(filename: Union[pathlib.Path, str]) -> bytes:
    hResData = None
    hModule = None
    try:
        hModule = LoadLibraryEx(str(filename), 0, LOAD_LIBRARY_AS_DATAFILE)
        if not hModule:
            raise Exception("载入模块失败")
        hRes = FindResource(hModule, 1, 24)
        if not hRes:
            raise Exception("找不到指定资源")
        hResData = LoadResource(hModule, hRes)
        if not hResData:
            raise Exception("载入资源失败")
        pData = LockResource(hResData)
        datalen = SizeofResource(hModule, hRes)
        if not pData or not datalen:
            raise Exception("读取资源失败")
        data = ctypes.string_at(pData, datalen)
        return data
    finally:
        if hResData:
            FreeResource(hResData)
        if hModule:
            FreeLibrary(hModule)


def main():
    if len(sys.argv) != 2:
        print(f"usage: {pathlib.Path(sys.argv[0]).name} <pefile>")
        exit(1)
    try:
        data = read_manifest(pathlib.Path(sys.argv[1]).absolute())
    except Exception as e:
        print(e)
        exit(-1)
    print(data.decode())


if __name__ == "__main__":
    main()
