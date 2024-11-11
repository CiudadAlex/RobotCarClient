from utils.FileUtils import FileUtils
from utils.MatchUtils import MatchUtils
import subprocess


class MusicPlayer:

    def __init__(self, root_dir):
        self.map_file_name_path = FileUtils.get_map_file_name_2_path(root_dir, MusicPlayer.preprocess_name, MusicPlayer.preprocess_path)
        self.process = None

    @staticmethod
    def preprocess_name(name):
        return name.lower().replace(".mp3", "").replace(".wav", "").replace("_", " ").replace("-", " ")

    @staticmethod
    def preprocess_path(path):
        return path.replace("/", "\\")

    def stop(self):

        if self.process is not None:
            self.process.terminate()

        self.process = None

    def process_text(self, text):

        self.stop()

        most_similar_key = MatchUtils.get_most_matching_text_item(text.lower(), self.map_file_name_path.keys())
        path_music_file = self.map_file_name_path[most_similar_key]

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + path_music_file)
        self.process = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe", "--started-from-file", path_music_file])

