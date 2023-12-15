import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Configuración de pines GPIO para los servos
pan_pin = 18  # Pin GPIO para el servo de pan
tilt_pin = 23  # Pin GPIO para el servo de tilt

GPIO.setmode(GPIO.BCM)
GPIO.setup(pan_pin, GPIO.OUT)
GPIO.setup(tilt_pin, GPIO.OUT)

pan_servo = GPIO.PWM(pan_pin, 50)  # Configura el pin PWM a 50 Hz (20 ms de periodo)
tilt_servo = GPIO.PWM(tilt_pin, 50)

pan_servo.start(7.5)  # Posición inicial del servo de pan
tilt_servo.start(7.5)  # Posición inicial del servo de tilt

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Ancho de la imagen
cap.set(4, 480)  # Altura de la imagen

# Rangos de color para el rojo en formato HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Filtrar por color rojo
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande (suponiendo que sea el objeto que estás buscando)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)

        # Calcular el centro del objeto
        center_x = x + w // 2
        center_y = y + h // 2

        # Hacer seguimiento ajustando los servos
        pan_position = center_x / 640 * 180  # Escalar la posición al rango de 0 a 180 grados
        tilt_position = center_y / 480 * 180

        pan_servo.ChangeDutyCycle(pan_position / 18 + 2.5)
        tilt_servo.ChangeDutyCycle(tilt_position / 18 + 2.5)

    # Mostrar la imagen
    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Presiona Esc para salir
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
