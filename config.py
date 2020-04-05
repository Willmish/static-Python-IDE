import configparser
from platform import system


# This Module takes care of the config file and directly interacts with it
class Config:
    def __init__(self):
        self._configParser = configparser.ConfigParser()

    def initialiseConfig(self, configFileName: str):
        # If configFile already exists, load it up
        # Otherwise create it
        try:
            with open(configFileName, 'r') as configFile:
                self._configParser.read(configFile)
        except FileNotFoundError:
            f = open(configFileName, 'w+')
            f.close()
        # First the user's system is determined
        sys = system()
        if sys == 'Windows':
            PLATFORM = 'Windows'
        elif sys == 'Linux':
            PLATFORM = 'Linux'
        else:
            raise Exception("Platform could not be determined")
        self._configParser['DEFAULT'] = {'OSType': PLATFORM}

        with open(configFileName, 'w') as configFile:
            self._configParser.write(configFile)

    def getCurrentSystem(self):
        return self._configParser['DEFAULT']['OSType']
