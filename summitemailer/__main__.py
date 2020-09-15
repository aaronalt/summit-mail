import logging
import sys
import summitemailer.gui.controller as gui
from summitemailer.gui import Application


def initialize_qt_app(args):
    # handle args somehow
    app = Application(args)
    return app


def run_gui(app):
    # logging.info('Running gui')
    start = gui.Controller()
    start.show_welcome()
    return app.exec_()


def main(args=sys.argv):
    app = initialize_qt_app(args)
    logging.basicConfig(filename='summitmailer.log', level=logging.INFO, format='%(asctime)s %(message)s')
    # logging.info('Started app')
    return run_gui(app)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(e, "there was an error...")
