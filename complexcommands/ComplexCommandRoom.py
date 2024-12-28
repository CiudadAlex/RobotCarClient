

class ComplexCommandRoom:

    instance = None

    @staticmethod
    def get_instance():
        if ComplexCommandRoom.instance is None:
            ComplexCommandRoom.instance = ComplexCommandRoom()

        return ComplexCommandRoom.instance

    # .models/room_s_20024_12_28.pt
