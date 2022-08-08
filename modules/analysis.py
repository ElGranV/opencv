DEFAULT_NUMBER_OF_AREAS = 7

def detect_area(video_capture, bbox, number_of_image_areas = DEFAULT_NUMBER_OF_AREAS):
    #Il faut absolument un nombre impair de zones dans l'image pour avoir une zone centrale
    if number_of_image_areas%2==0: number_of_image_areas+=1
    orientations = list(range(0,number_of_image_areas+1))
    width = video_capture.get(3)
    #height = video_capture.get(4)
    
    x,y,w,h = bbox
    box_center = (x+x+w)/2
    for i in range(number_of_image_areas):
        if (i*(width))/number_of_image_areas<= box_center<((i+1)*(width))/number_of_image_areas:
            return i

