import cv2
import numpy as np
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

### Functions

def imshow(title = "Image", image = None, size = 10):
    w, h = image.shape[0], image.shape[1]
    aspect_ratio = w/h
    plt.figure(figsize=(size * aspect_ratio,size))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

def open_image():
    global path, original_image, canvas, img_label
    path = filedialog.askopenfilename()
    if path:
        original_image = Image.open(path)
        update_image_display()

def update_image_display():
    if original_image:
        render_image = ImageTk.PhotoImage(original_image)
        canvas.itemconfig(img_label, image=render_image)
        canvas.image = render_image
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

def scan_qr_code():
    if path:
        # Detect and decode the qrcode
        image = cv2.imread(path)
        codes = decode(image)

        # Loop over the detected barcodes
        for bc in codes:
            # Get the rectangle coordinates for our text placement
            (x, y, w, h) = bc.rect
            print(bc.polygon)
            pt1, pt2, pt3, pt4 = bc.polygon

            # Draw a bounding box over our detected QR code
            pts = np.array([[pt1.x, pt1.y], [pt2.x, pt2.y], [pt3.x, pt3.y], [pt4.x, pt4.y]], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 0, 255), 3)

            # Extract the string info data and the type from our object
            barcode_text = bc.data.decode()
            barcode_type = bc.type

            # Show our QR Code both in console and GUI
            text = "{} ({})".format(barcode_text, barcode_type)
            cv2.putText(image, barcode_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(image, barcode_type, (x + w, y + h - 15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            print("QR Code revealed: {}".format(text))

            output_text.delete(1.0, tk.END)
            for res in codes:
                output_text.insert(tk.END, f"{res.data.decode('utf-8')}\n")

        # Display our output
        imshow("QR Code", image, size=12)

def scan_barcode():
    if path:
        # Detect and decode the barcode
        image = cv2.imread(path)
        barcodes = decode(image)

        # Loop over the detected barcodes
        for bc in barcodes:
            # Get the rectangle coordinates for our text placement
            (x, y, w, h) = bc.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

            # Extract the string info data and the type from our object
            barcode_text = bc.data.decode()
            barcode_type = bc.type

            # Show our barcode both in console and GUI
            text = "{} ({})".format(barcode_text, barcode_type)
            cv2.putText(image, barcode_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(image, barcode_type, (x + w, y + h - 15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            print("Barcode revealed: {}".format(barcode_text))
            print("Barcode revealed: {}".format(barcode_text))

            output_text.delete(1.0, tk.END)
            for res in barcodes:
                output_text.insert(tk.END, f"{res.data.decode('utf-8')}\n")

        # Display our output
        imshow("Barcode", image, size=16)


### GUI

# Create the main window
root = tk.Tk()
root.title("QR and Barcode Scanner")

# Create a frame for the canvas and scrollbar
frame_canvas = tk.Frame(root)
frame_canvas.pack(fill='both', expand=True)

# Create a canvas with a vertical scrollbar
canvas = tk.Canvas(frame_canvas)
scroll_y = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)

img_label = canvas.create_image(0, 0, anchor='nw')
canvas.pack(side='left', fill='both', expand=True)
scroll_y.pack(side='right', fill='y')

# Create a frame for buttons and text output
frame_controls = tk.Frame(root)
frame_controls.pack(fill='x')

btn_open = tk.Button(frame_controls, text="Open Image", command=open_image)
btn_open.pack(side='top', fill='x')

btn_scan_qr = tk.Button(frame_controls, text="Scan QR Code", command=scan_qr_code)
btn_scan_qr.pack(side='top', fill='x')

btn_scan_barcode = tk.Button(frame_controls, text="Scan Barcode", command=scan_barcode)
btn_scan_barcode.pack(side='top', fill='x')

# Add a text widget to display results
output_text = tk.Text(frame_controls, height=10)
output_text.pack(side='top', fill='x')

# Run the application
root.mainloop()



