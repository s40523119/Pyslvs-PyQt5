# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the link."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List
from core.QtModules import (
    QDialog,
    Qt,
    QIcon,
    QPixmap,
    QListWidgetItem,
    pyqtSlot,
    QDialogButtonBox,
)
from core.graphics import colorName, colorIcons
from core.libs import VPoint, VLink
from .Ui_edit_link import Ui_Dialog


class EditLinkDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the target path after closed.
    """
    
    def __init__(self,
        points: List[VPoint],
        links: List[VLink],
        pos: bool = False,
        parent=None
    ):
        super(EditLinkDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.points = points
        self.links = links
        icon = self.windowIcon()
        self.PointIcon = QIcon(QPixmap(":/icons/bearing.png"))
        for i, e in enumerate(colorName):
            self.Color.insertItem(i, colorIcons(e), e)
        for i in range(len(self.points)):
            self.noSelected.addItem(
                QListWidgetItem(self.PointIcon, 'Point{}'.format(i))
            )
        if pos is False:
            self.Link.addItem(icon, "New link")
            self.Link.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Blue'))
        else:
            for vlink in self.links:
                self.Link.insertItem(i, icon, vlink.name)
            self.Link.setCurrentIndex(pos)
        self.name_edit.textChanged.connect(self.__isOk)
        self.__isOk()
    
    @pyqtSlot(str)
    def __isOk(self, p0=None):
        """Set button box enable if options are ok."""
        del p0
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            self.__legalName(self.name_edit.text())
        )
    
    def __legalName(self, name: str) -> bool:
        """Return this name is usable or not."""
        if not name.isidentifier():
            return False
        for i, vlink in enumerate(self.links):
            if (i != self.Link.currentIndex()) and (name == vlink.name):
                return False
        return True
    
    @pyqtSlot(int)
    def on_Link_currentIndexChanged(self, index):
        """Load the parameters of the link."""
        if len(self.links) > index:
            vlink = self.links[index]
            self.name_edit.setText(vlink.name)
            self.Color.setCurrentIndex(self.Color.findText(vlink.colorSTR))
            self.noSelected.clear()
            self.selected.clear()
            for point in vlink.points:
                self.selected.addItem(
                    QListWidgetItem(self.PointIcon, 'Point{}'.format(point))
                )
            for point in range(len(self.points)):
                if point in vlink.points:
                    continue
                self.noSelected.addItem(
                    QListWidgetItem(self.PointIcon, 'Point{}'.format(point))
                )
        self.name_edit.setEnabled(index > 0)
        self.Color.setEnabled(index > 0)
    
    @pyqtSlot(QListWidgetItem)
    def on_noSelected_itemDoubleClicked(self, item):
        """Add item to selected list."""
        self.selected.addItem(
            self.noSelected.takeItem(self.noSelected.row(item))
        )
    
    @pyqtSlot(QListWidgetItem)
    def on_selected_itemDoubleClicked(self, item):
        """Add item to no selected list."""
        self.noSelected.addItem(
            self.selected.takeItem(self.selected.row(item))
        )
