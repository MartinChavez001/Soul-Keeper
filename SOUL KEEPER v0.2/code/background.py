# region Libraries
import pygame
# endregion

class Background:
    def __init__(self, height, width, image_paths):
        self.images = [pygame.transform.scale(pygame.image.load(path), (width, height)) for path in image_paths]
        self.rects = [image.get_rect() for image in self.images]
        for i, rect in enumerate(self.rects):
            rect.topleft = ((width - rect.width // 1.6), i * height)
    
    def draw(self, screen, offsett_y):
        for image, rect in zip(self.images, self.rects):
            new_y = rect.y - offsett_y  
            if -screen.get_height() < new_y < 2 * screen.get_height():
                screen.blit(image, (rect.x, new_y))

class Boss_images:
    def __init__(self, height, width, boss_images, boss_positions):
        self.boss = [pygame.transform.scale(image, (400, 300)) for image in boss_images]
        self.rects_boss = [image.get_rect() for image in self.boss]
        for rect, pos in zip(self.rects_boss, boss_positions):
            rect.topleft = pos
        
        self.boss_hurt = False
        self.change_time = 0  
        self.index_image = 0 
        self.animation_time = 0  
