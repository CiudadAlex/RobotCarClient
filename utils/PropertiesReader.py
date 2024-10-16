import configparser


class PropertiesReader:

    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        section = 'DEFAULT'

        self.host = config[section]['host']
        self.port_images_stream = config[section]['port_images_stream']
