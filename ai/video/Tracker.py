

class Tracker:

    margin_both_less_do_nothing = 10
    factor_to_trigger_movement = 10

    def __init__(self, width, height, car_movement):
        self.width = width
        self.height = height
        self.car_movement = car_movement

    def track(self, rectangle_up_left_position, rectangle_down_right_position):
        x1 = rectangle_up_left_position[0]
        y1 = rectangle_up_left_position[1]
        x2 = rectangle_down_right_position[0]
        y2 = rectangle_down_right_position[1]

        left_margin = x1
        right_margin = self.width - x2
        self.left_right_track(left_margin, right_margin)

        up_margin = y1
        down_margin = self.height - y2
        self.up_down_track(up_margin, down_margin)

    def left_right_track(self, left_margin, right_margin):

        if left_margin < Tracker.margin_both_less_do_nothing and right_margin < Tracker.margin_both_less_do_nothing:
            return

        factor_left_right = (left_margin + 1) / (right_margin + 1)
        if factor_left_right > Tracker.factor_to_trigger_movement:
            self.car_movement.move_right()
        elif 1/factor_left_right > Tracker.factor_to_trigger_movement:
            self.car_movement.move_left()

    def up_down_track(self, up_margin, down_margin):

        if up_margin < Tracker.margin_both_less_do_nothing and down_margin < Tracker.margin_both_less_do_nothing:
            return

        factor_up_down = (up_margin + 1) / (down_margin + 1)
        if factor_up_down > Tracker.factor_to_trigger_movement:
            self.car_movement.move_ahead()
        elif 1 / factor_up_down > Tracker.factor_to_trigger_movement:
            self.car_movement.move_ahead()

# FIXME use

