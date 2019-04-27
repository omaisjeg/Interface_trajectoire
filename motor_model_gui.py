#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QSpinBox, QLineEdit, QProgressBar,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
                             QApplication)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg\
                                        as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT\
                                        as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import yaml


class MotorModel(QWidget):
    def __init__(self, queue):
        super().__init__()
        # self.init_parameters()
        self.init_ui()
        self.queue = queue

    def init_parameters(self):
        with open('config.yml', 'r') as f:
            config = yaml.load(f.read())
        self.port_name = config['port_name']
        self.baud_rate = config['baud_rate']
        self.pwm = config['pwm']
        self.ts = config['ts']
        self.nb_measure = config['nb_measure']
        self.nb_sample = config['nb_sample']
        self.wait_time = config['wait_time']

    def set_pwm(self, new_pwm):
        self.pwm = new_pwm

    def set_ts(self, new_ts):
        self.ts = new_ts

    def set_nb_measure(self, new_nb_measure):
        self.nb_measure = new_nb_measure
        self.progress_bar.setMaximum(self.nb_measure)
        self.progress_bar.setValue(self.nb_measure)

    def set_nb_sample(self, new_nb_sample):
        self.nb_sample = new_nb_sample

    def set_wait_time(self, new_wait_time):
        self.wait_time = new_wait_time

    def init_ui(self):

        # Parameters
        # self.pwm_spin = QSpinBox()
        # self.pwm_spin.setMinimum(0)
        # self.pwm_spin.setMaximum(255)
        # self.pwm_spin.setValue(self.pwm)
        # self.pwm_spin.valueChanged.connect(self.set_pwm)
        #
        # self.ts_spin = QSpinBox()
        # self.ts_spin.setMinimum(1)
        # self.ts_spin.setMaximum(100)
        # self.ts_spin.setValue(self.ts)
        # self.ts_spin.valueChanged.connect(self.set_ts)
        #
        # self.nb_measure_spin = QSpinBox()
        # self.nb_measure_spin.setMinimum(1)
        # self.nb_measure_spin.setMaximum(100)
        # self.nb_measure_spin.setValue(self.nb_measure)
        # self.nb_measure_spin.valueChanged.connect(self.set_nb_measure)
        #
        # self.nb_sample_spin = QSpinBox()
        # self.nb_sample_spin.setMinimum(10)
        # self.nb_sample_spin.setMaximum(1000)
        # self.nb_sample_spin.setValue(self.nb_sample)
        # self.nb_sample_spin.valueChanged.connect(self.set_nb_sample)
        #
        # self.wait_time_spin = QSpinBox()
        # self.wait_time_spin.setMinimum(100)
        # self.wait_time_spin.setMaximum(10000)
        # self.wait_time_spin.setValue(self.wait_time)
        # self.wait_time_spin.valueChanged.connect(self.set_wait_time)

        # parameters_layout = QFormLayout()
        # parameters_layout.addRow('PWM', self.pwm_spin)
        # parameters_layout.addRow('Sample Time', self.ts_spin)
        # parameters_layout.addRow('Number of Measure', self.nb_measure_spin)
        # parameters_layout.addRow('Number of Sample', self.nb_sample_spin)
        # parameters_layout.addRow('Wait Time', self.wait_time_spin)

        # parameters_group = QGroupBox('Measure parameters')
        # parameters_group.setLayout(parameters_layout)

        # self.k_edit = QLineEdit()
        # self.k_edit.setReadOnly(True)
        #
        # self.tau_edit = QLineEdit()
        # self.tau_edit.setReadOnly(True)
        #
        # caracteristics_layout = QFormLayout()
        # caracteristics_layout.addRow('K', self.k_edit)
        # caracteristics_layout.addRow('Tau', self.tau_edit)
        #
        # caracteristics_group = QGroupBox('Motor caracteristics')
        # caracteristics_group.setLayout(caracteristics_layout)
        #
        # param_caract_layout = QVBoxLayout()
        # param_caract_layout.addWidget(parameters_group)
        # param_caract_layout.addWidget(caracteristics_group)
        # param_caract_layout.addStretch()

        # Display
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # self.progress_bar = QProgressBar()
        # self.progress_bar.setMinimum(0)
        # self.progress_bar.setMaximum(self.nb_measure)
        # self.progress_bar.setValue(self.nb_measure)

        self.run_button = QPushButton('Run')
        self.run_button.clicked.connect(self.plot)

        display_layout = QVBoxLayout()
        display_layout.addWidget(self.toolbar)
        display_layout.addWidget(self.canvas)
        # display_layout.addWidget(self.progress_bar)
        display_layout.addWidget(self.run_button)

        # Main
        # main_layout = QHBoxLayout()
        # main_layout.addLayout(param_caract_layout)
        # main_layout.addLayout(display_layout)

        self.setLayout(display_layout)

    def plot(self):
        """Plot step response"""
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        lines, = ax.plot(np.zeros(100), np.zeros(100))
        ax.set_title('Motor Step Response')
        ax.legend()
        ax.set_xlim([-.2, 3.2])
        ax.set_ylim([-.2, 2.2])

        ani = animation.FuncAnimation(self.figure, self.refresh,10000,
                                      fargs=(lines, ax), interval=20)

        self.canvas.draw()

    def refresh(self, i,lines, ax):

        print(self.queue.qsize(), "eruinsetuinrset")

        x_queue, y_queue, theta_queue = self.queue.get()

        x = np.array(x_queue)/100
        y = np.array(y_queue)/100
        print(x[-5:-1], y[-5:-1], len(x), len(y))
        theta = np.array(theta_queue)
        lines.set_data(x, y)

        return ax


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = MotorModel()
    mm.show()
    sys.exit(app.exec_())
