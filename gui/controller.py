from gui.dialog import Dialog
from gui.ui import Welcome, FromNew, FromSaved, MainWindow
from gui.creds import Creds


welcome = None
load_cfg = None
load_new = None
load_main = None


class Controller:

    def __init__(self):
        pass

    def loader(self, num):
        try:
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
                self.show_load_main()
                welcome.close()
            if num == 4:
                print(Creds.base_id)
                # todo: add more specific exceptions/error logic
                try:
                    main = MainWindow()
                    main.test_call()
                    welcome.close()
                    load_new.close()
                except KeyError as e:
                    dialog = Dialog('error: check your API key or Base ID')
                    return dialog
                except FileNotFoundError as f:
                    dialog = Dialog("File not found")
                    return dialog
                else:
                    self.show_load_main()
                    welcome.close()
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
