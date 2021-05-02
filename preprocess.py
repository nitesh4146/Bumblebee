import cv2 

def preprocess(img):

    sky_crop = 530
    hood_crop = 870
    left_crop = 300
    right_crop = 1600
    
    processed_img = img[sky_crop:hood_crop, left_crop:right_crop]
    processed_img = rescale(processed_img)

    return processed_img


def rescale(img):
    scale_percent = 60 
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
