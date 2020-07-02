from __future__ import absolute_import

import sys
import unittest

from PySide2.QtCore import QThread

import gui
from gui.main import main


class InitTest(unittest.TestCase):

    def setUp(self):
        sys.exit(main())

    def test_init(self):
        self.assertIs(gui.gui_thread, QThread)

if __name__ == '__main__':
    unittest.main(verbosity=2, module=gui.test)
