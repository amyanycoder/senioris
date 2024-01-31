canny(img):
    edges = cv2.Canny(img, threshold1 = 100, threshold2 = 200)
    return edges