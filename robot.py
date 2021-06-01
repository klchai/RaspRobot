import sys
import socket
import Adafruit_PCA9685
import RPi.GPIO as GPIO

## PARTIE CONTROLE            
pwm_A = 0
pwm_B = 0

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 0
left_backward = 1

right_forward = 0
right_backward= 1

def stop():#Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)

def setup():#Motor initialization
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)

	stop()
	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 1000)
		pwm_B = GPIO.PWM(Motor_B_EN, 1000)
	except:
		pass

def left(status, direction, speed):#Motor 2 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_B_Pin1, GPIO.LOW)
		GPIO.output(Motor_B_Pin2, GPIO.LOW)
		GPIO.output(Motor_B_EN, GPIO.LOW)
	else:
		if direction == Dir_backward:
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		elif direction == Dir_forward:
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)

def right(status, direction, speed):#Motor 1 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_A_Pin1, GPIO.LOW)
		GPIO.output(Motor_A_Pin2, GPIO.LOW)
		GPIO.output(Motor_A_EN, GPIO.LOW)
	else:
		if direction == Dir_forward:#
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
	return direction

def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
	#speed = 100
	if direction == 'forward':
		if turn == 'right':
			left(0, left_backward, int(speed*radius))
			right(1, right_forward, speed)
		elif turn == 'left':
			left(1, left_forward, speed)
			right(0, right_backward, int(speed*radius))
		else:
			left(1, left_forward, speed)
			right(1, right_forward, speed)
	elif direction == 'backward':
		if turn == 'right':
			left(0, left_forward, int(speed*radius))
			right(1, right_backward, speed)
		elif turn == 'left':
			left(1, left_backward, speed)
			right(0, right_forward, int(speed*radius))
		else:
			left(1, left_backward, speed)
			right(1, right_backward, speed)
	elif direction == 'no':
		if turn == 'right':
			left(1, left_backward, speed)
			right(1, right_forward, speed)
		elif turn == 'left':
			left(1, left_forward, speed)
			right(1, right_backward, speed)
		else:
			stop()
	else:
		pass

init_speed = 60

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 robot.py robot_name router_ip")
    else:
        #constants
        ROBOT_NAME = sys.argv[1]
        ROUTER_IP = sys.argv[2]
        MSG_MAX_SIZE = 1024
        PORT = 9000
        COMMANDS = ["register", "forward", "backward", "left", "right", "speed"]

        # Init du motor
        setup()
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(50)
        init_speed = 60

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ROUTER_IP, PORT))
        msg = f"register {ROBOT_NAME}"
        sock.send(msg.encode("ascii"))
        print(f"Robot {ROBOT_NAME} is started")
        while True:
            command = sock.recv(MSG_MAX_SIZE).decode("ascii")
            print("msg recu ",command)
            if command == "forward":
                print("Forward")
                move(init_speed, 'forward', 'no', '0.8')
            elif command == "backward":
                print("Backward")
                move(init_speed, 'backward', 'no', '0.8')
            elif command == "left":
                print("Left")
                move(init_speed, 'no', 'left', '0.8')
            elif command == "right":
                print("Right")
                move(init_speed, 'no', 'right', '0.8')
            elif command == "speed":
                new_speed = input("Change speed:")
                init_speed = int(new_speed)
                print(f"Speed now is {init_speed}")
            else:
                print(f"Command '{command}' is incorrect")


if __name__ == "__main__":
    main()
