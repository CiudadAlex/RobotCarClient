from utils.PropertiesReader import PropertiesReader
from clients.CommandsClient import CommandsClient
from ai.video.ModelGenerator import ModelGenerator
from inforeception.CarInformationReceptor import CarInformationReceptor
from inforeception.SelectedDataReceptor import SelectedDataReceptor
from tools.RoomRouter import RoomRouter
from remotecontrolui.VerticalLayoutComposer import VerticalLayoutComposer
import wx
import traceback
import os
import time


class RemoteControlUI(wx.Frame):

    button_height = 50
    button_width = 100
    button_pad_left_margin = 30
    button_pad_up_margin = 30

    @staticmethod
    def launch():
        app = wx.App()
        remote_control_ui = RemoteControlUI()
        remote_control_ui.Show()
        app.MainLoop()

    def __init__(self):
        super().__init__(parent=None, title='Camera Control Pad', size=(600, 600))
        panel = wx.Panel(self)

        self.properties_reader = PropertiesReader.get_instance()
        self.options_combo_led_commands = ['stop', 'alarm', 'police', 'rainbow', 'rainbow_flag', 'breathe', 'red',
                                           'fading_red']

        self.options_combo_rooms = self.properties_reader.room_list.split(",")

        room_router = RoomRouter()
        self.options_combo_doors = room_router.get_list_all_adjacency()

        self.create_button_pad(panel)
        self.create_second_column(panel)

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        margin_button_pad_image = 30

        self.static_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.NullBitmap, pos=(left_margin, up_margin + 3 * button_height + margin_button_pad_image))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        CarInformationReceptor.get_instance().list_on_image_received.append(self.on_image_received)

        self.commands_client = CommandsClient.get_instance()

    def on_image_received(self, image):

        # image = self.resize_pil_image(image, 1)
        wx_image = wx.Image(image.size[0], image.size[1])
        wx_image.SetData(image.convert("RGB").tobytes())
        bitmap = wx.Bitmap(wx_image)
        self.static_bitmap.SetBitmap(bitmap)

    @staticmethod
    def resize_pil_image(pil_image, factor):

        width, height = pil_image.size
        new_size = (round(width * factor), round(height * factor))
        pil_image = pil_image.resize(new_size)
        return pil_image

    def create_button_pad(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        RemoteControlUI.build_button_with_action(panel, 'FORWARD', (left_margin + button_width, up_margin), self.on_press_forward)
        RemoteControlUI.build_button_with_action(panel, 'BACKWARD', (left_margin + button_width, up_margin + 2 * button_height), self.on_press_backward)
        RemoteControlUI.build_button_with_action(panel, 'LEFT', (left_margin, up_margin + button_height), self.on_press_left)
        RemoteControlUI.build_button_with_action(panel, 'RIGHT', (left_margin + 2 * button_width, up_margin + button_height), self.on_press_right)
        RemoteControlUI.build_button_with_action(panel, 'STOP', (left_margin + button_width, up_margin + button_height), self.on_press_home)

    def create_second_column(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width
        total_left_margin = left_margin + 3 * button_width + left_margin

        vertical_layout_composer = VerticalLayoutComposer(total_left_margin, up_margin, button_height,
                                                          button_width * 1.5, button_height / 2)

        self.create_led_command_selector(panel, vertical_layout_composer)
        self.create_room_selector(panel, vertical_layout_composer)
        self.create_door_selector(panel, vertical_layout_composer)
        self.create_look_button_pad(panel, vertical_layout_composer)
        self.create_train_button_pad(panel, vertical_layout_composer)

    def create_look_button_pad(self, panel, vertical_layout_composer):

        size = vertical_layout_composer.get_size()

        RemoteControlUI.build_button_with_action(panel, 'look up', vertical_layout_composer.get_next_position(),
                                                 self.on_press_look_up, size)
        RemoteControlUI.build_button_with_action(panel, 'look down', vertical_layout_composer.get_next_position(),
                                                 self.on_press_look_down, size)
        RemoteControlUI.build_button_with_action(panel, 'look home', vertical_layout_composer.get_next_position(),
                                                 self.on_press_look_home, size)

    def create_train_button_pad(self, panel, vertical_layout_composer):

        size = vertical_layout_composer.get_size()
        RemoteControlUI.build_button_with_action(panel, 'Train room', vertical_layout_composer.get_next_position(),
                                                 self.on_press_train_room, size)
        RemoteControlUI.build_button_with_action(panel, 'Train door', vertical_layout_composer.get_next_position(),
                                                 self.on_press_train_door, size)

    def create_led_command_selector(self, panel, vertical_layout_composer):

        pos = vertical_layout_composer.get_next_position()
        size = vertical_layout_composer.get_size()
        cb = wx.ComboBox(panel, -1, pos=pos, size=size, choices=self.options_combo_led_commands, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_led_command_selection)

    def create_room_selector(self, panel, vertical_layout_composer):

        pos = vertical_layout_composer.get_next_position()
        size = vertical_layout_composer.get_size()
        cb = wx.ComboBox(panel, -1, pos=pos, size=size, choices=self.options_combo_rooms, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_room_selection)

    def create_door_selector(self, panel, vertical_layout_composer):

        pos = vertical_layout_composer.get_next_position()
        size = vertical_layout_composer.get_size()
        cb = wx.ComboBox(panel, -1, pos=pos, size=size, choices=self.options_combo_doors, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_door_selection)

    def on_led_command_selection(self, event):

        idx_selection = event.GetSelection()
        mode = self.options_combo_led_commands[idx_selection]
        self.commands_client.led(mode)

    def on_room_selection(self, event):

        id_room = event.GetSelection()
        room = self.options_combo_rooms[id_room]

        SelectedDataReceptor.get_instance().set_room(id_room, room)

    def on_door_selection(self, event):

        id_door = event.GetSelection()
        door = self.options_combo_doors[id_door]

        SelectedDataReceptor.get_instance().set_door(id_door, door)

    @staticmethod
    def build_button_with_action(panel, label, pos, action, size=None):

        if size is None:
            size = (RemoteControlUI.button_width, RemoteControlUI.button_height)

        my_btn = wx.Button(panel, label=label, pos=pos, size=size)
        my_btn.Bind(wx.EVT_BUTTON, action)

    def on_press_forward(self, event):
        self.move_seconds("forward", self.commands_client.move_forward)

    def on_press_backward(self, event):
        self.move_seconds("backward", self.commands_client.move_backward)

    def on_press_left(self, event):
        self.move_seconds("left", self.commands_client.move_turn_left, secs=0.2)

    def on_press_right(self, event):
        self.move_seconds("right", self.commands_client.move_turn_right, secs=0.2)

    def move_seconds(self, label, action_move, secs=0.5):
        try:
            print(f"Move {label}!!")
            action_move()
            time.sleep(secs)
            self.commands_client.move("stop")

        except:
            print(f"Problem with command move {label}")
            traceback.print_exc()

    def on_press_home(self, event):
        try:
            print("STOP!!")
            self.commands_client.move("stop")

        except:
            print("Problem with command home")
            traceback.print_exc()

    def on_press_look_up(self, event):
        try:
            print("Look up!!")
            self.commands_client.look_up()

        except:
            print("Problem with command Look up")
            traceback.print_exc()

    def on_press_look_down(self, event):
        try:
            print("Look down!!")
            self.commands_client.look_down()

        except:
            print("Problem with command Look down")
            traceback.print_exc()

    def on_press_look_home(self, event):
        try:
            print("Look home!!")
            self.commands_client.look_home()

        except:
            print("Problem with command Look home")
            traceback.print_exc()

    @staticmethod
    def on_press_train_room(event):
        try:
            print("Train room!!")
            ModelGenerator.train_model_rooms()

        except:
            print("Problem with training rooms")
            traceback.print_exc()

    @staticmethod
    def on_press_train_door(event):
        try:
            print("Train door!!")
            ModelGenerator.train_model_doors()

        except:
            print("Problem with training doors")
            traceback.print_exc()

    def OnClose(self, event):
        print("Closing stream")
        self.Destroy()
        os._exit(0)
