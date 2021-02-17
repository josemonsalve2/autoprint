
""" Dictionary of system params. 
The values that are here are the default values, they can be changed 
by modifying these definitions, or by using the CONFIG_FILE file.
If EXTENSIONS_FILTER is not specified, all the files will be printed
"""
ap_params = {
    "LOG_LEVEL" : "DEBUG", # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "LOG_FILE" : None,

    "CONFIG_FILE" : ".config.json",

    "PRINTER_NAME" : None,

    "FOLDERS_TO_WATCH" : ['./'], # List of folder locations. Must be an array
    "EXTENSIONS_FILTER" : [], # List of extensions to print. Must be an array
    "FILES_PREFIX" : [],

    "WAITING_TIME" : 1
}

