# region Libraries
import pygame
import time
import os

# endregion

class Character:
    def __init__(self, x, y, size, hp_character, iNVINCIBLE_time, assets_path, actual_path): 
        self.x = x              
        self.y = y
        self.size = size
        self.pose = None
        self.speed = 6
        self.speed_x = 0
        self.speed_y = 0
        self.jump_force = -15
        self.in_air = True
        self.arrows = []
        self.cooldown = 1000
        self.last_shot = 0
        self.hp_character = hp_character
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.iNVINCIBLE = False
        self.iNVINCIBLE_time = 0
        self.jumps_remaining = 2
        self.keydrop = True
        self.assets_path = os.path.join(actual_path, "assets")
        self.actual_path = os.path.dirname(os.path.dirname(__file__))
        
        
        self.img_stay_path = os.path.join(self.assets_path, "character", "pj quieto.png")
        self.img_stay = pygame.image.load(self.img_stay_path)
        self.img_left_path = os.path.join(self.assets_path, "character", "pj caminando izquierda.png")
        self.img_left = pygame.image.load(self.img_left_path)
        self.img_right_path = os.path.join(self.assets_path, "character", "pj caminando derecha.png")  
        self.img_right = pygame.image.load(self.img_right_path)
        self.img_jump_left_path = os.path.join(self.assets_path, "character", "pj saltando izquierda.png")
        self.img_jump_left = pygame.image.load(self.img_jump_left_path)
        self.img_jump_right_path = os.path.join(self.assets_path, "character", "pj saltando derecha.png")
        self.img_jump_right = pygame.image.load(self.img_jump_right_path)
        self.img_attack_path = os.path.join(self.assets_path, "character", "PJ disparo.png")
        self.img_attack = pygame.image.load(self.img_attack_path)
        self.img_arrow_path = os.path.join(self.assets_path, "character", "flecha.png")
        self.img_arrow = pygame.image.load(self.img_arrow_path)
        self.img_damage_path = os.path.join(self.assets_path, "character", "pj_daño.png") 
        self.img_damage = pygame.image.load(self.img_damage_path)
        self.lifes3_path = os.path.join(self.assets_path, "character", "3lifes.png")
        self.lifes3 = pygame.image.load(self.lifes3_path)
        self.lifes2_path = os.path.join(self.assets_path, "character", "2lifes.png")
        self.lifes2 = pygame.image.load(self.lifes2_path)
        self.lifes1_path = os.path.join(self.assets_path, "character", "1lifes.png")
        self.lifes1 = pygame.image.load(self.lifes1_path)
        
        # Escalar imágenes
        self.img_stay = pygame.transform.scale(self.img_stay, (size, size))  
        self.img_left = pygame.transform.scale(self.img_left, (size, size))        
        self.img_right = pygame.transform.scale(self.img_right, (size, size))        
        self.img_jump_left = pygame.transform.scale(self.img_jump_left, (size, size)) 
        self.img_jump_right = pygame.transform.scale(self.img_jump_right, (size, size))
        self.img_attack = pygame.transform.scale(self.img_attack, (size, size))
        self.img_arrow = pygame.transform.scale(self.img_arrow, (25, 45))
        self.img_damage = pygame.transform.scale(self.img_damage, (size, size))
        self.lifes3 = pygame.transform.scale(self.lifes3, (350, 160))
        self.lifes2 = pygame.transform.scale(self.lifes2, (350, 160))
        self.lifes1 = pygame.transform.scale(self.lifes1, (350, 160))
        
        #important, base stated of character

        self.pose = self.img_stay

        # endregion
    def move(self, keys, gravity):
    
        if keys[pygame.K_w] and self.jumps_remaining > 0 and self.keydrop:
            self.speed_y = self.jump_force
            self.in_air = True
            self.jumps_remaining -= 1
            self.keydrop = False
        
            if keys[pygame.K_a]:  
                self.pose = self.img_jump_left
            elif keys[pygame.K_d]:  
                self.pose = self.img_jump_right
            else:
                self.pose = self.img_stay  

        if not keys[pygame.K_w]:
            self.keydrop = True 
        if keys[pygame.K_a]:  
            self.x -= self.speed
            self.pose = self.img_left
        elif keys[pygame.K_d]:  
            self.x += self.speed
            self.pose = self.img_right
        else:
            self.pose = self.img_stay

        if keys[pygame.K_DOWN]:  
            self.pose = self.img_attack


        self.speed_y += gravity
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

    def collisions(self, platforms):
        hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        for platform in platforms:
            if hitbox.colliderect(platform):
                if self.speed_y > 0 and hitbox.bottom > platform.top and hitbox.top < platform.top:
                    self.y = platform.top - self.size
                    self.speed_y = 0
                    self.in_air = False
                    self.jumps_remaining = 2
                    
                    return
                elif self.speed_y < 0 and hitbox.top < platform.bottom and hitbox.bottom > platform.bottom:
                    self.y = platform.bottom
                    self.speed_y = 0
                    return
                if hitbox.right > platform.left and hitbox.left < platform.right:
                    if hitbox.centerx < platform.centerx:
                        self.x = platform.left - self.size
                    else:
                        self.x = platform.right
                    return
        self.in_air = True
    def get_position(self):
        return self.x, self.y
    def shot(self):
        actual_time = pygame.time.get_ticks()
        if actual_time - self.last_shot >= self.cooldown:
            self.last_shot = actual_time
            arrow_x = self.x + self.size // 2
            arrow_y = self.y + self.size
            self.arrows.append({"x": arrow_x, "y": arrow_y})
    def tracer(self, speed_shot, camera_offsett_y):
        for arrow in self.arrows:
            arrow["y"] += speed_shot

    def print_shot(self, screen, camera_offsett_y):
        for arrow in self.arrows:
            screen.blit(self.img_arrow, (arrow["x"], arrow["y"] - camera_offsett_y))
    
    def impact(self, source):
        if not self.iNVINCIBLE:
            self.hp_character -= 1
            self.iNVINCIBLE = True
            self.iNVINCIBLE_time = pygame.time.get_ticks()

            # Impacts calculate

            if source.x < self.x:
                self.speed_x = 20
            elif source.x > self.x:
                self.speed_x = -20
            if source.y < self.y:
                self.speed_y = 20
            if source.y > self.y:
                self.speed_y = -20

            self.jumps_remaining = 2
            
    def hit_character(self, danger_objetcs):
        hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        for obj in danger_objetcs:
            if obj.enemie_status:  
                obj_rect = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
                if hitbox.colliderect(obj_rect):
                    self.impact(obj)
                    if self.hp_character <= 0:
                        return True  
        return False
    
    def refresh(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.speed_x *= 0.9
        self.speed_y *= 0.9

        if self.iNVINCIBLE and pygame.time.get_ticks() - self.iNVINCIBLE_time > 1000:
            self.iNVINCIBLE = False
        
    def life_status(self):
        if self.hp_character == 3:
            return self.lifes3
        elif self.hp_character == 2:
            return self.lifes2
        elif self.hp_character == 1:
            return self.lifes1
        else:
            return None
        
    def draw(self,screen, camera_offsett_y):
        screen.blit(self.pose,(self.x, self.y - camera_offsett_y))