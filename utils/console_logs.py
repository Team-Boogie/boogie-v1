import apis


def info(msg: str):
    print(msg)
    apis.addConsoleLog("INFO", msg)


def error(msg: str):
    print(msg)
    apis.addConsoleLog("ERROR", msg)


def fortnite(msg: str):
    print(msg)
    apis.addConsoleLog("FORTNITE", msg)


def warning(msg: str):
    print(msg)
    apis.addConsoleLog("WARNING", msg)
