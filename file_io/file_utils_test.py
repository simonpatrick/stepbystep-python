# _*_ coding=utf-8 _*_
import os
from unittest import TestCase
from file_io.file_utils import SVNLogs

__author__ = 'patrick'


class FileUtilsTest(TestCase):

    def test_create_dir(self):
        SVNLogs().create_dir("differ_temp/8")
        assert os.path.exists("differ_temp/8")