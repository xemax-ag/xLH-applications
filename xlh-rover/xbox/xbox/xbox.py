from xbox360controller import Xbox360Controller
import time

class Xbox:
    def __init__(self):
        self.rAxLeftX = 0.0
        self.rAxLeftY = 0.0
        self.rAxRightX = 0.0
        self.rAxRightY = 0.0
        self.rTriggerLeft = 0.0
        self.rTriggerRight = 0.0

        self.bBtnA = False
        self.bBtnB = False
        self.bBtnX = False
        self.bBtnY = False
        self.bBtnBack = False
        self.bBtnStart = False
        self.bBtnThumbLeft = False
        self.bBtnThumbRight = False
        self.bBtnTriggerLeft = False
        self.bBtnTriggerRight = False
        self.bBtnDpadLeft = False
        self.bBtnDpadRight = False
        self.bBtnDpadUp = False
        self.bBtnDpadDown = False


        self.controller: Xbox360Controller | None = None
        self.connect_controller()

    def on_button_pressed(self, button):
        # print('Button {0} was pressed'.format(button.name))
        try:
            if self.controller is not None:
                if button.name == 'button_a':
                    self.bBtnA = True
                elif button.name == 'button_b':
                    self.bBtnB = True
                elif button.name == 'button_x':
                    self.bBtnX = True
                elif button.name == 'button_y':
                    self.bBtnY = True
                elif button.name == 'button_thumb_l':
                    self.bBtnThumbLeft = True
                elif button.name == 'button_thumb_r':
                    self.bBtnThumbRight = True
                elif button.name == 'button_trigger_l':
                    self.bBtnTriggerLeft = True
                elif button.name == 'button_trigger_r':
                    self.bBtnTriggerRight = True
                elif button.name == 'button_select':
                    self.bBtnBack = True
                elif button.name == 'button_start':
                    self.bBtnStart = True
                elif button.name == 'button_dpad_left':
                    self.bBtnDpadLeft = True
                elif button.name == 'button_dpad_right':
                    self.bBtnDpadRight = True
                elif button.name == 'button_dpad_up':
                    self.bBtnDpadUp = True
                elif button.name == 'button_dpad_down':
                    self.bBtnDpadDown = True
        except Exception as e:
            self.close_controller()

    def on_button_released(self, button):
        # print('Button {0} was released'.format(button.name))
        try:
            if self.controller is not None:
                if button.name == 'button_a':
                    self.bBtnA = False
                elif button.name == 'button_b':
                    self.bBtnB = False
                elif button.name == 'button_x':
                    self.bBtnX = False
                elif button.name == 'button_y':
                    self.bBtnY = False
                elif button.name == 'button_thumb_l':
                    self.bBtnThumbLeft = False
                elif button.name == 'button_thumb_r':
                    self.bBtnThumbRight = False
                elif button.name == 'button_trigger_l':
                    self.bBtnTriggerLeft = False
                elif button.name == 'button_trigger_r':
                    self.bBtnTriggerRight = False
                elif button.name == 'button_select':
                    self.bBtnBack = False
                elif button.name == 'button_start':
                    self.bBtnStart = False
                elif button.name == 'button_dpad_left':
                    self.bBtnDpadLeft = False
                elif button.name == 'button_dpad_right':
                    self.bBtnDpadRight = False
                elif button.name == 'button_dpad_up':
                    self.bBtnDpadUp = False
                elif button.name == 'button_dpad_down':
                    self.bBtnDpadDown = False
        except Exception as e:
            self.close_controller()

    def on_axis_moved(self, axis):
        # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
        try:
            if self.controller is not None:
                if axis.name == 'axis_l':
                    self.rAxLeftX = axis.x
                    self.rAxLeftY = axis.y
                elif axis.name == 'axis_r':
                    self.rAxRightX = axis.x
                    self.rAxRightY = axis.y
        except Exception as e:
            self.close_controller()

    def on_trigger_moved(self, trigger):
        # print(f'Trigger {trigger.name} moved to {trigger.value}')
        try:
            if self.controller is not None:
                if trigger.name == 'trigger_l':
                    self.rAxLeftX = trigger.value
                elif trigger.name == 'trigger_r':
                    self.rAxRightX = trigger.value
        except Exception as e:
            self.close_controller()

    def rumble(self):
        try:
            if self.controller is not None:
                # if self.controller.has_rumble():
                self.controller.set_rumble(1.0, 1.0, 50)
        except Exception as e:
            self.close_controller()

    def update(self):
        try:
            if self.controller is not None:
                self.controller.button_a.when_pressed = self.on_button_pressed
                self.controller.button_b.when_pressed = self.on_button_pressed
                self.controller.button_x.when_pressed = self.on_button_pressed
                self.controller.button_y.when_pressed = self.on_button_pressed
                self.controller.button_thumb_l.when_pressed = self.on_button_pressed
                self.controller.button_thumb_r.when_pressed = self.on_button_pressed
                self.controller.button_trigger_l.when_pressed = self.on_button_pressed
                self.controller.button_trigger_r.when_pressed = self.on_button_pressed
                self.controller.button_select.when_pressed = self.on_button_pressed
                self.controller.button_mode.when_pressed = self.on_button_pressed
                self.controller.button_start.when_pressed = self.on_button_pressed
                self.controller.button_dpad_left.when_pressed = self.on_button_pressed
                self.controller.button_dpad_right.when_pressed = self.on_button_pressed
                self.controller.button_dpad_up.when_pressed = self.on_button_pressed
                self.controller.button_dpad_down.when_pressed = self.on_button_pressed

                self.controller.button_a.when_released = self.on_button_released
                self.controller.button_b.when_released = self.on_button_released
                self.controller.button_x.when_released = self.on_button_released
                self.controller.button_y.when_released = self.on_button_released
                self.controller.button_thumb_l.when_released = self.on_button_released
                self.controller.button_thumb_r.when_released = self.on_button_released
                self.controller.button_trigger_l.when_released = self.on_button_released
                self.controller.button_trigger_r.when_released = self.on_button_released
                self.controller.button_select.when_released = self.on_button_released
                self.controller.button_mode.when_released = self.on_button_released
                self.controller.button_start.when_released = self.on_button_released
                self.controller.button_dpad_left.when_released = self.on_button_released
                self.controller.button_dpad_right.when_released = self.on_button_released
                self.controller.button_dpad_up.when_released = self.on_button_released
                self.controller.button_dpad_down.when_released = self.on_button_released

                self.controller.axis_l.when_moved = self.on_axis_moved
                self.controller.axis_r.when_moved = self.on_axis_moved
                self.controller.trigger_l.when_moved = self.on_trigger_moved
                self.controller.trigger_r.when_moved = self.on_trigger_moved
            else:
                self.connect_controller()
        except Exception as e:
            self.connect_controller()

    def reset(self):
        self.rAxLeftX = 0.0
        self.rAxLeftY = 0.0
        self.rAxRightX = 0.0
        self.rAxRightY = 0.0
        self.rTriggerLeft = 0.0
        self.rTriggerRight = 0.0

        self.bBtnA = False
        self.bBtnB = False
        self.bBtnX = False
        self.bBtnY = False
        self.bBtnBack = False
        self.bBtnStart = False
        self.bBtnThumbLeft = False
        self.bBtnThumbRight = False
        self.bBtnTriggerLeft = False
        self.bBtnTriggerRight = False
        self.bBtnDpadLeft = False
        self.bBtnDpadRight = False
        self.bBtnDpadUp = False
        self.bBtnDpadDown = False

    def connect_controller(self):
        self.reset()
        try:
            self.controller: Xbox360Controller | None = Xbox360Controller(0, axis_threshold=0.01)
        except Exception as e:
            self.controller = None

    def close_controller(self):
        try:
            self.controller.close()
            self.controller = None
        except Exception as e:
            self.controller = None

    def __str__(self):
        str_out = f'xbox | '
        if self.controller is not None:
            str_out += f'btnA = {self.bBtnA} | '
            str_out += f'btnA = {self.bBtnA} | '
            str_out += f'btnB = {self.bBtnB } | '
            str_out += f'rAxLeftX = {self.rAxLeftX:0.2f} | '
        else:
            str_out += f'None'
        return str_out


if __name__ == '__main__':
    xbox = Xbox()
    while True:
        xbox.update()
        # print(xbox)
        time.sleep(0.1)



