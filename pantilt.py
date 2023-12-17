import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    cv2.resizeWindow('img', 500, 500)
    cv2.line(img, (500, 250), (0, 250), (0, 255, 0), 1)
    cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 1)
    cv2.circle(img, (250, 250), 5, (255, 255, 255), -1)

    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Definir el rango de colores para el rojo en formato HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Filtrar por color rojo
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos y obtener el centro del objeto rojo
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filtrar contornos pequeños
            cv2.drawContours(img, [contour], 0, (0, 255, 0), 2)
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
                print("Center of Object is :", (cx, cy))

                # Hacer algo con las coordenadas del objeto (puedes enviarlas por serial al Arduino)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()