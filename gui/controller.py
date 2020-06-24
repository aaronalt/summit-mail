from gui.dialog import Dialog
from gui.ui import Welcome, FromNew, FromSaved, MainWindow, test_call
from gui.creds import Creds
# todo: change logic from signals returning int, to return fn switch(parent, next)

welcome = None
load_cfg = None
load_new = None
load_main = None


class Controller:

    def __init__(self):
        pass

    def loader(self, parent, child):
        print(type(parent).__name__, next)
        self.open_window(child)
        self.close_window(parent)


        """try:
            load_cfg.close()
        except AttributeError:
            pass
        finally:
            if num == 0:
                load_new.close()
            if num == 1:
                self.show_load_cfg()
            if num == 2:
                self.show_load_new()
            if num == 3:
                print("testing cfg (controller.loader.3)")
                # test airtable connection
                conn_tested = test_call()
                if conn_tested:
                    self.show_load_main()
                else:
                    print("0 returned from ui.py")
                    self.show_load_cfg()
            if num == 4:
                # todo: add more specific exceptions/error logic
                print("testing cfg (controller.loader.4)")
                # test airtable connection
                conn_tested = test_call()
                if conn_tested:
                    self.show_load_main()
                    welcome.close()
                    load_new.close()
                else:
                    self.show_load_new()"""

    def open_window(self, child):
        if child == 'welcome':
            self.show_welcome()
        if child == 'load_cfg':
            self.show_load_cfg()
        if child == 'load_new':
            self.show_load_new()
        if child == 'load_main':
            self.show_load_main()

    def close_window(self, parent):
        if type(parent).__name__ == 'Welcome':
            welcome.close()
        if type(parent).__name__ == 'FromSaved':
            load_cfg.close()
        if type(parent).__name__ == 'FromNew':
            load_new.close()

    def show_welcome(self):
        global welcome
        welcome = Welcome()
        welcome.switch.connect(self.loader)
        welcome.show()

    def show_load_cfg(self):
        global load_cfg
        load_cfg = FromSaved()
        load_cfg.switch.connect(self.loader)
        load_cfg.show()

    def show_load_new(self):
        global load_new
        load_new = FromNew()
        load_new.switch.connect(self.loader)
        load_new.show()

    def show_load_main(self):
        global load_main
        load_main = MainWindow()
        load_main.switch.connect(self.loader)
        load_main.show()
