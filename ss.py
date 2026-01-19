import numpy as np
import cv2

img = np.zeros((240, 360, 3), dtype=np.uint8)

cv2.rectangle(img, (20, 20), (340, 220), (0, 255, 0), 2)
cv2.putText(
    img,
    "OpenCV + NumPy OK",
    (40, 130),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

cv2.imshow("Interop Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
