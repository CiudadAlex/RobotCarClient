from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 connect_to_video_stream=online,
                 connect_to_audio_stream=online,
                 connect_to_text_stream=online)

    RemoteControlUI.launch()


# FIXME test: generate corpus with val and test images
# FIXME Room recognizer: redo training with higher look

# FIXME Edge recognition to guide.
# FIXME Wall follower

# FIXME ComplexCommandGoToRoom (Door recognition model)


# FIXME revise espeak (makes 360 hang)

'''
from tools.EdgeDetector import EdgeDetector

image_path = 'C:/Alex/Dev/data_corpus/VideoCamera/room_dataset_v0/train/images/kitchen_68fb62e4-e427-441a-a814-888d35da6887.png.png'


edges = EdgeDetector.get_horizontal_edges(image_path, show=True)
print(edges)

'''