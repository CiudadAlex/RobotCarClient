import wx
import traceback
import time


class RemoteControlUI(wx.Frame):

    button_height = 50
    button_width = 100
    button_pad_left_margin = 30
    button_pad_up_margin = 30

    @staticmethod
    def launch():
        app = wx.App()
        RemoteControlUI()
        app.MainLoop()

    def __init__(self):
        super().__init__(parent=None, title='Camera Control Pad', size=(400, 500))
        panel = wx.Panel(self)

        self.create_button_pad(panel)

        # To allow the client to connect correctly
        time.sleep(1)

        left_margin = RemoteControlUI.button_pad_left_margin
        up_margin = RemoteControlUI.button_pad_up_margin
        button_height = RemoteControlUI.button_height
        margin_button_pad_image = 30

        self.static_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.NullBitmap, pos=(left_margin, up_margin + 3 * button_height + margin_button_pad_image))
        self.update_static_bitmap()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show()

    def update_static_bitmap(self):
        pil_image = self.get_pil_image_from_camera()
        wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
        wx_image.SetData(pil_image.convert("RGB").tobytes())
        bitmap = wx.Bitmap(wx_image)
        self.static_bitmap.SetBitmap(bitmap)

    def get_pil_image_from_camera(self):

        # FIXME use ImageStreamClient

        pil_image = self.rtsp_client.get_pil_image()
        width, height = pil_image.size
        new_size = (round(width / 8), round(height / 8))
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

    @staticmethod
    def build_button_with_action(panel, label, pos, action):
        my_btn = wx.Button(panel, label=label, pos=pos, size=(RemoteControlUI.button_width, RemoteControlUI.button_height))
        my_btn.Bind(wx.EVT_BUTTON, action)

    def on_press_up(self, event):
        try:
            print("UP!!")
            time.sleep(2)
            self.update_static_bitmap()
        except:
            print("Problem with command up")
            traceback.print_exc()

    def on_press_down(self, event):
        try:
            print("DOWN!!")
            time.sleep(2)
            self.update_static_bitmap()
        except:
            print("Problem with command down")
            traceback.print_exc()

    def on_press_left(self, event):
        try:
            print("LEFT!!")
            time.sleep(2)
            self.update_static_bitmap()
        except:
            print("Problem with command left")
            traceback.print_exc()

    def on_press_right(self, event):
        try:
            print("RIGHT!!")
            time.sleep(2)
            self.update_static_bitmap()
        except:
            print("Problem with command right")
            traceback.print_exc()

    def on_press_home(self, event):
        try:
            print("HOME!!")
            time.sleep(5)
            self.update_static_bitmap()
        except:
            print("Problem with command home")
            traceback.print_exc()

    def OnClose(self, event):
        print("Closing stream")
        print("CLOSE!!")
        self.Destroy()
