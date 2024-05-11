import cv2
import numpy as np
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode
from PIL import Image

### imshow function
def imshow(title = "Image", image = None, size = 10):
    w, h = image.shape[0], image.shape[1]
    aspect_ratio = w/h
    plt.figure(figsize=(size * aspect_ratio,size))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

### Decoding QR Codes

img = Image.open('qrcode.png')
result = decode(img)
for i in result:
    print(i.data.decode("utf-8"))

### Detecting QR Codes

image = cv2.imread("qrcode.png")

# Detect and decode the qrcode
codes = decode(image)

# Loop over the detected barcodes
for bc in codes:
  # Get the rectangle coordinates for our text placement
  (x, y, w, h) = bc.rect
  print(bc.polygon)
  pt1,pt2,pt3,pt4 = bc.polygon

  # Draw a bounding box over our detected QR code
  pts = np.array( [[pt1.x,pt1.y], [pt2.x,pt2.y], [pt3.x,pt3.y], [pt4.x,pt4.y]], np.int32)
  pts = pts.reshape((-1,1,2))
  cv2.polylines(image, [pts], True, (0,0,255), 3)

  # Extract the string info data and the type from our object
  barcode_text = bc.data.decode()
  barcode_type = bc.type

  # Show our QR Code
  text = "{} ({})".format(barcode_text, barcode_type)
  cv2.putText(image, barcode_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
  cv2.putText(image, barcode_type, (x+w, y+h - 15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
  print("QR Code revealed: {}".format(text))

# Display our output
imshow("QR Scanner", image, size = 12)



### Detecting Barcodes

image = cv2.imread("1024px-ISBN.jpg")

# Detect and decode the barcode
barcodes = decode(image)

# Loop over the detected barcodes
for bc in barcodes:
  # Get the rectangle coordinates for our text placement
  (x, y, w, h) = bc.rect
  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

  # Extract the string info data and the type from our object
  barcode_text = bc.data.decode()
  barcode_type = bc.type

  # Show our barcode
  text = "{} ({})".format(barcode_text, barcode_type)
  cv2.putText(image, barcode_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
  cv2.putText(image, barcode_type, (x+w, y+h - 15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
  print("Barcode revealed: {}".format(barcode_text))
  print("Barcode revealed: {}".format(barcode_text))

# Display our output
imshow("QR Scanner", image, size = 16)




