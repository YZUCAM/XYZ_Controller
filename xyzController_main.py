from xyzController import *
from Conex_xyz import Conex_xyz
import time
from datetime import datetime
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    '''instantiate windon and controller class'''
    controller_window = Window()
    x_stage = Conex_xyz('COM7')
    y_stage = Conex_xyz('COM8')
    z_stage = Conex_xyz('COM9')

    '''connect slot with signal in GUI window'''
    controller_window.up_signal.connect(lambda step_value: go_up(step_value))
    controller_window.down_signal.connect(lambda step_value: go_down(step_value))
    controller_window.left_signal.connect(lambda step_value: go_left(step_value))
    controller_window.right_signal.connect(lambda step_value: go_right(step_value))
    controller_window.z_up_signal.connect(lambda step_value: z_up(step_value))
    controller_window.z_down_signal.connect(lambda step_value: z_down(step_value))
    controller_window.go_home_signal.connect(lambda: go_home())
    controller_window.send_xyz_signal.connect(lambda x_value, y_value, z_value: go_target(x_value, y_value, z_value))
    # controller_window.send_xy_signal.connect(lambda x_value, y_value: go_target(x_value, y_value))
    controller_window.close_signal.connect(lambda: close_software())

    '''connect slot with signal in sub thread'''
    controller_window.backend.get_x.connect(lambda: get_x_pos())
    controller_window.backend.get_y.connect(lambda: get_y_pos())
    controller_window.backend.get_z.connect(lambda: get_z_pos())
    controller_window.backend.update_graph.connect(lambda: update_graph())

    '''get parameter from the GUI window, used this parameter to call function in Conex_xyz'''
    def go_up(step_value):
        y_pos = y_stage.get_current_position()
        if 0 < y_pos + step_value < 8:
            y_stage.move_absolute(y_pos + step_value)
            controller_window.chk_y.setChecked(False)
        else:
            controller_window.chk_y.setChecked(True)
            print('Hit y limit')
        print(step_value)

    def go_down(step_value):
        y_pos = y_stage.get_current_position()
        if 0 < y_pos - step_value < 8:
            y_stage.move_absolute(y_pos - step_value)
            controller_window.chk_y.setChecked(False)
        else:
            controller_window.chk_y.setChecked(True)
            print('Hit y limit')
        print(step_value)

    def go_left(step_value):
        x_pos = x_stage.get_current_position()
        if 0 < x_pos - step_value < 22:
            x_stage.move_absolute(x_pos - step_value)
            controller_window.chk_x.setChecked(False)
        else:
            controller_window.chk_x.setChecked(True)
            print('Hit x limit')
        print(step_value)

    def go_right(step_value):
        x_pos = x_stage.get_current_position()
        if 0 < x_pos + step_value < 22:
            x_stage.move_absolute(x_pos + step_value)
            controller_window.chk_x.setChecked(False)
        else:
            controller_window.chk_x.setChecked(True)
            print('Hit x limit')
        print(step_value)

    def z_up(step_value):
        z_pos = z_stage.get_current_position()
        if 0 < z_pos + step_value < 8.5:
            z_stage.move_absolute(z_pos + step_value)
            controller_window.chk_z.setChecked(False)
        else:
            controller_window.chk_z.setChecked(True)
            print('Hit z limit')
        print(step_value)

    def z_down(step_value):
        z_pos = z_stage.get_current_position()
        if 0 < z_pos - step_value < 8.5:
            z_stage.move_absolute(z_pos - step_value)
            controller_window.chk_z.setChecked(False)
        else:
            controller_window.chk_z.setChecked(True)
            print('Hit z limit')
        print(step_value)

    def go_home():
        x_stage.OR(1, '')
        y_stage.OR(1, '')
        z_stage.OR(1, '')

    def go_target(x_value, y_value, z_value):
        if 0 < x_value < 22 and 0 < y_value < 8 and 0 < z_value < 8.5:
            x_stage.move_absolute(x_value)
            y_stage.move_absolute(y_value)
            z_stage.move_absolute(z_value)
            controller_window.chk_x.setChecked(False)
            controller_window.chk_y.setChecked(False)
            controller_window.chk_z.setChecked(False)
            print('good to go!')
            print(x_value, y_value, z_value)
        else:
            if not (0 < x_value < 22):
                controller_window.chk_x.setChecked(True)
                print(x_value)
            else:
                controller_window.chk_x.setChecked(False)
                print(x_value)
            if not (0 < y_value < 20):
                controller_window.chk_y.setChecked(True)
                print(y_value)
            else:
                controller_window.chk_y.setChecked(False)
                print(y_value)
            if not (0 < z_value < 8.5):
                controller_window.chk_z.setChecked(True)
                print(z_value)
            else:
                controller_window.chk_z.setChecked(False)
                print(z_value)

    # def test_xy_move(x, y):
    #     controller_window.line_x.setText(str(x))
    #     controller_window.line_y.setText(str(y))

    def get_x_pos():
        x_pos = x_stage.get_current_position()
        # i = 0
        # controller_window.line_x.setText(str(i))
        controller_window.line_x.setText(str(x_pos))

    def get_y_pos():
        # i = 0
        # controller_window.line_y.setText(str(i))
        y_pos = y_stage.get_current_position()
        controller_window.line_y.setText(str(y_pos))

    def get_z_pos():
        # now = datetime.now()
        # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # i = 19
        # controller_window.line_z.setText(str(dt_string))
        z_pos = z_stage.get_current_position()
        controller_window.line_z.setText(str(z_pos))

    def update_graph():
        controller_window.update_plot(float(controller_window.line_x.text()), float(controller_window.line_y.text()))

    def close_software():
        print('Unregister device')
        controller_window.backend.beckend_flg = False
        x_stage.CloseInstrument()
        y_stage.CloseInstrument()
        z_stage.CloseInstrument()
        # del x_stage
        # del y_stage
        # del z_stage

    controller_window.show()
    sys.exit(app.exec_())
