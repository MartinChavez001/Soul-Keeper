# region Libraries
import pygame
# endregion

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.offsett_y = 0
        self.fixed = False
    def apply(self, entity):
        return entity.rect.move(0, -self.offsett_y)

    def refresh(self, character_y, height):
        if not self.fixed:
            self.offsett_y = max(0, character_y - height // 2)

    def boss_cam(self, character_y, boss_y, fixed_offset_y):
        if character_y >= boss_y:
            self.fixed = True
            self.offsett_y = fixed_offset_y
        else:
            self.fixed = False