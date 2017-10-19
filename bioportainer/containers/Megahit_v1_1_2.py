from bioportainer.containers.Megahit_v1_1_1 import Megahit_v1_1_1


class Megahit_v1_1_2(Megahit_v1_1_1):  # ony bug fixes no parameter change in new version
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)

