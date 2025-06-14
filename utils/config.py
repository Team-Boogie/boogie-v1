import type_definitions
import constants
import json

def read() -> type_definitions.Config:
    with open(file=constants.configFilePath) as f:
        config = json.loads(f.read())
        return config