from utils.PropertiesReader import PropertiesReader
from clients.ImageStreamClient import ImageStreamClient
from clients.CommandsClient import CommandsClient
from clients.TextStreamClient import TextStreamClient
from clients.AudioStreamClient import AudioStreamClient
from textinterpreter.TextCommandInterpreter import TextCommandInterpreter
import wx
import traceback
import os


class RemoteControlUI(wx.Frame):

    button_height = 50
    button_width = 100
    button_pad_left_margin = 30
    button_pad_up_margin = 30

    @staticmethod
    def launch(connect_to_video_stream=True, connect_to_audio_or_text_command_stream=True):
        app = wx.App()
        remote_control_ui = RemoteControlUI(connect_to_video_stream, connect_to_audio_or_text_command_stream)
        remote_control_ui.Show()
        app.MainLoop()

    def __init__(self, connect_to_video_stream, connect_to_audio_or_text_command_stream):
        super().__init__(parent=None, title='Camera Control Pad', size=(500, 500))
        panel = wx.Panel(self)

        self.options_combo_led_commands = ['stop', 'alarm', 'police', 'rainbow', 'rainbow_flag', 'breathe']

        self.create_button_pad(panel)
        self.create_led_command_selector(panel)

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        margin_button_pad_image = 30

        self.static_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.NullBitmap, pos=(left_margin, up_margin + 3 * button_height + margin_button_pad_image))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        commands_by_audio = True
        self.create_stream_clients(commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream)
        self.commands_client = CommandsClient.get_instance()
        self.text_command_interpreter = TextCommandInterpreter()

    def on_text_received(self, text):
        print(f"############################ {text}")
        self.text_command_interpreter.interpret(text)

    def create_stream_clients(self, commands_by_audio, connect_to_video_stream, connect_to_audio_or_text_command_stream):

        properties_reader = PropertiesReader('config.properties')
        host = properties_reader.host
        port_images_stream = int(properties_reader.port_images_stream)
        port_text_stream = int(properties_reader.port_text_stream)
        port_audio_stream = int(properties_reader.port_audio_stream)

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

        RemoteControlUI.build_button_with_action(panel, 'UP', (left_margin + button_width, up_margin), self.on_press_up)
        RemoteControlUI.build_button_with_action(panel, 'DOWN', (left_margin + button_width, up_margin + 2 * button_height), self.on_press_down)
        RemoteControlUI.build_button_with_action(panel, 'LEFT', (left_margin, up_margin + button_height), self.on_press_left)
        RemoteControlUI.build_button_with_action(panel, 'RIGHT', (left_margin + 2 * button_width, up_margin + button_height), self.on_press_right)
        RemoteControlUI.build_button_with_action(panel, 'HOME', (left_margin + button_width, up_margin + button_height), self.on_press_home)

    def create_led_command_selector(self, panel):

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        button_width = RemoteControlUI.button_width

        pos = (left_margin + 3 * button_width + left_margin, up_margin)
        cb = wx.ComboBox(panel, -1, pos=pos, size=(button_width, button_height), choices=self.options_combo_led_commands, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.on_led_command_selection)

    def on_led_command_selection(self, event):

        idx_selection = event.GetSelection()
        mode = self.options_combo_led_commands[idx_selection]
        self.commands_client.led(mode)

    @staticmethod
    def build_button_with_action(panel, label, pos, action):
        my_btn = wx.Button(panel, label=label, pos=pos, size=(RemoteControlUI.button_width, RemoteControlUI.button_height))
        my_btn.Bind(wx.EVT_BUTTON, action)

    def on_press_up(self, event):
        try:
            print("UP!!")

        except:
            print("Problem with command up")
            traceback.print_exc()

    def on_press_down(self, event):
        try:
            print("DOWN!!")

        except:
            print("Problem with command down")
            traceback.print_exc()

    def on_press_left(self, event):
        try:
            print("LEFT!!")

        except:
            print("Problem with command left")
            traceback.print_exc()

    def on_press_right(self, event):
        try:
            print("RIGHT!!")

        except:
            print("Problem with command right")
            traceback.print_exc()

    def on_press_home(self, event):
        try:
            print("HOME!!")

        except:
            print("Problem with command home")
            traceback.print_exc()

    def OnClose(self, event):
        print("Closing stream")
        self.Destroy()
        os._exit(0)
