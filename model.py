from typing import List
from type_checking_algorithm import TCA

# namespaces
class Model:
    def __init__(self, controller) -> None:
        self._lines: List[str] = []
        self._numLines: List[int] = []
        self._tca: TCA = TCA()

    def runTCA(self, lines: List) -> None:
        self._lines = lines
        # this list keeps track of the line number of each line
        self._numLines = [_ for _ in range(1, len(self._lines)+1)]
        self._lines = self._tca.removeComments(self._lines)
        swapTuple = self._tca.removeEmptyLines(self._lines, self._numLines)
        self._lines = swapTuple[0]
        self._numLines = swapTuple[1]

        self._tca.sortScopes(self._lines, self._numLines)
        #self._tca.findVariables(self._lines, self._numLines)

        #self._tca.findVariablesUsage(self._lines, self._numLines, self._tca.getScopes()) # TODO fix findVariables first
        self._tca.printErrors()
        self._tca.cleanAttributes()


