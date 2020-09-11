import sys
from summitemailer.gui import Application
import summitemailer.gui.controller


def initialize_qt_app(args):
    # handle args somehow
    app = Application(args)
    return app


def run_gui(app):
    print("running gui...")
    start = summitemailer.gui.controller.Controller()
    start.show_welcome()
    return app.exec_()


def main(args=sys.argv):
    app = initialize_qt_app(args)
    return run_gui(app)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(e, "there was an error...")
