# -*- coding: utf-8 -*-

"""Custom table of Points and Links.
Also contains selection status label.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TypeVar,
    Tuple,
    List,
)
from core.QtModules import (
    QTableWidget,
    pyqtSignal,
    QSizePolicy,
    QAbstractItemView,
    QTableWidgetItem,
    Qt,
    pyqtSlot,
    QApplication,
    QTableWidgetSelectionRange,
    QLabel,
)
from core.graphics import colorIcons, colorQt
from core.libs import VPoint, VLink


class BaseTableWidget(QTableWidget):
    
    """Two tables has some shared function."""
    
    deleteRequest = pyqtSignal()
    
    def __init__(self,
        RowCount: int,
        HorizontalHeaderItems: Tuple[str],
        parent=None
    ):
        super(BaseTableWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        ))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setRowCount(RowCount)
        self.setColumnCount(len(HorizontalHeaderItems)+1)
        for i, e in enumerate(('Name',) + HorizontalHeaderItems):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))
    
    def rowTexts(self, row: int, *, hasName: bool = False) -> List[str]:
        """Get the whole row of texts.
        
        + Edit point: hasName = False
        + Edit link: hasName = True
        """
        texts = []
        for column in self.effectiveRange(hasName):
            item = self.item(row, column)
            if item is None:
                texts.append('')
            else:
                texts.append(item.text())
        return texts
    
    def dataTuple(self) -> Tuple[TypeVar("Element", VPoint, VLink)]:
        """Return data set as a container."""
        return tuple(self.data())
    
    def selectedRows(self) -> List[int]:
        """Get what row is been selected."""
        tmp_set = set([])
        for r in self.selectedRanges():
            tmp_set.update([i for i in range(r.topRow(), r.bottomRow() + 1)])
        return sorted(tmp_set)
    
    def keyPressEvent(self, event):
        """Hit the delete key,
        will emit delete signal from this table.
        """
        if event.key()==Qt.Key_Delete:
            self.deleteRequest.emit()
    
    def clear(self):
        """Overrided the clear function, just removed all items."""
        for row in range(self.rowCount()):
            self.removeRow(0)

class PointTableWidget(BaseTableWidget):
    
    """Custom table widget for points."""
    
    name = 'Point'
    rowSelectionChanged = pyqtSignal(list)
    selectionLabelUpdate = pyqtSignal(list, list)
    
    def __init__(self, parent=None):
        super(PointTableWidget, self).__init__(0, (
            'Links',
            'Type',
            'Color',
            'X',
            'Y',
            'Current'
        ), parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 90)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 130)
        self.itemSelectionChanged.connect(self.__emitSelectionChanged)
    
    def data(self) -> VPoint:
        """Yield the digitization of all table data."""
        for row in range(self.rowCount()):
            Links = self.item(row, 1).text()
            color = self.item(row, 3).text()
            x = float(self.item(row, 4).text())
            y = float(self.item(row, 5).text())
            '''
            Type = (type:str, angle:float)
            '''
            Type = self.item(row, 2).text().split(':')
            if Type[0]=='R':
                Type = 0
                angle = 0.
            elif Type[0]=='P' or Type[0]=='RP':
                angle = float(Type[1])
                Type = {'P':1, 'RP':2}[Type[0]]
            vpoint = VPoint(Links, Type, angle, color, x, y, colorQt)
            vpoint.move(*self.currentPosition(row))
            yield vpoint
    
    def editArgs(self,
        row: int,
        Links: str,
        Type: str,
        Color: str,
        x: float,
        y: float
    ):
        """Edite a point."""
        for i, e in enumerate([
            'Point{}'.format(row),
            Links,
            Type,
            Color,
            x,
            y,
            "({}, {})".format(x, y)
        ]):
            item = QTableWidgetItem(str(e))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i == 3:
                item.setIcon(colorIcons(e))
            self.setItem(row, i, item)
    
    def rename(self, row: int):
        """When index changed, the points need to rename."""
        for j in range(row, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    
    def currentPosition(self, row: int) -> List[Tuple[float, float]]:
        """Get the current coordinate from a point."""
        Type = self.item(row, 2).text().split(':')
        coords = eval("[{}]".format(self.item(row, 6).text().replace(';', ',')))
        if (len(coords) < 2) and ((Type[0] == 'P') or (Type[0] == 'RP')):
            self.item(row, 6).setText("({0}, {1}); ({0}, {1})".format(*coords[0]))
            coords.append(coords[0])
        return coords
    
    def updateCurrentPosition(self, coords: Tuple[Tuple[Tuple[float, float]]]):
        """Update the current coordinate for a point."""
        for i, c in enumerate(coords):
            if type(c[0]) == float:
                text = "({}, {})".format(*c)
            else:
                text = "; ".join("({}, {})".format(x, y) for x, y in c)
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.setItem(i, 6, item)
    
    def getBackPosition(self):
        """Let all the points go back to origin coordinate."""
        self.updateCurrentPosition(tuple(
            (float(self.item(row, 4).text()), float(self.item(row, 5).text()))
            for row in range(self.rowCount())
        ))
    
    @pyqtSlot(tuple, bool)
    def setSelections(self, selections: Tuple[int], keyDetect: bool):
        """Auto select function, get the signal from canvas."""
        self.setFocus()
        keyboardModifiers = QApplication.keyboardModifiers()
        if keyDetect:
            if keyboardModifiers == Qt.ShiftModifier:
                self.__setSelectedRanges(selections, continueSelect=True, UnSelect=False)
            elif keyboardModifiers == Qt.ControlModifier:
                self.__setSelectedRanges(selections, continueSelect=True, UnSelect=True)
            else:
                self.__setSelectedRanges(selections, continueSelect=False, UnSelect=False)
        else:
            continueSelect = (keyboardModifiers == Qt.ShiftModifier)
            self.__setSelectedRanges(selections, continueSelect=continueSelect, UnSelect=False)
        distance = []
        selectedRows = self.selectedRows()
        if len(selectedRows) > 1:
            data = self.dataTuple()
            for i, row in enumerate(selectedRows):
                if i==len(selectedRows)-1:
                    break
                distance.append(round(data[row].distance(data[selectedRows[i+1]]), 4))
        self.selectionLabelUpdate.emit(selectedRows, distance)
    
    def __setSelectedRanges(self,
        selections: Tuple[int],
        continueSelect: bool,
        UnSelect: bool
    ):
        """Different mode of select function."""
        selectedRows = self.selectedRows()
        if not continueSelect:
            self.clearSelection()
        self.setCurrentCell(selections[-1], 0)
        for row in selections:
            isSelected = not row in selectedRows
            self.setRangeSelected(
                QTableWidgetSelectionRange(row, 0, row, self.columnCount()-1),
                isSelected if UnSelect else True)
            self.scrollToItem(self.item(row, 0))
    
    def getLinks(self, row: int) -> List[str]:
        item = self.item(row, 1)
        if not item:
            return []
        return [s for s in item.text().split(',') if s]
    
    def effectiveRange(self, hasName: bool):
        """Row range that can be delete."""
        if hasName:
            return range(self.columnCount())
        else:
            return range(1, self.columnCount()-1)
    
    @pyqtSlot()
    def __emitSelectionChanged(self):
        """Let canvas to show the point selections."""
        self.rowSelectionChanged.emit(self.selectedRows())
    
    @pyqtSlot()
    def clearSelection(self):
        """Overrided the 'clearSelection' slot,
        so it will emit "selectionLabelUpdate"
        signal to clean the selection.
        """
        super(PointTableWidget, self).clearSelection()
        self.selectionLabelUpdate.emit([], [])

class LinkTableWidget(BaseTableWidget):
    
    """Custom table widget for link."""
    
    name = 'Line'
    
    def __init__(self, parent=None):
        super(LinkTableWidget, self).__init__(1, ('Color', 'Points'), parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.editArgs(0, 'ground', 'White', '')
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 130)
    
    def data(self) -> VLink:
        """Yield the digitization of all table data."""
        for row in range(self.rowCount()):
            name = self.item(row, 0).text()
            color = self.item(row, 1).text()
            points = []
            for p in self.item(row, 2).text().split(','):
                if not p:
                    continue
                points.append(int(p.replace('Point', '')))
            yield VLink(name, color, tuple(points), colorQt)
    
    def editArgs(self,
        row: int,
        name: str,
        color: str,
        points: str
    ):
        """Edite a link."""
        for i, e in enumerate((name, color, points)):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==1:
                item.setIcon(colorIcons(e))
            self.setItem(row, i, item)
    
    def findName(self, name: str) -> int:
        """Return row index by input name."""
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if not item:
                continue
            if name == item.text():
                return row
    
    def getPoints(self, row: int) -> List[int]:
        """Get all point names."""
        item = self.item(row, 2)
        if not item:
            return []
        return [int(s.replace('Point', '')) for s in item.text().split(',') if s]
    
    def effectiveRange(self, hasName: bool):
        """Row range that can be delete."""
        return range(self.columnCount())
    
    def clear(self):
        """We should keep the 'ground' left."""
        super(LinkTableWidget, self).clear()
        self.setRowCount(1)
        self.editArgs(0, 'ground', 'White', '')

class ExprTableWidget(BaseTableWidget):
    
    """Expression table."""
    
    def __init__(self, parent=None):
        super(ExprTableWidget, self).__init__(
            0,
            ('p0', 'p1', 'p2', 'p3', 'target'),
            parent
        )
        for column in range(6):
            self.setColumnWidth(column, 60)
        self.exprs = []
    
    def setExpr(self, exprs: List[Tuple[str]]):
        if exprs == self.exprs:
            return
        self.clear()
        self.setRowCount(len(exprs))
        for row, expr in enumerate(exprs):
            self.setItem(row, 5, QTableWidgetItem(expr[-1]))
            for column, e in enumerate(expr[:-1]):
                self.setItem(row, column, QTableWidgetItem(e))
        self.exprs = exprs

class SelectionLabel(QLabel):
    
    """This QLabel can show distance in status bar."""
    
    def __init__(self, *args):
        super(SelectionLabel, self).__init__(*args)
        self.updateSelectPoint()
    
    @pyqtSlot()
    @pyqtSlot(list, list)
    def updateSelectPoint(self,
        points: List[int] =[],
        distance: List[float] =[]
    ):
        """Get points and distance from Point table widget."""
        text = ""
        if points:
            text += "Selected: {}".format('-'.join('[{}]'.format(p) for p in points))
        if distance:
            text += " | {}".format(", ".join('({})'.format(d) for d in distance))
        if text:
            self.setText(text)
        else:
            self.setText("No selection.")
    
    @pyqtSlot(float, float)
    def updateMousePosition(self, x, y):
        """Get the mouse position from canvas
        when press the middle button.
        """
        self.setText("Mouse at: ({}, {})".format(round(x, 4), round(y, 4)))
