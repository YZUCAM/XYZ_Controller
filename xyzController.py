from PyQt5.Qt import QWidget, QApplication, QThread, pyqtSignal, QShortcut
from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence
from ui_xyzController import Ui_xyz_controller
import time
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# create figure plot class
class MplCanvas(FigureCanvasQTAgg):
    '''matplotlib canvas setting'''
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor(None)
        fig.patch.set_alpha(0)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim([0, 22])
        self.axes.set_ylim([0, 22])
        self.axes.spines['bottom'].set_color('w')
        self.axes.spines['top'].set_color('w')
        self.axes.spines['right'].set_color('w')
        self.axes.spines['left'].set_color('w')
        self.axes.tick_params(axis='x', colors='w')
        self.axes.tick_params(axis='y', colors='w')
        self.axes.set_facecolor('black')
        self.axes.set_alpha(0)
        super(MplCanvas, self).__init__(fig)
        self._plot_ref = None

    def xy_plot(self, x, y):
        pass

    # def update_plot(self, x, y):
    #     if self._plot_ref is None:
    #         # First time we have no plot reference, so do a normal plot.
    #         # .plot returns a list of line <reference>s, as we're
    #         # only getting one we can take the first element.
    #         plot_refs = self.axes.plot(x, y, 'y')
    #         self._plot_ref = plot_refs[0]
    #         print(plot_refs[0])
    #     else:
    #         self._plot_ref.set_xdata(x)
    #         self._plot_ref.set_ydata(y)
    #     self.axes.plot(x,y)

# start a new thread to continue read xyz coordinates
class BackendThread(QThread):
    # update_coordinates = pyqtSignal(str, str, str)
    get_x =pyqtSignal()
    get_y = pyqtSignal()
    get_z = pyqtSignal()
    update_graph = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.beckend_flg = True

    def run(self):
        while self.beckend_flg:
            self.get_x.emit()
            self.get_y.emit()
            self.get_z.emit()
            self.update_graph.emit()
            time.sleep(1)
"""now the problem is how to pass the x, y, z value from other package"""

class Window(QWidget, Ui_xyz_controller):
    '''define signal'''
    up_signal = pyqtSignal(float)
    down_signal = pyqtSignal(float)
    left_signal = pyqtSignal(float)
    right_signal = pyqtSignal(float)
    z_up_signal = pyqtSignal(float)
    z_down_signal = pyqtSignal(float)
    go_home_signal = pyqtSignal(float)
    send_xyz_signal = pyqtSignal(float, float, float)
    # send_xy_signal = pyqtSignal(float, float)
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ''' add shortcut to Qslider widget'''
        self.setZshortcutUp = QShortcut(QKeySequence('Ctrl+PgUp'), self)
        self.setZshortcutUp.activated.connect(self.set_z_up)
        self.setZshortcutUp_fast = QShortcut(QKeySequence('Alt+PgUp'), self)
        self.setZshortcutUp_fast.activated.connect(self.set_z_up_fast)
        self.setZshortcutDn = QShortcut(QKeySequence('Ctrl+PgDown'), self)
        self.setZshortcutDn.activated.connect(self.set_z_down)
        self.setZshortcutDn_fast = QShortcut(QKeySequence('Alt+PgDown'), self)
        self.setZshortcutDn_fast.activated.connect(self.set_z_down_fast)
        self.setXYshortcutUp = QShortcut(QKeySequence('Ctrl+Up'), self)
        self.setXYshortcutUp.activated.connect(self.set_XY_up)
        self.setXYshortcutUp_fast = QShortcut(QKeySequence('Alt+Up'), self)
        self.setXYshortcutUp_fast.activated.connect(self.set_XY_up_fast)
        self.setXYshortcutDn = QShortcut(QKeySequence('Ctrl+Down'), self)
        self.setXYshortcutDn.activated.connect(self.set_XY_down)
        self.setXYshortcutDn_fast = QShortcut(QKeySequence('Alt+Down'), self)
        self.setXYshortcutDn_fast.activated.connect(self.set_XY_down_fast)

        '''add shortcut to QPushbutton'''
        self.sc_btn_z_up = QShortcut(QKeySequence('PgUp'), self)
        self.sc_btn_z_up.activated.connect(self.z_up)
        self.sc_btn_z_down = QShortcut(QKeySequence('PgDown'), self)
        self.sc_btn_z_down.activated.connect(self.z_down)
        self.sc_btn_up = QShortcut(QKeySequence('Up'), self)
        self.sc_btn_up.activated.connect(self.go_up)
        self.sc_btn_left = QShortcut(QKeySequence('Left'), self)
        self.sc_btn_left.activated.connect(self.go_left)
        self.sc_btn_right = QShortcut(QKeySequence('Right'), self)
        self.sc_btn_right.activated.connect(self.go_right)
        self.sc_btn_down = QShortcut(QKeySequence('Down'), self)
        self.sc_btn_down.activated.connect(self.go_down)


        '''show slider value in xy_step and z_step label'''
        self.slid_xy_speed.valueChanged.connect(lambda: self.xy_step.setText(str(self.slid_xy_speed.value()/10000)))
        self.slid_z_speed.valueChanged.connect(lambda: self.z_step.setText(str(self.slid_z_speed.value()/10000)))

        '''initial target line edit widget'''
        self.target_line_x = None
        self.target_line_y = None
        self.target_line_z = None

        '''build a canvas for plot'''
        self.sc = MplCanvas(self, width=250, height=250, dpi=100)
        # sc.axes.plot([0], [0])

        plot_layout =QtWidgets.QVBoxLayout(self.plot_canvas)
        plot_layout.setContentsMargins(0,0,0,0)
        plot_layout.addWidget(self.sc)

        self._plot_ref = None

        #----------------------------------------------------------------#
        self.initbackend()

    '''draw figure'''
    '''Enable real time position mapping function'''
    def update_plot(self, x, y):
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.sc.axes.plot(x, y, 'y', marker='o', markersize=5)
            self._plot_ref = plot_refs[0]
        else:
            self._plot_ref.set_xdata(x)
            self._plot_ref.set_ydata(y)
        self.sc.draw()

    '''start a sub thread to continuous read data'''
    def initbackend(self):
        self.backend = BackendThread()
        self.backend.start()

    def go_up(self):
        """emit a signal with one param of
            self.slid_xy_speed.value()/10000
        """
        step_value = self.slid_xy_speed.value()/10000
        self.up_signal.emit(step_value)
        print('go up')
            
    def go_left(self):
        step_value = self.slid_xy_speed.value() / 10000
        self.left_signal.emit(step_value)
        print('go left')
            
    def go_down(self):
        step_value = self.slid_xy_speed.value() / 10000
        self.down_signal.emit(step_value)
        print('go down')
            
    def go_right(self):
        step_value = self.slid_xy_speed.value() / 10000
        self.right_signal.emit(step_value)
        print('go right')
            
    def go_home(self):
        self.go_home_signal.emit()
        print('go home')
            
    def z_up(self):
        step_value = self.slid_z_speed.value() / 10000
        self.z_up_signal.emit(step_value)
        print('z_up')
            
    def z_down(self):
        step_value = self.slid_z_speed.value() / 10000
        self.z_down_signal.emit(step_value)
        print('z_down')
            
    def enable_key(self, status):
        print(f'keyboard enabled: {status}')
        self.setZshortcutUp.setEnabled(status)
        self.setZshortcutDn.setEnabled(status)
        self.setXYshortcutUp.setEnabled(status)
        self.setXYshortcutDn.setEnabled(status)
        self.setZshortcutDn_fast.setEnabled(status)
        self.setZshortcutUp_fast.setEnabled(status)
        self.setXYshortcutUp_fast.setEnabled(status)
        self.setXYshortcutDn_fast.setEnabled(status)
        self.sc_btn_z_up.setEnabled(status)
        self.sc_btn_z_down.setEnabled(status)
        self.sc_btn_up.setEnabled(status)
        self.sc_btn_down.setEnabled(status)
        self.sc_btn_right.setEnabled(status)
        self.sc_btn_left.setEnabled(status)

    def lock_key(self, status):
        print(f'motion locked: {status}')
        if status:
            key = not status
        else:
            key = not status
        self.btn_right.setEnabled(key)
        self.btn_left.setEnabled(key)
        self.btn_up.setEnabled(key)
        self.btn_down.setEnabled(key)
        self.btn_home.setEnabled(key)
        self.btn_go.setEnabled(key)
        self.btn_z_up.setEnabled(key)
        self.btn_z_down.setEnabled(key)


    '''Shortcut functions to Qslider widget'''
    def set_z_up(self):
        self.slid_z_speed.setValue(self.slid_z_speed.value() + 1)
        print('Ctrl + PgUp has been fired')

    def set_z_up_fast(self):
        self.slid_z_speed.setValue(self.slid_z_speed.value() + 100)
        print('Ctrl + PgUp has been fired')

    def set_z_down(self):
        self.slid_z_speed.setValue(self.slid_z_speed.value() - 1)
        print('Ctrl + PgDn has been fired')

    def set_z_down_fast(self):
        self.slid_z_speed.setValue(self.slid_z_speed.value() - 100)
        print('Ctrl + PgDn has been fired')

    def set_XY_up(self):
        self.slid_xy_speed.setValue(self.slid_xy_speed.value() + 1)
        print('Ctrl + Up has been fired')

    def set_XY_up_fast(self):
        self.slid_xy_speed.setValue(self.slid_xy_speed.value() + 100)

    def set_XY_down(self):
        self.slid_xy_speed.setValue(self.slid_xy_speed.value() - 1)
        print('Ctrl + Down has been fired')

    def set_XY_down_fast(self):
        self.slid_xy_speed.setValue(self.slid_xy_speed.value() - 100)
        print('Ctrl + Down has been fired')

    def add_list(self):
        print('add to list')
        self.target_line_x.setText(self.line_x.text())
        self.target_line_y.setText(self.line_y.text())
        self.target_line_z.setText(self.line_z.text())

    def del_list(self):
        print('del the list')
        self.target_line_x.setText(None)
        self.target_line_y.setText(None)
        self.target_line_z.setText(None)

    def go_target(self):
        print('go to the target')
        if self.target_line_x is None:
            self.target_line_x = self.line_x1
            self.target_line_x.setText(self.line_x.text())
        elif self.target_line_x.text() == '':
            self.target_line_x.setText(self.line_x.text())
        if self.target_line_y is None:
            self.target_line_y = self.line_y1
            self.target_line_y.setText(self.line_y.text())
        elif self.target_line_y.text() == '':
            self.target_line_y.setText(self.line_y.text())
        if self.target_line_z is None:
            self.target_line_z = self.line_z1
            self.target_line_z.setText(self.line_z.text())
        elif self.target_line_z.text() == '':
            self.target_line_z.setText(self.line_z.text())
        x_value = float(self.target_line_x.text())
        y_value = float(self.target_line_y.text())
        z_value = float(self.target_line_z.text())
        self.send_xyz_signal.emit(x_value, y_value, z_value)

    '''TODO Enable saving coordinates function'''
    def line1_selected(self):
        self.target_line_x = self.line_x1
        self.target_line_y = self.line_y1
        self.target_line_z = self.line_z1
        print('line1 selected')

    def line2_selected(self):
        self.target_line_x = self.line_x2
        self.target_line_y = self.line_y2
        self.target_line_z = self.line_z2
        print('line2 selected')

    def line3_selected(self):
        self.target_line_x = self.line_x3
        self.target_line_y = self.line_y3
        self.target_line_z = self.line_z3
        print('line3 selected')

    def line4_selected(self):
        self.target_line_x = self.line_x4
        self.target_line_y = self.line_y4
        self.target_line_z = self.line_z4
        print('line4 selected')

    def line5_selected(self):
        self.target_line_x = self.line_x5
        self.target_line_y = self.line_y5
        self.target_line_z = self.line_z5
        print('line5 selected')

    def line6_selected(self):
        self.target_line_x = self.line_x6
        self.target_line_y = self.line_y6
        self.target_line_z = self.line_z6
        print('line6 selected')

    def line7_selected(self):
        self.target_line_x = self.line_x7
        self.target_line_y = self.line_y7
        self.target_line_z = self.line_z7
        print('line7 selected')

    '''TODO add marked position in to graph with label'''

    def closeEvent(self, event):
        self.close_signal.emit()
        print('Program closed')
        print('event: {0}'.format(event))
        event.accept()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    my_window = Window()
    my_window.show()
    sys.exit(app.exec_())

