import configparser


class PropertiesReader:

    instance = None

    @staticmethod
    def get_instance():

        if PropertiesReader.instance is None:
            PropertiesReader.instance = PropertiesReader('config.properties')

        return PropertiesReader.instance

    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        section = 'DEFAULT'

        self.host = config[section]['host']
        self.port_images_stream = config[section]['port_images_stream']
        self.port_text_stream = config[section]['port_text_stream']
        self.port_audio_stream = config[section]['port_audio_stream']
        self.port_commands_rest_api = config[section]['port_commands_rest_api']
        self.vlc_executable_path = config[section]['vlc_executable_path']
        self.music_dir_path = config[section]['music_dir_path']
        self.model_llama_ccp_path = config[section]['model_llama_ccp_path']
        self.room_list = config[section]['room_list']
        self.room_adjacency = config[section]['room_adjacency']
