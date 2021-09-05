import pathlib
import subprocess
import sys
from typing import Union

from findmtexe import find_mt_exe


def mtadd(filename: Union[pathlib.Path, str],
          manifests: list[Union[pathlib.Path, str]]):
    mt_exe = find_mt_exe()
    cmd = [
        mt_exe, "-nologo", "-manifest", *manifests,
        f"-outputresource:{filename};1"
    ]
    ret = subprocess.run(cmd).returncode
    if ret != 0:
        raise Exception(f"修改 manifest 失败: {ret}")


def _main(argv: list[str]):
    cur_exe = pathlib.Path(argv[0]).absolute()
    if len(argv) < 3:
        print(f"usage: {cur_exe.name} exefile manifestname [manifestname ...]")
        exit(1)
    exe = argv[1]
    cur_path = cur_exe.parent
    manifests = []
    for m in argv[2:]:
        p = pathlib.Path(m)
        if p.exists():
            manifests.append(p)
        elif m == "base":
            manifests.extend([
                cur_path.joinpath("manifests", f"{m}.xml")
                for m in ["nouac", "ui", "win10"]
            ])
        else:
            p = cur_path.joinpath("manifests", f"{m}.xml")
            if not p.exists():
                raise Exception(f"文件 {p} 不存在")
            manifests.append(p)
    try:
        mtadd(exe, manifests)
    except Exception as e:
        print(e)
        exit(-1)
    print("完成")


def main():
    _main(sys.argv)


if __name__ == "__main__":
    main()
