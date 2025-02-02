import RPi.GPIO as GPIO
import spidev
import time
import math

RCLK_PIN = 24
OE_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCLK_PIN, GPIO.OUT)
GPIO.setup(OE_PIN, GPIO.OUT)
# disable output
GPIO.output(OE_PIN, GPIO.HIGH)

spi = spidev.SpiDev()  # Create SPI object
spi.open(0, 0)         # Open SPI bus 0, device (chip select) 0
# Set SPI speed and mode
spi.max_speed_hz = 50000  # 50 kHz
spi.mode = 0              # SPI mode 0

def gpio_start():

  # start
  GPIO.output(OE_PIN, GPIO.LOW)



def send_sr_byte(sr_byte):
  spi.xfer([sr_byte])
  # latch in
  GPIO.output(RCLK_PIN, GPIO.LOW)
  time.sleep(5/1000000.0)
  GPIO.output(RCLK_PIN, GPIO.HIGH)

flap = 0
mouth = 0

def update_motors():
  global flap
  global mouth
  sr_byte = 0
  if flap > 0:
    sr_byte |= 1 << 5
  if flap < 0:
    sr_byte |= 1 << 7
  if mouth > 0:
    sr_byte |= 1 << 6
  if mouth < 0:
    sr_byte |= 1 << 0
  send_sr_byte(sr_byte)
  
def mouth_open():
  # print("[O]", end=' ', flush=True)
  global mouth
  mouth = -1
  update_motors()

def mouth_close():
  # print("[C]", end=' ', flush=True)
  global mouth
  mouth = 1
  update_motors()

def mouth_neutral():
  global mouth
  mouth = 0
  update_motors()

def flap_forward():
  global flap
  flap = -1
  update_motors()

def flap_backward():
  global flap
  flap = 1
  update_motors()

def flap_neutral():
  global flap
  flap = 0
  update_motors()

def gpio_cleanup():
  GPIO.cleanup()
  print("GPIO cleanup complete")

def main():
  gpio_start()

  while True:
    flap_forward()
    time.sleep(1)

    mouth_open()
    time.sleep(0.2)
    mouth_close()
    time.sleep(0.4)
    mouth_open()
    time.sleep(0.3)
    mouth_close()
    time.sleep(0.1)
    mouth_open()
    time.sleep(0.3)
    mouth_close()
    time.sleep(0.1)
    mouth_neutral()
    time.sleep(1)

    flap_backward()
    time.sleep(0.3)
    flap_neutral()
    time.sleep(2)

if __name__ == "__main__":  
  try:
    main()
  except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    print("Program interrupted")

  finally:
    # Clean up GPIO
    GPIO.cleanup()
    print("GPIO cleanup complete")
