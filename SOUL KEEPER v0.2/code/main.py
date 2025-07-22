# region of libraries
import pygame
import sys
import os
from background import Background
from background import Boss_images
from Camera import Camera
from character import Character
from enemies import Ghost, Boss
# endregion

# region of paths
actual_path = os.path.dirname(os.path.dirname(__file__))

assets_path = os.path.join(actual_path, "assets")

music_path = os.path.join(actual_path, "assets", "Music")

music_paths = {
    "main_theme": os.path.join(music_path,"The Moor - Opeth (game version).mp3"),
    "death_music": os.path.join(music_path,"Gojira - Unicorn (game version).mp3"),
    "boss_music":  os.path.join(music_path,"Voice of the Soul - Death (game version).mp3")
}

background_folder = os.path.join(assets_path, "background")
image_path = [
    os.path.join(background_folder, f"{i}.png") for i in range(1, 10)
]

boss_image_paths = [
    os.path.join(assets_path, "enemies", "boss1.png"),
    os.path.join(assets_path, "enemies", "boss2.png"),
    os.path.join(assets_path, "enemies", "bosshit.png")
]

boss_images = [pygame.image.load(path) for path in boss_image_paths]

# endregion PATHS

# region HITBOXS
platforms = [
    pygame.Rect(670, 220, 390, 25), #platform 1
    pygame.Rect(430, 510, 170, 25), #platform 2            # x, y, width, hight
    pygame.Rect(810, 640, 160, 25), #platform 3
    pygame.Rect(340, 770, 400, 100), #platform 4
    pygame.Rect(780, 1500, 280, 100), #platform 5
    pygame.Rect(400, 2140, 220, 25),  #platform 6      
    pygame.Rect(955, 2280, 105, 300), #platfrom 7
    pygame.Rect(610, 2520, 220, 25),#platform 8
    pygame.Rect(340, 2600, 120, 300), #platform 9
    pygame.Rect(800, 2935, 200, 25), #platform 10
    pygame.Rect(430, 3260, 210, 25), #platform 11
    pygame.Rect(490, 3740, 410, 70), #platform 12
    pygame.Rect(410, 4230, 240, 25), #platform 13
    pygame.Rect(730, 4835, 260, 25), #platform 14
    pygame.Rect(810, 5510, 250, 65), #platform 15
    pygame.Rect(340, 6350, 240, 100), #platform 16
    pygame.Rect(790, 6935, 250, 25), #platform 17
    pygame.Rect(450, 7515, 130, 25), #platform 18
    pygame.Rect(825, 7645, 130, 25), #platform 19
    pygame.Rect(300, 0, 42, 9000), #lateral left
    pygame.Rect(1060, 0, 42, 9000), #lateral right
]

hitboxs_boss = [
    pygame.Rect(390, 7930, 90, 300),  
    pygame.Rect(300, 8080, 800, 215),
    pygame.Rect(916, 7900, 90, 219),
]
boss_position =  (300, 7900)
# endregion 

# region [BASIC CONFIG]
pygame.init()
pygame.mixer.init()
width, height = 1440, 1040
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Soul Keeper")
gravity = 0.5
RED = (255, 0, 0)
clock = pygame.time.Clock()
pygame.mixer.music.load(music_paths["main_theme"])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

Ghost_live = False
# endregion [BASIC CONFIG]

# region DEATHCAM
def death_cam(character, size, screen):
    
    deathcam_path = os.path.join(assets_path, "background", "deathcam.png")
    deathcam = pygame.image.load(deathcam_path)
    deathcam = pygame.transform.scale(deathcam, (screen.get_width(), screen.get_height()))

    Yes_path = os.path.join(assets_path, "text", "Si.png")
    Yes = pygame.image.load(Yes_path)
    Yes = pygame.transform.scale(Yes, (400, 300))
    No_path = os.path.join(assets_path, "text", "No.png")
    No = pygame.image.load(No_path)
    No = pygame.transform.scale(No, (400, 300))

    option = "Yes" 
    decision = True  

    while decision:

        screen.blit(deathcam, (0, 0))

        if option == "Yes":
            screen.blit(Yes, (400, 300))
        else:
            screen.blit(No, (400, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    option = "Yes"
                if event.key == pygame.K_RIGHT:
                    option = "No"
                if event.key == pygame.K_DOWN:
                    return "restart" if option == "Yes" else "quit"
# endregion

# region ENGINE
def game_loop():
    
    character = Character(800, 0 , 80, 3, 1000, assets_path, actual_path)
    background = Background(1000, 800, image_path) 
    Boss_images(1000, 800, boss_images, [boss_position])
    camera = Camera(width, height)
    boss = Boss(boss_images, hitboxs_boss, boss_position, assets_path, actual_path)

    if Ghost_live:
        ghosts = [
            Ghost(500, 900, 3, 100, 2,assets_path,actual_path),
            Ghost(500, 1500, 3, 100, 2,assets_path,actual_path),
            Ghost(500, 2500, 3, 100, 2,assets_path,actual_path),
            Ghost(500, 3500, 3, 100, 2,assets_path,actual_path),
            Ghost(500, 4500, 3, 100, 2,assets_path,actual_path),
            Ghost(500, 5500, 3, 100, 2,assets_path,actual_path),
        ]
        danger_objetcs = ghosts
    else:
        ghosts = []
        danger_objetcs = []
    music_state = "main_theme"  
    fadeout_started = False  

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        actual_time = pygame.time.get_ticks()
        camera.refresh(character.y, height)
        camera.boss_cam(character.y, 7000, 7250)
        background.draw(screen, camera.offsett_y)
        change_time = pygame.time.get_ticks()  
        
        
        if character.hp_character > 0:
            life_image = character.life_status()
            if life_image:
                screen.blit(character.life_status(), (1100, 820))
                character.draw(screen, camera.offsett_y)
                character.move(keys, gravity)
                character.refresh()  

                if character.y > 7000 and music_state == "main_theme":
                    pygame.mixer.music.fadeout(1000) 
                    music_state = "boss_music" 
                    fadeout_started = True  

            if keys[pygame.K_DOWN]:
                character.shot()
            character.tracer(speed_shot=8, camera_offsett_y=camera.offsett_y)
            character.print_shot(screen, camera.offsett_y)
        
            hitbox = pygame.Rect(character.x, character.y, character.size, character.size)
            for platform in platforms:
                #pygame.draw.rect(screen, RED, platform,-camera.offsett_y)
                if hitbox.colliderect(platform):
                    character.collisions(platforms)

            for hitbox in hitboxs_boss:
                hitbox_boss_draw = hitbox.move(0, -camera.offsett_y)  
                pygame.draw.rect(screen, RED, hitbox_boss_draw)
        
            if Ghost_live:
                for ghost in ghosts:
                    if ghost.hp_ghost > 0:
                        character_x, character_y = character.get_position()
                        distance = abs(ghost.x - character_x) + abs(ghost.y - character_y)
                        if distance < 1000:
                            ghost.move_ghost(character_x, character_y)
                        ghost.draw_ghost(screen, camera.offsett_y)
                        ghost.hit_ghost(character.arrows) 
        
            if character.hit_character(danger_objetcs):
                print("character is dead.")

            if boss.hp_boss > 0:
                for hitbox in hitboxs_boss:
                    hitbox_boss_draw = hitbox.move(0, -camera.offsett_y)  
                    #pygame.draw.rect(screen, RED, hitbox_boss_draw)

                boss.refresh(screen, camera, actual_time, character.arrows, character, camera.offsett_y, change_time)
            
            if fadeout_started and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(music_paths[music_state])
                pygame.mixer.music.play(-1)
                fadeout_started = False

            if character.hp_character <= 0:
                if music_state != "death_music":  
                    pygame.mixer.music.stop() 
                    pygame.mixer.music.load(music_paths["death_music"]) 
                    pygame.mixer.music.play(-1)
                    music_state = "death_music"
                decision = death_cam(character, character.size, screen)
                if decision == "restart":
                    pygame.mixer.music.load(music_paths["main_theme"])
                    pygame.mixer.music.play(-1)
                    music_state = "main_theme"
                    return "restart"  
                elif decision == "quit":
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            clock.tick(60)  
    pygame.mixer.music.stop()
    pygame.quit()
# endregion

# region GAME STAR
def main():
    while True:
        result = game_loop()
        if result != "restart":
            break

if __name__ == "__main__":
    main()

# endregion


