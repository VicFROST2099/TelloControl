import pygame
def videoFeed(tello):
    frame = tello.get_frame_read().frame
    frameInWindow = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
    return frameInWindow
