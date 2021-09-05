import os
import pathlib
import subprocess
import sys
import tempfile

from findmtexe import find_mt_exe
from mtget import read_manifest


def write_manifest(filename: pathlib.Path, data: bytes) -> int:
    with tempfile.TemporaryFile(mode="wb", suffix=".xml", delete=False) as f:
        f.write(data)
        xmlfile = f.name
    p = subprocess.run([
        find_mt_exe(), "-nologo", "-manifest", xmlfile,
        f"-outputresource:{filename};1"
    ])
    os.remove(xmlfile)
    return p.returncode


def remove_uac(filename: pathlib.Path):
    data = read_manifest(filename)
    data = data.replace(b"requireAdministrator", b"asInvoker")
    print("将要写入以下清单数据：")
    print(data.decode("utf-8"))
    yn = input("是否继续？[Y/n] ").lower() or "y"
    if yn != "y":
        exit(1)
    ret = write_manifest(filename, data)
    if ret != 0:
        print(f"修改 manifest 失败: {ret}")
        exit(-1)
    print("=======")
    print("完成！")


def main():
    if len(sys.argv) != 2:
        print(f"usage: {pathlib.Path(sys.argv[0]).name} <pefile>")
        exit(1)
    try:
        remove_uac(pathlib.Path(sys.argv[1]).absolute())
    except Exception as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
