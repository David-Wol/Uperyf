import cv2
import numpy as np
from tkinter import *

def run_gui():    
    root = Tk()  
    root.geometry("400x300") 
    
    v1 = DoubleVar() # saturation
    v2 = BooleanVar() # recording checkbox
    
    s1 = Scale( root, variable = v1, 
            from_ = 0, to = 255, 
            orient = HORIZONTAL)   
    
    
    l3 = Label(root, text = "Saturation")
    
    b1 = Button(root, text ="Start camera",   # start button
                command = root.destroy, 
                bg = "green")   
    
    b2 = Checkbutton(root, text = "Start recording", variable=v2)
    
    l1 = Label(root)
  
  
    s1.pack(anchor = CENTER) 
    l3.pack()
    b2.pack(anchor = CENTER)
    b1.pack(anchor = CENTER)
    l1.pack() 
    
    root.mainloop()
    
    return v1.get(), v2.get()

def main():
        
    rec = ''
    img_counter = 0
    
    saturation, is_recording = run_gui()
    cam.set(cv2.CAP_PROP_SATURATION, saturation)
    
    if is_recording:
        rec = cv2.VideoWriter('recording.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15.0, (640,480))
    
    while True:
        ret, frame = cam.read()
        
        if not ret:
            print("Failed to grab frame.")
            break
        
        cv2.imshow("Camera", frame)
        
        key = cv2.waitKey(1)
        if key%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif key%256 == 32:
            # SPACE pressed
            img_name = f"opencv_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} saved")
            img_counter += 1
        elif key%256 == 112:
            # pause - press P
            while True:
                key = cv2.waitKey(1)
                if key%256 == 113:
                # resume - press R
                    break
    
    if rec:
        rec.write(frame.astype('uint8'))
        rec.release()
    
    cam.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main()