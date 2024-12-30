import cv2
import serial
import time

# Set up the serial connection to the Arduino
arduino = serial.Serial('COM12', 9600)  # Update 'COM12' with your Arduino's port

# Load the pre-trained classifiers for human detection
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load YOLOv3 for animal detection
net = cv2.dnn.readNetFromDarknet('C:/Users/harsh/Downloads/yolov3.cfg',
                                 'C:/Users/harsh/Downloads/yolov3.weights')  # Update paths accordingly
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

with open(r'C:\Users\harsh\Downloads\coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Specify the classes to detect (in this case, animals)
animal_classes = ['dog', 'cat', 'bird', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']  # Add more if needed

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect humans (bodies and faces)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 4)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Detect animals using YOLOv3
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    animals = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = scores.argmax()
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in animal_classes:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                animals.append((x, y, w, h))

    # Determine the signal to send to the Arduino
    if len(bodies) > 0 or len(faces) > 0:
        arduino.write(b'H')  # 'H' for human
    elif len(animals) > 0:
        arduino.write(b'A')  # 'A' for animal
    else:
        arduino.write(b'O')  # 'O' for off

    # Show the frame with detection
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (x, y, w, h) in animals:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        arduino.write(b'Q')
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
