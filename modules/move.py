import modules.arduino_io as arduino_io
from modules.move import detect_area


def send_area_information_to_arduino(video_capture, bbox, old_area):
    area = detect_area(video_capture, bbox)
    if area != old_area: print(arduino_io.write_read(area))
    return area