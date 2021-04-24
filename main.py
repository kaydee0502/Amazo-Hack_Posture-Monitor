import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic



class Posture:
    def __init__(self):
        self.rshold = None
        self.lshold = None
        self.nose = None
        self.isCap = True


def checkPose(nose,rsh,lsh,toComp):
    pass






cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    
  cposture = Posture()
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = holistic.process(image)
    image_height, image_width, _ = image.shape

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    '''
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
    '''
  
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Holistic', image)
    print("LEFT SHOULDER","RIGHT SHOULDER","NOSE")
    if results.pose_landmarks:
        cnose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_width
        
        crshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_width
        
        clshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_width
        
        print(clshold,crshold,cnose)
   
    
   
    print(cposture.lshold,cposture.rshold,cposture.nose)
    if cv2.waitKey(1) == ord('c') and cposture.isCap:
        cposture.isCap = False
        cposture.rshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_width
        cposture.lshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_width
        cposture.nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_width
    
    try:
        checkPose(cnose,crshold,clshold,cposture)
    except:
        pass
    
    if cv2.waitKey(1) == ord('q'):
         break
    
cap.release()