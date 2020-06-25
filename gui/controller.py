from gui.ui import Welcome, FromNew, FromSaved, MainWindow, test_call

welcome = None
load_cfg = None
load_new = None
load_main = None


class Controller:

    def __init__(self):
        pass

    def loader(self, parent, child):
        if child == 'welcome':
            self.show_welcome()
            self.close_window(parent)
        if child == 'load_cfg':
            self.show_load_cfg()
            self.close_window(parent)
        if child == 'load_new':
            self.show_load_new()
            self.close_window(parent)
        if child == 'load_main':
            conn_success = test_call()
            if conn_success:
                self.show_load_main()
                self.close_window(parent)
            else:
                print('error from trying to load main')

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
