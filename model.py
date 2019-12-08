from typing import List, Tuple

from type_checking_algorithm import TCA


# namespaces
class Model:
    def __init__(self, controller) -> None:
        self._lines: List[str] = []
        self._numLines: List[int] = []
        self._tca: TCA = TCA()

    def runTCA(self, lines: List) -> None:
        self._tca.cleanAttributes()
        self._lines = lines
        # this list keeps track of the line number of each line
        self._numLines = [_ for _ in range(1, len(self._lines)+1)]
        self._lines = self._tca.removeComments(self._lines)
        swapTuple: Tuple[List[str], List[int]] = self._tca.removeEmptyLines(self._lines, self._numLines)
        self._lines = swapTuple[0]
        self._numLines = swapTuple[1]
        self._numLines.append(len(self._numLines))
        self._lines.append('#')  # this string is added at the end, to ensure that if the file ends without
        # a proper dedent (e.g. ends at a certain indent != 0) it will still sort the scopes correctly
        self._tca.setLines(self._lines)
        self._tca.setNumLines(self._numLines)
        self._tca.setInitialLinesChecked(len(self._lines))

        self._tca.sortScopes(self._lines, self._numLines)
        #self._tca.findVariables(self._lines, self._numLines)
        self._tca.findVariablesUsage(self._lines, self._numLines, self._tca.getScopes())

        self._tca.printErrors()
        a = self._tca.getTokens()
        b = self._tca.getLines()
        c = self._tca.getVariableUseToken()
        for i in range(len(a)):
            print(a[i], c[i], b[i])
