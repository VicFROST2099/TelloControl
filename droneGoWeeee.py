from djitellopy import Tello
from droneCam import videoFeed
import pygame
import threading
import time

pygame.init()
clock = pygame.time.Clock()
displayInfo = pygame.display.Info()
width, height = displayInfo.current_w, displayInfo.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tello Drone")

frameWidth, frameHeight = 960, 720
xOffset = (width - frameWidth) // 2
yOffset = (height - frameHeight) // 2

tello = Tello()
tello.connect()
tello.streamon()

font = pygame.font.SysFont("Arial", 20)

running = True
vel = {"lr": 0, "fb": 0, "ud": 0, "yaw": 0}
def movementControl():
    while running:
        tello.send_rc_control(vel["lr"], vel["fb"], vel["ud"], vel["yaw"])
        time.sleep(0.05)
threading.Thread(target=movementControl, daemon=True).start()

while running:
    cameraView = videoFeed(tello)
    screen.fill((0, 0, 0))
    screen.blit(cameraView, (xOffset, yOffset))
    
    battery = tello.get_battery()
    highTemp = tello.get_highest_temperature()
    lowTemp = tello.get_lowest_temperature()
    flightTime = tello.get_flight_time()
    droneHeight = tello.get_height()
   
    batteryText = font.render(f"Battery: {battery}%", True, (255, 255, 255))
    hTempText = font.render(f"High Temp: {highTemp}°C", True, (255, 255, 255))
    lTempText = font.render(f"Low Temp: {lowTemp}°C", True, (255, 255, 255))
    flightTimeText = font.render(f"Flight Time: {flightTime} Seconds", True, (255, 255, 255))
    droneHeightText = font.render(f"Height: {droneHeight} cm", True, (255, 255, 255))
    
    controlsHeader = font.render("Controls:", True, (255, 255, 255))
    takeOffText = font.render("T = Take-Off", True, (255, 255, 255))
    landText = font.render("L = Land", True, (255, 255, 255))
    emergencyStopText = font.render("P = Emergency Stop", True, (255, 255, 255))
    forwardText = font.render("W = Forward", True, (255, 255, 255))
    backwardText = font.render("S = Backward", True, (255, 255, 255))
    leftText = font.render("A = Left", True, (255, 255, 255))
    rightText = font.render("D = Right", True, (255, 255, 255))
    upText = font.render("↑ = Up", True, (255, 255, 255))
    downText = font.render("↓ = Down", True, (255, 255, 255))
    rotateLeftText = font.render("← = Rotate Left", True, (255, 255, 255))
    rotateRightText = font.render("→ = Rotate Right", True, (255, 255, 255)) 
    flipForwardText = font.render("8 = Flip Forward", True, (255, 255, 255))
    flipBackwardText = font.render("2 = Flip Backward", True, (255, 255, 255))
    flipLeftText = font.render("4 = Flip Left", True, (255, 255, 255))
    flipRightText = font.render("6 = Flip Right", True, (255, 255, 255))
    quitText = font.render("ESC = Exit Program", True, (255, 255, 255))

    screen.blit(batteryText, (10, 10))
    screen.blit(hTempText, (10, 30))
    screen.blit(lTempText, (10, 50))
    screen.blit(flightTimeText, (10, 70))
    screen.blit(droneHeightText, (10, 90))
    
    screen.blit(controlsHeader, (width - 200, 10))
    screen.blit(takeOffText, (width - 200, 30))
    screen.blit(landText, (width - 200, 50))
    screen.blit(emergencyStopText, (width - 200, 70))
    screen.blit(forwardText, (width - 200, 90))
    screen.blit(backwardText, (width - 200, 110))
    screen.blit(leftText, (width - 200, 130))
    screen.blit(rightText, (width - 200, 150))
    screen.blit(upText, (width - 200, 170))
    screen.blit(downText, (width - 200, 190))
    screen.blit(rotateLeftText, (width - 200, 210))
    screen.blit(rotateRightText, (width - 200, 230))
    screen.blit(flipForwardText, (width - 200, 250))
    screen.blit(flipBackwardText, (width - 200, 270))
    screen.blit(flipLeftText, (width - 200, 290))
    screen.blit(flipRightText, (width - 200, 310))
    screen.blit(quitText, (width - 200, 330))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_t:
                threading.Thread(target=tello.takeoff).start()
            elif event.key == pygame.K_l:
                threading.Thread(target=tello.land).start()
            elif event.key == pygame.K_p:
                threading.Thread(target=tello.emergency).start()
            elif event.key == pygame.K_w:
                vel["fb"] = 50
            elif event.key == pygame.K_s:
                vel["fb"] = -50
            elif event.key == pygame.K_a:
                vel["lr"] = -50
            elif event.key == pygame.K_d:
                vel["lr"] = 50
            elif event.key == pygame.K_UP:
                vel["ud"] = 50
            elif event.key == pygame.K_DOWN:
                vel["ud"] = -50
            elif event.key == pygame.K_LEFT:
                vel["yaw"] = -50
            elif event.key == pygame.K_RIGHT:
                vel["yaw"] = 50
            elif event.key == pygame.K_KP8:
                threading.Thread(target=tello.flip_forward).start()
            elif event.key == pygame.K_KP2:
                threading.Thread(target=tello.flip_back).start()
            elif event.key == pygame.K_KP4:
                threading.Thread(target=tello.flip_left).start()
            elif event.key == pygame.K_KP6:
                threading.Thread(target=tello.flip_right).start()
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s]:
                vel["fb"] = 0
            elif event.key in [pygame.K_a, pygame.K_d]:
                vel["lr"] = 0
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                vel["ud"] = 0
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                vel["yaw"] = 0
    pygame.display.update()
    clock.tick(60) 
pygame.quit()
tello.end()