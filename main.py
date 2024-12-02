import cv2
import time
import hand as htm

X_START, Y_START = 50, 50
BUTTON_SIZE = 70
BUTTON_GAP = 30
MY_KEYBOARD = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

class Button:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
    def draw(self, frame, color):
        pt = [self.pos[0] + BUTTON_SIZE, self.pos[1] + BUTTON_SIZE]
        cv2.rectangle(frame, self.pos, pt, color, cv2.FILLED)
        cv2.putText(frame, self.text, [self.pos[0] + BUTTON_SIZE // 5, pt[1] - BUTTON_SIZE // 5], cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, cap.get(3) * 2)
cap.set(4, cap.get(4) * 2)
print(cap.get(3), cap.get(4))
pTime = time.time()
detector = htm.handDetector(detectionCon=1)

def finger_pointing(finger, button):
    return button.pos[0] <= finger[1] and finger[1] <= button.pos[0] + BUTTON_SIZE and button.pos[1] <= finger[2] and finger[2] <= button.pos[1] + BUTTON_SIZE
           

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    cTime = time.time()
    fps = int(1 / (cTime - pTime))
    pTime = cTime
    cv2.putText(frame, 'FPS: ' + str(fps), (15, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    for i in range(0, 3):
        for j in range(len(MY_KEYBOARD[i])):
            cur_button = Button([Y_START + j * (BUTTON_SIZE + BUTTON_GAP), X_START + i * (BUTTON_SIZE + BUTTON_GAP)], MY_KEYBOARD[i][j])
            cur_button.draw(frame, (255, 0, 255))
    if len(lmList) != 0:
        finger = lmList[8]
        for i in range(0, 3):
            for j in range(len(MY_KEYBOARD[i])):
                cur_button = Button([Y_START + j * (BUTTON_SIZE + BUTTON_GAP), X_START + i * (BUTTON_SIZE + BUTTON_GAP)], MY_KEYBOARD[i][j])
                if finger_pointing(finger, cur_button):
                    pt = [cur_button.pos[0] + BUTTON_SIZE, cur_button.pos[1] + BUTTON_SIZE]
                    cur_button.draw(frame, (255, 0, 132))
        cv2.circle(frame, (lmList[8][1], lmList[8][2]), 15, (0, 255, 0), -1)
    cv2.imshow('Virtual Keyboard', frame)
    if cv2.waitKey(1) == ord('s'):
        break
cap.release()
cv2.destroyAllWindows()