from utils.PropertiesReader import PropertiesReader
from clients.ImageStreamClient import ImageStreamClient
from clients.CommandsClient import CommandsClient
from clients.TextStreamClient import TextStreamClient
from clients.AudioStreamClient import AudioStreamClient
from textinterpreter.TextCommandInterpreter import TextCommandInterpreter
from complexcommands.ComplexCommand360 import ComplexCommand360
from complexcommands.ComplexCommandFollowMe import ComplexCommandFollowMe
from complexcommands.ComplexCommandRecord import ComplexCommandRecord
from complexcommands.ComplexCommandRoom import ComplexCommandRoom
from ai.video.ModelGenerator import ModelGenerator
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
    def launch(connect_to_video_stream=True, connect_to_audio_or_text_command_stream=True, car_speaks=True):
        app = wx.App()
        remote_control_ui = RemoteControlUI(connect_to_video_stream, connect_to_audio_or_text_command_stream, car_speaks)
        remote_control_ui.Show()
        app.MainLoop()

    def __init__(self, connect_to_video_stream, connect_to_audio_or_text_command_stream, car_speaks):
        super().__init__(parent=None, title='Camera Control Pad', size=(500, 500))
        panel = wx.Panel(self)

        self.properties_reader = PropertiesReader.get_instance()
        self.options_combo_led_commands = ['stop', 'alarm', 'police', 'rainbow', 'rainbow_flag', 'breathe', 'red',
                                           'fading_red']
        self.options_combo_rooms = self.properties_reader.room_list.split(",")

        self.create_button_pad(panel)
        self.create_led_command_selector(panel)
        self.create_room_selector(panel)
        self.create_look_button_pad(panel)
        self.create_train_button_pad(panel)

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        margin_button_pad_image = 30

        self.static_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.NullBitmap, pos=(left_margin, up_margin + 3 * button_height + margin_button_pad_image))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        commands_by_audio = True
        self.create_stream_clients(commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream)
        self.commands_client = CommandsClient.get_instance()
        self.text_command_interpreter = TextCommandInterpreter(car_speaks=car_speaks)

    def on_text_received(self, text):
        print(f"############################ {text}")
        self.text_command_interpreter.interpret(text)

    def create_stream_clients(self, commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream):

        host = self.properties_reader.host
        port_images_stream = int(self.properties_reader.port_images_stream)
        port_text_stream = int(self.properties_reader.port_text_stream)
        port_audio_stream = int(self.properties_reader.port_audio_stream)

        if connect_to_video_stream:
            image_stream_client = ImageStreamClient(host, port_images_stream, self.on_image_received)
            image_stream_client.start()

        if connect_to_audio_or_text_command_stream:
            if commands_by_audio:
                audio_stream_client = AudioStreamClient(host, port_audio_stream, self.on_text_received)
                audio_stream_client.start()
            else:
                text_stream_client = TextStreamClient(host, port_text_stream, self.on_text_received)
                text_stream_client.start()

    def on_image_received(self, image):

        ComplexCommand360.get_instance().last_image = image
        ComplexCommandFollowMe.get_instance().last_image = image
        ComplexCommandRecord.get_instance().set_last_image(image)
        ComplexCommandRoom.get_instance().last_image = image

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

    def create_look_button_pad(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        total_left_margin = left_margin + 3 * button_width + left_margin
        total_up_margin = 3 * up_margin + 2 * button_height

        RemoteControlUI.build_button_with_action(panel, 'look up', (total_left_margin, total_up_margin), self.on_press_look_up)
        RemoteControlUI.build_button_with_action(panel, 'look down', (total_left_margin, total_up_margin + button_height), self.on_press_look_down)
        RemoteControlUI.build_button_with_action(panel, 'look home', (total_left_margin, total_up_margin + 2 * button_height), self.on_press_look_home)

    def create_train_button_pad(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        total_left_margin = left_margin + 3 * button_width + left_margin
        total_up_margin = 4 * up_margin + 5 * button_height

        RemoteControlUI.build_button_with_action(panel, 'Train room', (total_left_margin, total_up_margin), self.on_press_train_room)

    def create_led_command_selector(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        pos = (left_margin + 3 * button_width + left_margin, up_margin)
        cb = wx.ComboBox(panel, -1, pos=pos, size=(button_width, button_height), choices=self.options_combo_led_commands, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_led_command_selection)

    def create_room_selector(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        total_up_margin = 2 * up_margin + button_height

        pos = (left_margin + 3 * button_width + left_margin, total_up_margin)
        cb = wx.ComboBox(panel, -1, pos=pos, size=(button_width, button_height), choices=self.options_combo_rooms, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_room_selection)

    def on_led_command_selection(self, event):

        idx_selection = event.GetSelection()
        mode = self.options_combo_led_commands[idx_selection]
        self.commands_client.led(mode)

    def on_room_selection(self, event):

        id_room = event.GetSelection()
        room = self.options_combo_rooms[id_room]
        ComplexCommand360.get_instance().selected_room = room
        ComplexCommand360.get_instance().id_selected_room = id_room

    @staticmethod
    def build_button_with_action(panel, label, pos, action):
        my_btn = wx.Button(panel, label=label, pos=pos, size=(RemoteControlUI.button_width, RemoteControlUI.button_height))
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

    def on_press_train_room(self, event):
        try:
            print("Train room!!")
            ModelGenerator.train_model_rooms()

        except:
            print("Problem with command Look up")
            traceback.print_exc()

    def OnClose(self, event):
        print("Closing stream")
        self.Destroy()
        os._exit(0)
