import pathlib
import shutil
import sys
import tempfile
import unittest


class MyTest(unittest.TestCase):
    def test_find_mt(self):
        from findmtexe import find_mt_exe
        self.assertTrue(find_mt_exe().exists())

    def test_read_manifest(self):
        from mtget import read_manifest
        self.assertIsNotNone(read_manifest(sys.executable))

    def test_write_manifest(self):
        import mtadd
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = pathlib.Path(tempdir)
            exe = shutil.copyfile(sys.executable,
                                  tempdir.joinpath("python.exe"))
            mtadd._main([__file__, str(exe), "base"])


if __name__ == "__main__":
    unittest.main()
