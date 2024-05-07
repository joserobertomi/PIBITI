from picamera2 import Picamera2

def init_camera(cam_size):
    # Captura a imagem da camera e salva em um arquivo tipo jpg
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (cam_size)}, lores={"size": (cam_size)}, display="lores")
    picam2.configure(camera_config)
    return picam2


def take_photo(picam2):
    # Captura a imagem da camera e salva em um arquivo tipo jpg
    picam2.start() 
    path = "/home/perry/project/images/original-frame.jpg"
    picam2.capture_file(path)
    return path


