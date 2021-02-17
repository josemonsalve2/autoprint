import platform as plat
from config.debug import log

if plat.system() == "Windows":
    import win32api
    import win32print
elif plat.system() == "Darwin" or plat.system() == "Linux":
    import subprocess
else:
    log.critical("OS NOT SUPPORTED")


class printer_driver:
    printer_name = None
    print = None
    """Communicate with the CUPS driver via lpr command
    """
    def print_linux_unix(self, filename):
        out = ""
        if self.printer_name:
            out = subprocess.run(['lpr',"-d", self.printer_name, filename], shell = True, capture_output = True )
        else:
            out = subprocess.run(['lpr', filename], shell = True, capture_output = True )
        if out.stderr:
            log.error(f"Error when printing {out.stderr}")
        if out.stdout:
            log.info(f"Output when printing {out.stdout}")

    """ Communicate with windows print driver via command
    """
    def print_windows(self, filename):
        win32api.ShellExecute (
            0,
            "printto",
            filename,
            self.printer_name,
            ".",
            0
        )

    """ Initialize printer driver
    """     
    def __init__(self, p_name = None):
        self.printer_name = p_name
        if plat.system() == "Darwin" or plat.system() == "Linux":
            log.info("Using LINUX or MAC OS")
            self.print = self.print_linux_unix
        elif plat.system() == "Windows":
            log.info("Using WINDOWS")
            self.print = self.print_windows
            if not self.printer_name:
                self.printer_name = win32print.GetDefaultPrinter()
        else:
            log.critical("OS Not supported")

        