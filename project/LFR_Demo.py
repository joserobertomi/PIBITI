import cv2
import numpy as np

def script(pontos): 
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.blur(frame, (10, 10))
        frame = cv2.erode(frame, None, iterations = 10)

        _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        low_b = np.uint8([5])
        high_b = np.uint8([0])
        mask = cv2.inRange(frame, high_b, low_b)
        contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0 :
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] !=0 :
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                print("CX : "+str(cx)+"  CY : "+str(cy))
                if cx >= pontos[1] :
                    print("Turn Left")
                if cx < pontos[1] and cx > 40 :
                    print("On Track!")
                if cx <= pontos[0] :
                    print("Turn Right")
                cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
        else :
            print("I don't see the line")
        cv2.drawContours(frame, c, -1, (0,255,0), 1)
        cv2.imshow("Mask",mask)
        cv2.imshow("Frame",frame)
        if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
            break
    cap.release()
    cv2.destroyAllWindows()
