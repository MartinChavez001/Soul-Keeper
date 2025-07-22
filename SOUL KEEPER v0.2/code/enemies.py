# region Libraries
import pygame
import random
import os
from pygame import Rect
# endregion

class Ghost:
    def __init__(self, x, y, hp_ghost, size, speed, assets_path, actual_path,enemie_status=True):
        self.x = x
        self.y = y
        self.hp_ghost = hp_ghost
        self.size = size
        self.speed = speed
        self.enemie_status = enemie_status
        self.assets_path = os.path.join(actual_path, "assets")
        self.actual_path = os.path.dirname(os.path.dirname(__file__))
        self.imagen_left_path = os.path.join(self.assets_path, "enemies", "g.png")
        self.imagen_left = pygame.image.load(self.imagen_left_path)
        self.imagen_left = pygame.transform.scale(self.imagen_left, (size, size))
        self.imagen_right_path = os.path.join(self.assets_path, "enemies", "g_r.png")
        self.imagen_right = pygame.image.load(self.imagen_right_path)
        self.imagen_right = pygame.transform.scale(self.imagen_right, (size, size))
        self.imagen_now = self.imagen_right
        

    def move_ghost(self, character_x, character_y):
        if self.x < character_x:
            self.x += self.speed    
            self.imagen_now = self.imagen_right
        elif self.x > character_x:
            self.x -= self.speed
            self.imagen_now = self.imagen_left
        if self.y < character_y:
            self.y += self.speed
        
        elif self.y > character_y:
            self.y -= self.speed

    def hit_ghost(self, arrows):
        hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        for arrow in arrows:
            arrow_rect = pygame.Rect(arrow["x"], arrow["y"], 10, 10)
            if hitbox.colliderect(arrow_rect):
                self.hp_ghost -= 1
                arrows.remove(arrow)
                if self.hp_ghost == 0:
                    self.enemie_status = False
                    return True
        return False
    
    def draw_ghost(self, screen, camera_offsett_y):
        screen.blit(self.imagen_now, (self.x, self.y - camera_offsett_y))

class Boss:
    def __init__(self, boss_images, hitboxs_boss, boss_position, assets_path, actual_path):
        self.boss_images = [pygame.transform.scale(image, (800, 600)) for image in boss_images]
        self.hitboxs_boss = hitboxs_boss  
        self.boss_position = boss_position 
        self.hp_boss = 2000
        self.boss_hurt = False
        self.change_time = 0  
        self.index_image = 0 
        self.animation_time = 0  
        self.projectiles = []  
        self.last_shot = 0
        self.cooldown = 700
        self.assets_path = os.path.join(actual_path, "assets")
        self.actual_path = os.path.dirname(os.path.dirname(__file__))
        self.img_projectile_path = os.path.join(self.assets_path, "enemies", "projectile.png")  
        self.img_projectile = pygame.image.load(self.img_projectile_path)  
        self.img_projectile = pygame.transform.scale(self.img_projectile, (35,55))
        
    def refresh(self, screen, camera, actual_time, projectiles, character, camera_offsett_y, change_time):
        if character.hp_character <= 0 or self.hp_boss <= 0:
            return None
        
        if self.boss_hurt:
            image_to_draw = self.boss_images[2]  
            if actual_time - self.animation_time > 200: 
                self.boss_hurt = False
            
        else:
            if change_time - self.animation_time > 100:  
                self.index_image = (self.index_image + 1) % 2  
                self.animation_time = actual_time
            image_to_draw = self.boss_images[self.index_image]

        screen.blit(image_to_draw, (self.boss_position[0], self.boss_position[1] - camera.offsett_y))

        for projectile in projectiles:
            hitbox_projectile = Rect(projectile["x"], projectile["y"], 35,55)
            for hitbox_boss in self.hitboxs_boss:
                if hitbox_boss.colliderect(hitbox_projectile):
                    self.hp_boss -= 200
                    self.boss_hurt = True
                    self.change_time = change_time
                    projectiles.remove(projectile)

                    if self.hp_boss <= 0:
                        self.hitboxs_boss = []  
                        self.projectiles = []
                        return "boss dead"

        if character.y >= 7000:
            self.boss_shot()

        self.update_shots(screen, camera_offsett_y, character)

        hitbox_character = Rect(character.x, character.y, character.size, character.size)
        for hitbox_boss in self.hitboxs_boss:
            if hitbox_character.colliderect(hitbox_boss):
                character.hp_character = 0 

        return None

    def boss_shot(self):
        actual_time = pygame.time.get_ticks()
        if actual_time - self.last_shot >= self.cooldown:
            self.last_shot = actual_time
            for hitbox in self.hitboxs_boss:
                projectile_x = random.randint(hitbox.left, hitbox.right)
                projectile_y = hitbox.top
                self.projectiles.append({"x": projectile_x, "y": projectile_y})

    def update_shots(self, screen, camera_offsett_y, character):
        for projectile in self.projectiles:
            projectile["y"] -= 10  
            if projectile["y"] < 0:
                self.projectiles.remove(projectile)
            else:
                screen.blit(self.img_projectile, (projectile["x"], projectile["y"] - camera_offsett_y))
                
                hitbox_projectile = Rect(projectile["x"], projectile["y"], 35,55)
                hitbox_character = Rect(character.x, character.y, character.size, character.size)
                if hitbox_projectile.colliderect(hitbox_character):
                    character.hp_character -= 1
                    character.x += 50  
                    self.projectiles.remove(projectile)
