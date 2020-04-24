from typing import List
from model import Model
from view import View
from config import Config


class Controller:
    def __init__(self) -> None:
        self._view: View = View(self)
        self._model: Model = Model(self)

    def runTCA(self, lines: List[str]) -> None:
        self._model.runTCA(lines)
        errors: List[str] = self._model.getErrors()
        self._view.addErrors(errors)

    def getConfiguration(self, config: Config) -> None:
        self._currentSystem = config.getCurrentSystem()

    def setAllConfiguration(self) -> None:
        View.PLATFORM = self._currentSystem
        self._view.setPlatformInfo()


if __name__ == '__main__':
    config: Config = Config()
    controller: Controller = Controller()
    # tests
    controller._model._tca.unitTests()
    # Initialise config
    config.initialiseConfig('config.ini')
    controller.getConfiguration(config)
    controller.setAllConfiguration()
    # Initialise GUI
    controller._view.createGUI()
    controller._view.openFileByName('programs/testFile')
    controller._view.mainLoop()


