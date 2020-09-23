# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\design\agreement.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.h_layout_central = QtWidgets.QHBoxLayout(self.central_widget)
        self.h_layout_central.setContentsMargins(0, 0, 0, 0)
        self.h_layout_central.setObjectName("h_layout_central")
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.table_tab = QtWidgets.QWidget()
        self.table_tab.setObjectName("table_tab")
        self.h_layout_table = QtWidgets.QHBoxLayout(self.table_tab)
        self.h_layout_table.setObjectName("h_layout_table")
        self.table_view_main = QtWidgets.QTableView(self.table_tab)
        self.table_view_main.setObjectName("table_view_main")
        self.h_layout_table.addWidget(self.table_view_main)
        self.group_box_table_settings = QtWidgets.QGroupBox(self.table_tab)
        self.group_box_table_settings.setObjectName("group_box_table_settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_box_table_settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.v_layout_from = QtWidgets.QVBoxLayout()
        self.v_layout_from.setObjectName("v_layout_from")
        self.label_from = QtWidgets.QLabel(self.group_box_table_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_from.sizePolicy().hasHeightForWidth())
        self.label_from.setSizePolicy(sizePolicy)
        self.label_from.setObjectName("label_from")
        self.v_layout_from.addWidget(self.label_from)
        self.date_time_from = QtWidgets.QDateTimeEdit(self.group_box_table_settings)
        self.date_time_from.setCalendarPopup(True)
        self.date_time_from.setObjectName("date_time_from")
        self.v_layout_from.addWidget(self.date_time_from)
        self.v_layout_from.setStretch(0, 1)
        self.v_layout_from.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.v_layout_from)
        self.v_layout_to = QtWidgets.QVBoxLayout()
        self.v_layout_to.setObjectName("v_layout_to")
        self.label_to = QtWidgets.QLabel(self.group_box_table_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_to.sizePolicy().hasHeightForWidth())
        self.label_to.setSizePolicy(sizePolicy)
        self.label_to.setObjectName("label_to")
        self.v_layout_to.addWidget(self.label_to)
        self.date_time_to = QtWidgets.QDateTimeEdit(self.group_box_table_settings)
        self.date_time_to.setCalendarPopup(True)
        self.date_time_to.setObjectName("date_time_to")
        self.v_layout_to.addWidget(self.date_time_to)
        self.v_layout_to.setStretch(0, 1)
        self.v_layout_to.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.v_layout_to)
        self.push_button_all_period = QtWidgets.QPushButton(self.group_box_table_settings)
        self.push_button_all_period.setObjectName("push_button_all_period")
        self.verticalLayout_3.addWidget(self.push_button_all_period)
        self.h_layout_step = QtWidgets.QHBoxLayout()
        self.h_layout_step.setObjectName("h_layout_step")
        self.push_button_prev = QtWidgets.QPushButton(self.group_box_table_settings)
        self.push_button_prev.setObjectName("push_button_prev")
        self.h_layout_step.addWidget(self.push_button_prev)
        self.push_button_next = QtWidgets.QPushButton(self.group_box_table_settings)
        self.push_button_next.setObjectName("push_button_next")
        self.h_layout_step.addWidget(self.push_button_next)
        self.h_layout_step.setStretch(0, 1)
        self.h_layout_step.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.h_layout_step)
        self.h_layout_switch = QtWidgets.QHBoxLayout()
        self.h_layout_switch.setObjectName("h_layout_switch")
        self.spin_box_switch = QtWidgets.QSpinBox(self.group_box_table_settings)
        self.spin_box_switch.setMinimum(1)
        self.spin_box_switch.setObjectName("spin_box_switch")
        self.h_layout_switch.addWidget(self.spin_box_switch)
        self.push_button_switch = QtWidgets.QPushButton(self.group_box_table_settings)
        self.push_button_switch.setObjectName("push_button_switch")
        self.h_layout_switch.addWidget(self.push_button_switch)
        self.h_layout_switch.setStretch(0, 1)
        self.h_layout_switch.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.h_layout_switch)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.push_button_build_report = QtWidgets.QPushButton(self.group_box_table_settings)
        self.push_button_build_report.setObjectName("push_button_build_report")
        self.verticalLayout_3.addWidget(self.push_button_build_report)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_3.setStretch(4, 1)
        self.verticalLayout_3.setStretch(5, 3)
        self.verticalLayout_3.setStretch(6, 1)
        self.h_layout_table.addWidget(self.group_box_table_settings)
        self.h_layout_table.setStretch(0, 5)
        self.h_layout_table.setStretch(1, 2)
        self.tab_widget.addTab(self.table_tab, "")
        self.charts_tab = QtWidgets.QWidget()
        self.charts_tab.setObjectName("charts_tab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.charts_tab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.v_layout_charts = QtWidgets.QVBoxLayout()
        self.v_layout_charts.setObjectName("v_layout_charts")
        self.h_layout_subcharts_1 = QtWidgets.QHBoxLayout()
        self.h_layout_subcharts_1.setObjectName("h_layout_subcharts_1")
        self.v_layout_volunteer_chart = QtWidgets.QVBoxLayout()
        self.v_layout_volunteer_chart.setObjectName("v_layout_volunteer_chart")
        self.h_layout_subcharts_1.addLayout(self.v_layout_volunteer_chart)
        self.v_layout_section_chart = QtWidgets.QVBoxLayout()
        self.v_layout_section_chart.setObjectName("v_layout_section_chart")
        self.h_layout_subcharts_1.addLayout(self.v_layout_section_chart)
        self.h_layout_subcharts_1.setStretch(0, 1)
        self.h_layout_subcharts_1.setStretch(1, 1)
        self.v_layout_charts.addLayout(self.h_layout_subcharts_1)
        self.v_layout_block_chart = QtWidgets.QVBoxLayout()
        self.v_layout_block_chart.setObjectName("v_layout_block_chart")
        self.v_layout_charts.addLayout(self.v_layout_block_chart)
        self.v_layout_charts.setStretch(0, 2)
        self.v_layout_charts.setStretch(1, 3)
        self.horizontalLayout_5.addLayout(self.v_layout_charts)
        self.v_layout_charts_right = QtWidgets.QVBoxLayout()
        self.v_layout_charts_right.setObjectName("v_layout_charts_right")
        self.group_box_charts_settings = QtWidgets.QGroupBox(self.charts_tab)
        self.group_box_charts_settings.setObjectName("group_box_charts_settings")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.group_box_charts_settings)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.group_box_charts_report = QtWidgets.QGroupBox(self.group_box_charts_settings)
        self.group_box_charts_report.setObjectName("group_box_charts_report")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group_box_charts_report)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.combo_box_charts_report = QtWidgets.QComboBox(self.group_box_charts_report)
        self.combo_box_charts_report.setObjectName("combo_box_charts_report")
        self.verticalLayout_2.addWidget(self.combo_box_charts_report)
        self.push_button_charts_report = QtWidgets.QPushButton(self.group_box_charts_report)
        self.push_button_charts_report.setObjectName("push_button_charts_report")
        self.verticalLayout_2.addWidget(self.push_button_charts_report)
        self.push_button_charts_delete_report = QtWidgets.QPushButton(self.group_box_charts_report)
        self.push_button_charts_delete_report.setObjectName("push_button_charts_delete_report")
        self.verticalLayout_2.addWidget(self.push_button_charts_delete_report)
        self.verticalLayout_4.addWidget(self.group_box_charts_report)
        self.group_box_volunteer = QtWidgets.QGroupBox(self.group_box_charts_settings)
        self.group_box_volunteer.setObjectName("group_box_volunteer")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.group_box_volunteer)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.v_layout_volunteer = QtWidgets.QVBoxLayout()
        self.v_layout_volunteer.setObjectName("v_layout_volunteer")
        self.label_volunteer = QtWidgets.QLabel(self.group_box_volunteer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_volunteer.sizePolicy().hasHeightForWidth())
        self.label_volunteer.setSizePolicy(sizePolicy)
        self.label_volunteer.setObjectName("label_volunteer")
        self.v_layout_volunteer.addWidget(self.label_volunteer)
        self.spin_box_volunteer = QtWidgets.QSpinBox(self.group_box_volunteer)
        self.spin_box_volunteer.setMinimum(1)
        self.spin_box_volunteer.setMaximum(9999999)
        self.spin_box_volunteer.setObjectName("spin_box_volunteer")
        self.v_layout_volunteer.addWidget(self.spin_box_volunteer)
        self.v_layout_volunteer.setStretch(0, 1)
        self.v_layout_volunteer.setStretch(1, 2)
        self.horizontalLayout_6.addLayout(self.v_layout_volunteer)
        self.push_button_volunteer = QtWidgets.QPushButton(self.group_box_volunteer)
        self.push_button_volunteer.setObjectName("push_button_volunteer")
        self.horizontalLayout_6.addWidget(self.push_button_volunteer)
        self.verticalLayout_4.addWidget(self.group_box_volunteer)
        self.group_box_section = QtWidgets.QGroupBox(self.group_box_charts_settings)
        self.group_box_section.setObjectName("group_box_section")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.group_box_section)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.v_layout_section = QtWidgets.QVBoxLayout()
        self.v_layout_section.setObjectName("v_layout_section")
        self.label_section = QtWidgets.QLabel(self.group_box_section)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_section.sizePolicy().hasHeightForWidth())
        self.label_section.setSizePolicy(sizePolicy)
        self.label_section.setObjectName("label_section")
        self.v_layout_section.addWidget(self.label_section)
        self.spin_box_section = QtWidgets.QSpinBox(self.group_box_section)
        self.spin_box_section.setMinimum(1)
        self.spin_box_section.setMaximum(9999999)
        self.spin_box_section.setObjectName("spin_box_section")
        self.v_layout_section.addWidget(self.spin_box_section)
        self.v_layout_section.setStretch(0, 1)
        self.v_layout_section.setStretch(1, 2)
        self.horizontalLayout_7.addLayout(self.v_layout_section)
        self.push_button_section = QtWidgets.QPushButton(self.group_box_section)
        self.push_button_section.setObjectName("push_button_section")
        self.horizontalLayout_7.addWidget(self.push_button_section)
        self.verticalLayout_4.addWidget(self.group_box_section)
        spacerItem1 = QtWidgets.QSpacerItem(20, 171, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 2)
        self.verticalLayout_4.setStretch(2, 2)
        self.verticalLayout_4.setStretch(3, 4)
        self.v_layout_charts_right.addWidget(self.group_box_charts_settings)
        self.group_box_categories = QtWidgets.QGroupBox(self.charts_tab)
        self.group_box_categories.setObjectName("group_box_categories")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.group_box_categories)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.color_category_1 = QtWidgets.QWidget(self.group_box_categories)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_category_1.sizePolicy().hasHeightForWidth())
        self.color_category_1.setSizePolicy(sizePolicy)
        self.color_category_1.setMinimumSize(QtCore.QSize(15, 15))
        self.color_category_1.setMaximumSize(QtCore.QSize(15, 15))
        self.color_category_1.setStyleSheet("background-color: rgb(44, 160, 44);")
        self.color_category_1.setObjectName("color_category_1")
        self.horizontalLayout.addWidget(self.color_category_1)
        self.label_category_1 = QtWidgets.QLabel(self.group_box_categories)
        self.label_category_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_category_1.setObjectName("label_category_1")
        self.horizontalLayout.addWidget(self.label_category_1)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.color_category_2 = QtWidgets.QWidget(self.group_box_categories)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_category_2.sizePolicy().hasHeightForWidth())
        self.color_category_2.setSizePolicy(sizePolicy)
        self.color_category_2.setMinimumSize(QtCore.QSize(15, 15))
        self.color_category_2.setMaximumSize(QtCore.QSize(15, 15))
        self.color_category_2.setStyleSheet("background-color: rgb(31, 119, 180);")
        self.color_category_2.setObjectName("color_category_2")
        self.horizontalLayout_2.addWidget(self.color_category_2)
        self.label_category_2 = QtWidgets.QLabel(self.group_box_categories)
        self.label_category_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_category_2.setObjectName("label_category_2")
        self.horizontalLayout_2.addWidget(self.label_category_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.color_category_3 = QtWidgets.QWidget(self.group_box_categories)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_category_3.sizePolicy().hasHeightForWidth())
        self.color_category_3.setSizePolicy(sizePolicy)
        self.color_category_3.setMinimumSize(QtCore.QSize(15, 15))
        self.color_category_3.setMaximumSize(QtCore.QSize(15, 15))
        self.color_category_3.setStyleSheet("background-color: rgb(255, 127, 14);")
        self.color_category_3.setObjectName("color_category_3")
        self.horizontalLayout_3.addWidget(self.color_category_3)
        self.label_category_3 = QtWidgets.QLabel(self.group_box_categories)
        self.label_category_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_category_3.setObjectName("label_category_3")
        self.horizontalLayout_3.addWidget(self.label_category_3)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.color_category_4 = QtWidgets.QWidget(self.group_box_categories)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_category_4.sizePolicy().hasHeightForWidth())
        self.color_category_4.setSizePolicy(sizePolicy)
        self.color_category_4.setMinimumSize(QtCore.QSize(15, 15))
        self.color_category_4.setMaximumSize(QtCore.QSize(15, 15))
        self.color_category_4.setStyleSheet("background-color: rgb(214, 39, 40);")
        self.color_category_4.setObjectName("color_category_4")
        self.horizontalLayout_4.addWidget(self.color_category_4)
        self.label_category_4 = QtWidgets.QLabel(self.group_box_categories)
        self.label_category_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_category_4.setObjectName("label_category_4")
        self.horizontalLayout_4.addWidget(self.label_category_4)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.v_layout_charts_right.addWidget(self.group_box_categories)
        self.v_layout_charts_right.setStretch(0, 7)
        self.v_layout_charts_right.setStretch(1, 3)
        self.horizontalLayout_5.addLayout(self.v_layout_charts_right)
        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 2)
        self.tab_widget.addTab(self.charts_tab, "")
        self.rating_tab = QtWidgets.QWidget()
        self.rating_tab.setObjectName("rating_tab")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.rating_tab)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.table_view_rating = QtWidgets.QTableView(self.rating_tab)
        self.table_view_rating.setObjectName("table_view_rating")
        self.horizontalLayout_8.addWidget(self.table_view_rating)
        self.group_box_rating = QtWidgets.QGroupBox(self.rating_tab)
        self.group_box_rating.setObjectName("group_box_rating")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.group_box_rating)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.group_box_rating_report = QtWidgets.QGroupBox(self.group_box_rating)
        self.group_box_rating_report.setObjectName("group_box_rating_report")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.group_box_rating_report)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.combo_box_rating_report = QtWidgets.QComboBox(self.group_box_rating_report)
        self.combo_box_rating_report.setObjectName("combo_box_rating_report")
        self.verticalLayout_5.addWidget(self.combo_box_rating_report)
        self.push_button_rating_report = QtWidgets.QPushButton(self.group_box_rating_report)
        self.push_button_rating_report.setObjectName("push_button_rating_report")
        self.verticalLayout_5.addWidget(self.push_button_rating_report)
        self.push_button_rating_delete_report = QtWidgets.QPushButton(self.group_box_rating_report)
        self.push_button_rating_delete_report.setObjectName("push_button_rating_delete_report")
        self.verticalLayout_5.addWidget(self.push_button_rating_delete_report)
        self.verticalLayout_6.addWidget(self.group_box_rating_report)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_8.addWidget(self.group_box_rating)
        self.horizontalLayout_8.setStretch(0, 5)
        self.horizontalLayout_8.setStretch(1, 2)
        self.tab_widget.addTab(self.rating_tab, "")
        self.h_layout_central.addWidget(self.tab_widget)
        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оценка согласованности"))
        self.group_box_table_settings.setTitle(_translate("MainWindow", "Настройки отображения:"))
        self.label_from.setText(_translate("MainWindow", "Начало периода:"))
        self.date_time_from.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd HH:mm:ss"))
        self.label_to.setText(_translate("MainWindow", "Конец периода:"))
        self.date_time_to.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd HH:mm:ss"))
        self.push_button_all_period.setText(_translate("MainWindow", "Весь период"))
        self.push_button_prev.setText(_translate("MainWindow", "<"))
        self.push_button_next.setText(_translate("MainWindow", ">"))
        self.push_button_switch.setText(_translate("MainWindow", "Перейти"))
        self.push_button_build_report.setText(_translate("MainWindow", "Построить отчет"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.table_tab), _translate("MainWindow", "Таблица разметки"))
        self.group_box_charts_settings.setTitle(_translate("MainWindow", "Настройки диаграмм:"))
        self.group_box_charts_report.setTitle(_translate("MainWindow", "Выбор отчета:"))
        self.push_button_charts_report.setText(_translate("MainWindow", "Показать"))
        self.push_button_charts_delete_report.setText(_translate("MainWindow", "Удалить отчет"))
        self.group_box_volunteer.setTitle(_translate("MainWindow", "Выбор волонтера:"))
        self.label_volunteer.setText(_translate("MainWindow", "ID волонтера"))
        self.push_button_volunteer.setText(_translate("MainWindow", "Показать"))
        self.group_box_section.setTitle(_translate("MainWindow", "Выбор абзаца:"))
        self.label_section.setText(_translate("MainWindow", "ID абзаца"))
        self.push_button_section.setText(_translate("MainWindow", "Показать"))
        self.group_box_categories.setTitle(_translate("MainWindow", "Категории:"))
        self.label_category_1.setText(_translate("MainWindow", "Кворум"))
        self.label_category_2.setText(_translate("MainWindow", "Возможный кворум"))
        self.label_category_3.setText(_translate("MainWindow", "Мнения разделились"))
        self.label_category_4.setText(_translate("MainWindow", "Установленное меньшинство"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.charts_tab), _translate("MainWindow", "Диаграммы согласованности"))
        self.group_box_rating.setTitle(_translate("MainWindow", "Настройка отображения:"))
        self.group_box_rating_report.setTitle(_translate("MainWindow", "Выбор отчета:"))
        self.push_button_rating_report.setText(_translate("MainWindow", "Показать"))
        self.push_button_rating_delete_report.setText(_translate("MainWindow", "Удалить отчет"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.rating_tab), _translate("MainWindow", "Рейтинг волонтёров"))