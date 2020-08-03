
import cv2, os
from sys import argv

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')





if argv[1] == 'g':
  
  try:
    int(argv[2])
  except:
    print('face_id must be integer!')
    quit(1)

  os.mkdir('dataset/' + argv[2])
  vid_cam = cv2.VideoCapture(0)
  count = 0
  
  while(True):
    _ , image_frame = vid_cam.read()
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
      cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255,0,0), 2)
      cv2.imwrite('dataset/' + argv[2] + '/' + str(count) + '.jpg', gray[y : y + h, x : x + w])
      cv2.imshow('frame', image_frame)
      count += 1

    if cv2.waitKey(100) & 0xFF == ord('q') or count > 200:
      break
    
  vid_cam.release()
  cv2.destroyAllWindows()
  
  
      
      
      
elif argv[1] == 't':
  
  import numpy as np
  from PIL import Image

  recognizer = cv2.face.LBPHFaceRecognizer_create()
  face_imgs, ids = [], []
  
  for face_id in os.listdir('dataset'):
    for sample in os.listdir('dataset/' + face_id):
      path = 'dataset/' + face_id + '/' + sample
      print('processing : ' + path)
      PIL_img = Image.open(path).convert('L')
      numpy_img = np.array(PIL_img,'uint8')
      faces = face_detector.detectMultiScale(numpy_img)
      for (x, y, w, h) in faces:
        face_imgs.append(numpy_img[y : y + h, x : x + w])
        ids.append(int(face_id))

  recognizer.train(face_imgs, np.array(ids))
  recognizer.save('model.yml')
  




elif argv[1] == 'r':
  
  board = None
  
  try:
    
    from pyfirmata import Arduino
    
    if os.name == 'nt':
      board = Arduino('COM3')
    else:
      board = Arduino('/dev/ttyACM0') # goto arduino ide -> examples -> Firmata -> StandardFirmata and burn it into board before
  except Exception as e:
    print(str(e) + '\nBOARD NOT WORKING')
  
  board_is_active = 0
  
  def board_start():
    global board_is_active
    if board:
      
      # DO ARDUINO ACTIONS AFTER STARTING BOARD HERE
      board.digital[12].write(1)
      board.digital[13].write(0)
    
    board_is_active = 0
  
  def board_stop():
    global board_is_active
    if board:
      
      # DO ARDUINO ACTIONS BEFORE STOPPING BOARD HERE
      board.digital[12].write(0)
      board.digital[13].write(0)
    
    board_is_active = 0
  
  from time import sleep
  
  def board_if_success():
    global board_is_active
    if board:
      
      # DO ARDUINO ACTIONS IF VERIFIED HERE
      board.digital[12].write(0)
      board.digital[13].write(1)
      sleep(2)
      board.digital[12].write(1)
      board.digital[13].write(0)
      
    board_is_active = 0
      
  from threading import Thread
  
  def launch_board_action(action):
    global board_is_active
    if board_is_active == 0:
      board_is_active = 1
      t = Thread(target = action)
      t.daemon = True
      t.start()

  recognizer = cv2.face.LBPHFaceRecognizer_create()
  recognizer.read('model.yml')
  font = cv2.FONT_HERSHEY_SIMPLEX
  vid_cam = cv2.VideoCapture(0)
  FACE_CONFD_THRESHOLD = 50 # percent
  board_start()

  while True:
    ret, im = vid_cam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.2, 5)
    
    for (x, y, w, h) in faces:
      face_id, distrust = recognizer.predict(gray[y : y + h, x : x + w])
      confidence = 100 - distrust
      caption = '%s -> %s' % (face_id, round(confidence, 2))
      if confidence >= FACE_CONFD_THRESHOLD:
        launch_board_action(board_if_success)
        rect_col = (0, 255, 0)
      else:
        rect_col = (0, 0, 255)
      cv2.rectangle(im, (x - 20, y - 20), (x + w + 20, y + h + 20), rect_col, 4)
      cv2.rectangle(im, (x - 22, y - 90), (x + w + 22, y - 22), rect_col, -1)
      cv2.putText(im, caption, (x, y - 40), font, 1, (255, 255, 255), 3)
      
    cv2.imshow('im', im) 
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break
    

  vid_cam.release()
  cv2.destroyAllWindows()
  board_stop()

      
    


