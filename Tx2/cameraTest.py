import cv2

cap = cv2.VideoCapture(2)
if not cap.isOpened():
   print("camera open failed")
   raise RuntimeError
ret, img = cap.read()
if not ret:
   print("Can't read camera")
   raise RuntimeError

# crop_img = img[120:-120,160:-160]
# scaleX = 2
# scaleY = 2
# scaleUp_img = cv2.resize(crop_img, None, fx=scaleX, fy=scaleY, interpolation = cv2.INTER_CUBIC)

img_captured = cv2.imwrite('images/img_captured.jpg', img, params=[cv2.IMWRITE_JPEG_QUALITY,100])