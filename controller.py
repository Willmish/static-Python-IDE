from typing import List

from model import Model
from view import View


class Controller:
    def __init__(self) -> None:
        self._view: View = View(self)
        self._model: Model = Model(self)

    def runTCA(self, lines: List[str]):
        self._model.runTCA(lines)
        errors: List[str] = self._model._tca.getErrorMessages()
        self._view.addErrors(errors)


if __name__ == '__main__':
    controller: Controller = Controller()

    controller._model._tca.unitTests()
    
    controller._view.createGUI()
    controller._view.openFileByName('programs/testFile')
    print(controller._view._scroll.index("@0,0"))
    controller._view.mainLoop()


