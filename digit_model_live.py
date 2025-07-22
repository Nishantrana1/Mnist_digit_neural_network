import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf

# Load your model
model = tf.keras.models.load_model("digit_model.h5") 

# Create a drawing canvas
class DrawApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=280, height=280, bg='black')
        self.canvas.pack()
        self.image = Image.new("L", (280, 280), color=0)
        self.draw = ImageDraw.Draw(self.image)
        
        self.canvas.bind("<B1-Motion>", self.paint)

        btn_predict = tk.Button(master, text="Predict", command=self.predict_digit)
        btn_predict.pack()

        btn_clear = tk.Button(master, text="Clear", command=self.clear_canvas)
        btn_clear.pack()

    def paint(self, event):
        x, y = event.x, event.y
        r = 20
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='white', outline='white')
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill=255)

    def predict_digit(self):
        img_resized = self.image.resize((28, 28))
        img_array = np.array(img_resized)
        img_array = np.where(img_array > 128, 255, 0).astype(np.uint8)  # Optional threshold
        img_array = img_array / 255.0
        img_array = img_array.reshape(1, 28, 28, 1)  # adjust if your model input is different

        prediction = model.predict(img_array)
        predicted_digit = np.argmax(prediction)
        print(f"Predicted Digit: {predicted_digit}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), color=0)
        self.draw = ImageDraw.Draw(self.image)

# Run the app
root = tk.Tk()
root.title("Draw a Digit")
app = DrawApp(root)
root.mainloop()
