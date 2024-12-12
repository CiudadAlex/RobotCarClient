import imageio
import numpy as np


class ImageUtils:

    @staticmethod
    def generate_gif(path_file, list_images):
        gif = []
        for image in list_images:
            gif.append(image)

        gif[0].save(path_file, save_all=True, optimize=False, append_images=gif[1:], duration=1000, loop=0)

    @staticmethod
    def generate_mp4(path_file, list_images):

        writer = imageio.get_writer(path_file, format='mp4', mode='I', fps=20)

        for image in list_images:
            writer.append_data(np.asarray(image))

        writer.close()
