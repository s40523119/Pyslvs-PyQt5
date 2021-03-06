# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ahshoe\Desktop\Pyslvs-PyQt5\core\widgets\inputs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(408, 616)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.joint_groupBox = QtWidgets.QGroupBox(Form)
        self.joint_groupBox.setObjectName("joint_groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.joint_groupBox)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.joint_list_lable = QtWidgets.QLabel(self.joint_groupBox)
        self.joint_list_lable.setObjectName("joint_list_lable")
        self.verticalLayout_13.addWidget(self.joint_list_lable)
        self.joint_list = QtWidgets.QListWidget(self.joint_groupBox)
        self.joint_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.joint_list.setObjectName("joint_list")
        self.verticalLayout_13.addWidget(self.joint_list)
        self.horizontalLayout.addLayout(self.verticalLayout_13)
        self.inputs_label_right1 = QtWidgets.QLabel(self.joint_groupBox)
        self.inputs_label_right1.setObjectName("inputs_label_right1")
        self.horizontalLayout.addWidget(self.inputs_label_right1)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.base_link_list_lable = QtWidgets.QLabel(self.joint_groupBox)
        self.base_link_list_lable.setObjectName("base_link_list_lable")
        self.verticalLayout_15.addWidget(self.base_link_list_lable)
        self.base_link_list = QtWidgets.QListWidget(self.joint_groupBox)
        self.base_link_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.base_link_list.setObjectName("base_link_list")
        self.verticalLayout_15.addWidget(self.base_link_list)
        self.horizontalLayout.addLayout(self.verticalLayout_15)
        self.inputs_label_right2 = QtWidgets.QLabel(self.joint_groupBox)
        self.inputs_label_right2.setObjectName("inputs_label_right2")
        self.horizontalLayout.addWidget(self.inputs_label_right2)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.drive_link_list_lable = QtWidgets.QLabel(self.joint_groupBox)
        self.drive_link_list_lable.setObjectName("drive_link_list_lable")
        self.verticalLayout_16.addWidget(self.drive_link_list_lable)
        self.drive_link_list = QtWidgets.QListWidget(self.joint_groupBox)
        self.drive_link_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.drive_link_list.setObjectName("drive_link_list")
        self.verticalLayout_16.addWidget(self.drive_link_list)
        self.variable_list_add = QtWidgets.QPushButton(self.joint_groupBox)
        self.variable_list_add.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/arrow_down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.variable_list_add.setIcon(icon)
        self.variable_list_add.setObjectName("variable_list_add")
        self.verticalLayout_16.addWidget(self.variable_list_add)
        self.horizontalLayout.addLayout(self.verticalLayout_16)
        self.verticalLayout.addWidget(self.joint_groupBox)
        self.variable_groupBox = QtWidgets.QGroupBox(Form)
        self.variable_groupBox.setObjectName("variable_groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.variable_groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.inputs_dial_layout = QtWidgets.QHBoxLayout()
        self.inputs_dial_layout.setObjectName("inputs_dial_layout")
        self.variable_list = QtWidgets.QListWidget(self.variable_groupBox)
        self.variable_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.variable_list.setObjectName("variable_list")
        self.inputs_dial_layout.addWidget(self.variable_list)
        self.line_5 = QtWidgets.QFrame(self.variable_groupBox)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.inputs_dial_layout.addWidget(self.line_5)
        self.verticalLayout_4.addLayout(self.inputs_dial_layout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.variable_remove = QtWidgets.QPushButton(self.variable_groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.variable_remove.setIcon(icon1)
        self.variable_remove.setObjectName("variable_remove")
        self.horizontalLayout_3.addWidget(self.variable_remove)
        self.line = QtWidgets.QFrame(self.variable_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.variable_speed_label = QtWidgets.QLabel(self.variable_groupBox)
        self.variable_speed_label.setObjectName("variable_speed_label")
        self.horizontalLayout_4.addWidget(self.variable_speed_label)
        self.variable_speed = QtWidgets.QSpinBox(self.variable_groupBox)
        self.variable_speed.setEnabled(False)
        self.variable_speed.setMinimum(-100)
        self.variable_speed.setMaximum(100)
        self.variable_speed.setSingleStep(5)
        self.variable_speed.setProperty("value", -10)
        self.variable_speed.setObjectName("variable_speed")
        self.horizontalLayout_4.addWidget(self.variable_speed)
        self.verticalLayout_18.addLayout(self.horizontalLayout_4)
        self.extremeRebound = QtWidgets.QCheckBox(self.variable_groupBox)
        self.extremeRebound.setChecked(True)
        self.extremeRebound.setObjectName("extremeRebound")
        self.verticalLayout_18.addWidget(self.extremeRebound)
        self.horizontalLayout_3.addLayout(self.verticalLayout_18)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.variable_play = QtWidgets.QPushButton(self.variable_groupBox)
        self.variable_play.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.variable_play.setIcon(icon2)
        self.variable_play.setCheckable(True)
        self.variable_play.setObjectName("variable_play")
        self.verticalLayout_3.addWidget(self.variable_play)
        self.variable_stop = QtWidgets.QPushButton(self.variable_groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/interrupted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.variable_stop.setIcon(icon3)
        self.variable_stop.setObjectName("variable_stop")
        self.verticalLayout_3.addWidget(self.variable_stop)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.line_2 = QtWidgets.QFrame(self.variable_groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.dial_spinbox = QtWidgets.QDoubleSpinBox(self.variable_groupBox)
        self.dial_spinbox.setEnabled(False)
        self.dial_spinbox.setMinimum(-360.0)
        self.dial_spinbox.setMaximum(360.0)
        self.dial_spinbox.setObjectName("dial_spinbox")
        self.horizontalLayout_3.addWidget(self.dial_spinbox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.variable_groupBox)
        self.record_groupBox = QtWidgets.QGroupBox(Form)
        self.record_groupBox.setObjectName("record_groupBox")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.record_groupBox)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.record_interval_label = QtWidgets.QLabel(self.record_groupBox)
        self.record_interval_label.setObjectName("record_interval_label")
        self.horizontalLayout_6.addWidget(self.record_interval_label)
        self.record_interval = QtWidgets.QDoubleSpinBox(self.record_groupBox)
        self.record_interval.setMinimum(0.5)
        self.record_interval.setMaximum(10.0)
        self.record_interval.setProperty("value", 6.0)
        self.record_interval.setObjectName("record_interval")
        self.horizontalLayout_6.addWidget(self.record_interval)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.record_show = QtWidgets.QCheckBox(self.record_groupBox)
        self.record_show.setChecked(True)
        self.record_show.setObjectName("record_show")
        self.horizontalLayout_6.addWidget(self.record_show)
        self.verticalLayout_22.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.record_list = QtWidgets.QListWidget(self.record_groupBox)
        self.record_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.record_list.setObjectName("record_list")
        item = QtWidgets.QListWidgetItem()
        self.record_list.addItem(item)
        self.horizontalLayout_8.addWidget(self.record_list)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.record_start = QtWidgets.QPushButton(self.record_groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.record_start.setIcon(icon4)
        self.record_start.setCheckable(True)
        self.record_start.setObjectName("record_start")
        self.verticalLayout_2.addWidget(self.record_start)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.record_remove = QtWidgets.QPushButton(self.record_groupBox)
        self.record_remove.setIcon(icon1)
        self.record_remove.setObjectName("record_remove")
        self.verticalLayout_2.addWidget(self.record_remove)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.verticalLayout_22.addLayout(self.horizontalLayout_8)
        self.verticalLayout.addWidget(self.record_groupBox)

        self.retranslateUi(Form)
        self.record_list.setCurrentRow(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.joint_groupBox.setTitle(_translate("Form", "Inputs"))
        self.joint_list_lable.setText(_translate("Form", "Points"))
        self.joint_list.setStatusTip(_translate("Form", "Choose a point to be a revolute joint."))
        self.inputs_label_right1.setText(_translate("Form", ">>"))
        self.base_link_list_lable.setText(_translate("Form", "Base link"))
        self.base_link_list.setStatusTip(_translate("Form", "Coordinate reference."))
        self.inputs_label_right2.setText(_translate("Form", ">>"))
        self.drive_link_list_lable.setText(_translate("Form", "Drive link"))
        self.drive_link_list.setStatusTip(_translate("Form", "Coordinate movement reference."))
        self.variable_list_add.setStatusTip(_translate("Form", "Add to variable list with above settings."))
        self.variable_groupBox.setTitle(_translate("Form", "Variables"))
        self.variable_list.setStatusTip(_translate("Form", "All the variable of this mechanism."))
        self.variable_remove.setStatusTip(_translate("Form", "Delete the specified variable."))
        self.variable_speed_label.setText(_translate("Form", "Speed:"))
        self.variable_speed.setStatusTip(_translate("Form", "Speed value of the auto driver."))
        self.variable_speed.setSuffix(_translate("Form", " rpm"))
        self.extremeRebound.setStatusTip(_translate("Form", "When solver calls error, auto driver will change the direction."))
        self.extremeRebound.setText(_translate("Form", "Extreme rebound"))
        self.variable_play.setStatusTip(_translate("Form", "Start / Pause the auto driver of this variables."))
        self.variable_stop.setStatusTip(_translate("Form", "Stop the auto driver and return to original place."))
        self.record_groupBox.setTitle(_translate("Form", "Records"))
        self.record_interval_label.setText(_translate("Form", "Interval: "))
        self.record_interval.setStatusTip(_translate("Form", "Each coordinate will be recorded after this angle value."))
        self.record_interval.setSuffix(_translate("Form", "°"))
        self.record_show.setStatusTip(_translate("Form", "Show path data on the canvas."))
        self.record_show.setText(_translate("Form", "Show path data"))
        self.record_list.setStatusTip(_translate("Form", "All recorded path data of this workbook."))
        __sortingEnabled = self.record_list.isSortingEnabled()
        self.record_list.setSortingEnabled(False)
        item = self.record_list.item(0)
        item.setText(_translate("Form", "Auto preview"))
        self.record_list.setSortingEnabled(__sortingEnabled)
        self.record_start.setStatusTip(_translate("Form", "Start / Stop record."))
        self.record_remove.setStatusTip(_translate("Form", "Delete the specified path data."))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

