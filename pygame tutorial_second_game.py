import os
import random
import math
import pygame
from os import listdir
from os.path import isfile,join

#we need os for loading all images and sprite sheets. thus we wont need to manually type specific file names


#Use pygame.display.flip() when you want to update the entire display surface at once,
# typically at the end of each frame in your game loop.
# This ensures a smooth and consistent experience for the player.


# Use pygame.display.update() when you know which specific areas of the display have changed,
# and you want to update only those regions to save processing time.
# This is particularly beneficial when you have complex scenes with many static elements that do not change frequently.


pygame.init()
pygame.display.set_caption('My second game')

#GLOBAL VARIABLES

WIDTH,HEIGHT= 900,700
FPS = 45# frames per second in our game
player_vel = 5 # speed at which our player moves on screen

window= pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites): #if you look at our sprites in assets folder, you will see that all character images face right.

    # However, we also need to change character's side to left when direction is left. that's why we will flip the image

    #variable sprites will be a list of sprites

    return [pygame.transform.flip(sprite, True,False) for sprite in sprites]# second parameter is asking flipping in x direction and
    # third for flipping in y direction. we just need to flip it horizontally

def load_sprite_sheets(directory1,directory2,width,height,direction=False):#this is going to load sprite sheets for character. for example if we want to jump, we will load animation of jumping

    #we need directory variables to load other images which aren't about our character. we can thus quickly switch character and have prepared sprite sheets of them

    #height,width for character image size

    #direction is for loading multiple directions. if it is false, same animation for left and right
    # if this is True, then direction will have different animations for left and right

    path = join('assets',directory1,directory2)#we will firstly get in main folder like Main Character,then get in one of the specific folders, thus getting all images of particular character

    images= [ f for f in listdir(path) if isfile(join(path,f))]#image is list of files of that folder in path but it also checks whether it is file or whole folder by using isfile
    # basically listdir creates suitable format for isfile func by making list of files inside path variable

    all_sprites={}#the keys in this dict will be animation style(running,jumping,hitting,etc.) and values will be all the images of specific action in animation
    for image in images:

        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()#join serves as building a way to get access to smth. so we need directory as first parameter and filename as second
        #convert_alpha=  so its back stuff is actually in background. what I want to say is we see character but from the back it is already kinda mixed with background

        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):# so lets say there are 6 images in one file. and total width of that 360.
        # so each image is 60. then we will divide whole file width by single image width and it is like cutting each time same amount of paper from big paper

            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)#src alpha is same as convert_alpha(it makes frame transparent)
            #if you want to display a character animation and animate it by showing different frames in succession, you'll need to use surfaces to represent each frame of the animation.

            #surfaces are like frames in tkinter

            rect = pygame.Rect(i * width,0,width,height)#if you noticed, we haven't cut images individually yet. we just divided width in for loop but we didnt cut them
            #that's why each time loop goes, if there are 6 images in file(each 30 pixels wide), first image will be taken for example(0 * 30 , 0, 30 ,30)
            #then second (1*30,0,30,30). thus we will choose another image each time  and creating rect for each of them. Thus, we will create separate images in rectangles

            #it is better to blit character on surface we created instead of on background.
            # for multiple reasons - double buffering,scene management,or for charaging specific parts of screen instead of whole background

            surface.blit(sprite_sheet,(0,0),rect)#third parameter is area. area variable is always either none or rect. you put coordinates x,y,width,height for rect,
            # which is going to take specific portion (based on width and height given of how much to take) of first parameter. it will take portion from first parameter's image based on given x,y

            #NOTE: remember that we didn't blit this surface on our main window(background) yet. so yes, we blitted character on surface,
            # but this surface is not blitted on main screen so it is not seen. that's why we add each of them to sprites list below

            # i need rect because thus I can blit on my screen individual image.
            # sprite sheet variable loads whole image file which has 6 images together
            # so to separate i created surface and then put whole image file on it but with rect i will take only specified portion

            sprites.append(pygame.transform.scale2x(surface))#this makes default size 2 times larger and
            #scaling the images 2x can create a retro, low-resolution look(it is like in games terraria or dead cells).
            # you see their character are not exact, they are kinda pixelated and vague-like(a bit blurry)

            #if you want to know how scaling impacts visual, then -- When you apply 2x scaling using pygame.transform.scale2x(), it doesn't add new pixels to the image.
            # Instead, it increases the size of each existing pixel. Each pixel in the original image is duplicated to cover four pixels in the new, larger image.
            # These duplicated pixels will have the exact same color as the original pixel, so the color information is preserved.
            # The issue with 2x scaling is that it doesn't add any new details to the image.
            # The scaled-up image lacks additional information that would have been present if the image were created at the larger size from the start.
            # This can lead to a blocky and pixelated appearance, which can sometimes be perceived as visually blurry because of the lower level of detail.
            # (other info of pixels are Fine Gradients and Textures,shapr edges,small features,Subtle Lighting and Shadows) these are like not added when scaling.
            # -- that's why detailed image disappears and it becomes kinda vague
        if direction:
            all_sprites[image.replace('.png','')+'_right']=sprites#remember images are list of all filenames in the directory
            all_sprites[image.replace('.png', '') + '_left'] = flip(sprites)# dont forget that we created flip function above

            #so what we essentially did was we created two MAIN keys(left and right) for all sprites dict.
            #we gave sprites list( which contains each individual frame and logically all frames there are in right direction)
            #to keys with names "double_jump_right","fall_right" and etc. If direction is left however,
            # we give sprites list but flipped version to keys with names "double_jump_left","fall_left" and etc.


            #so how it all goes - first for loop loads image file(lets say containing 6 images) ,
            # then second for loop starts and we make frames individually and each time in second for loop, we add new created individual frame to our sprites list
            #then we go to "if direction". since first for loop still didnt change its value, first key name will be "double jump_right"
            # and as I said earlier, the frames for double jump that we appended in sprites list will now be value to double jump key.
            #after this,second loop finishes and it all starts again, first for loop iterates to second image file,
            # and sprites list gets clear of all previous individual frames, which means this time when key is "fall_right", the frames of the second image in first for loop will be of falling
            #I want to say that thus we won't mix all animation frames of different actions in one list since it gets clear each iteration AFTER storing all of its frames to suitable action(key) in dictionary

        else:
            all_sprites[image.replace('.png','')] = sprites#we need else since sometimes characters are symmetrical in both direcitons

    return all_sprites#at the end of all of this,function returns all the animation frames invidiually and each connected to its right key in dict


def load_block(size):
    path = join('assets','Terrain','Terrain.png')
    image = pygame.image.load(path).convert_alpha()#convert_alpha for transparent background
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)#width , height = size,size
    rect = pygame.Rect(0,128,size,size)#the first two parameters - we pass coordinates of the block which we want to use from all of the others in terrain file
    surface.blit(image,(0,0),rect)#thus we create block separately from others.
    return pygame.transform.scale2x(surface)



#for sprite animations, we will need to use a class from pygame but INHERIT it to add our own methods/attributes with it as well:

class Player(pygame.sprite.Sprite):#this class allows us very easy to do pixel perfect collision

    COLOR=(255, 0, 0)
    GRAVITY = 1 #value for acceleration in gravity
    ANIMATION_DELAY = 3#amount of delay between changing sprites


    #now let's use our sprite sheets from our sprite sheet loading function
    SPRITES= load_sprite_sheets('MainCharacters','NinjaFrog',32,32,True)#we pass true since we dont want animations to repeat in both left/right directions


    def __init__(self,x,y,width,height):
        super().__init__()

        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=0

        self.y_vel = 0#the x and y velocity show how fast we will move our player in x and y directions per frame
        #we will apply velocity to move in particular direction and then it will be again as 0 when for example stopped somewhere

        self.mask=None

        self.direction = 'left' #this is for our player's face.
        # if its face is turned to right, we can turn it to left,for example, when player choose to move back/left

        self.animation_count = 0#we can change animation when turning left/right solely depending on self.direction.
        # but animation count is basically responsible for NOT LAGGY but smooth transition of animation when switching direction

        self.fall_count= 0 #this variable will tell us for how long (in frames) we were falling when jumping.
        # thus, we will know by how much we need to increase y velocity with gravity. for example if jumping from long building, then we have to accelerate faster than falling from short height right?

        self.jump_count = 0

        self.hit = False
        self.hit_count = 0

    def jump(self):

        # don't forget that when we go up in y direction, we should have negative velocity and when down, then positive vel.

        self.y_vel = -self.GRAVITY * 8#you can choose any number to multiply to. it will just affect speed of your jump

        self.animation_count = 0
        self.jump_count += 1

        if self.jump_count == 1:# we need this if statement because when jumping first time,it will be full jump
            # without any falling value being added to y velocity(we reset fall count below)
            #thus when there is second jump, fall count is not reset which means falling value will be added to y velocity
            #and that's why second jump will be smaller

            self.fall_count = 0#By resetting fall_count to 0 only on the first jump,
            # you allow the second jump to be slightly lower than the first one.

    def move(self,dx,dy):#displacement x/y
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_left(self,velocity):# by moving right,velocity is positive. by moving left, it is like moving back so negative value given
        self.x_vel = -velocity
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count= 0
    def move_right(self,velocity):
        self.x_vel = velocity
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count= 0
    #in pygame, if you go up in y axis, you subtract. if down, you add. if left in x axis, you subtract. if right , you add.

    def loop(self,fps):
        #Making the "falling" animation conditional on the y-velocity (y_vel) being positive is a more efficient approach

        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)#remember velocity is at what speed player goes in some direction
        #so here we try to find the fraction of time that the player has been falling out of the total time of each second(fall count/fps)
        #then it is multipled by gravity to make effect of acceleration.
        # and min is just used for safety reasons - in case all this calculation gets too high, computer will simply take 1 as minimum
        self.move(self.x_vel,self.y_vel)

        if self.hit:
            self.hit_count+=1
        if self.hit_count > 15:# you could also use instead of this if statement -> if self.hit_count > FPS * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count +=1#  when 60/60 fps = 1 second of falling
        self.update_sprite()

    def landed(self):#after falling at the start of game, we will hit the block
        # but that's when python will see that the limit is to be on top of block,thus not letting player going down further
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1#we want to reverse our velocity when ,let's say, after jumping and hitting object above us,we should immediately start falling back on the  ground right?



    def update_sprite(self):#this is for updating/changing our frames for creating animation on screen

        sprite_sheet = 'idle'#this is default animation. if we dont run, jump, being attacked, or etc.,then we just use idle
        if self.hit:
            sprite_sheet = 'hit'

        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = 'jump'
            elif self.jump_count == 2:
                sprite_sheet = 'double_jump'

        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = 'fall'

        elif self.x_vel != 0:
            sprite_sheet = 'run'



        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]


        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        #animation delay shows us different sprite when changing animation every 5 frames. so every 5 frames we check whether action was done or not, and then change animation frame to different one
        #self.animation_count // self.ANIMATION_DELAY - let's say person was running for 2 seconds which is (2 * 60 fps = 120 frames of running in total)
        #now, we should show repeated running animation in those 2 seconds. that's why if animation changes only every 5 frames
        #how many times will running cycle be repeated in 120 frames? 24 times( 120//5). 24 times running animation will be repeated
        # how we achieve loop, by which I mean, how we achieve so that after all frames in running key in dict are done once, to keep this running animation repeated more?
        #To achieve a looping animation, we need to make sure that when self.animation_count// self.animation delay
        # becomes greater than the total number of frames in sprites, it loops back to the first frame.
        #this is why we divide on len(sprites)/ for example if animation deay is 5, and animation started 15 frames ago,
        #then 15 //5 = 3 animation cycles must be done in 15 frames. then, 3 % let's say on 6= 3 so it means current running animation is at frame 3 from the key in dict
        # if player keeps running and now there are 25 frames of running, then 25 //5 =5 , 5 % 6 =5 so it means now we show different running animation which is at frame 5 in our key
        #then , we 30 // 5 = 6 cycles repeated , and 6 %6 =0 , you see animation will start over, beginning from first frame in dict
        #thus illusion of continued running motion will be created

        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):

        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))#this is not that important.
        # we did this for rect not to be left behind or get delayed(типо отставать)from its object image/sprite
        #By updating the rect based on the sprite's position, you ensure that
        # the game object's position accurately represents its current location on the screen.(it is like that method move_ip but here we just update)
        #so let's say VISUALLY your sprite moved 5 left. However,your rect didn't get updated so that's why there is need to sync rect's position with current position of sprite

        self.mask = pygame.mask.from_surface(self.sprite)#Using this collision mask, developers can perform pixel-perfect collision detection
        # pixel collision is better than rectangle collision(it is when u check whether 2 rectangles collided).
        # if you change below width or height of instance of PLayer class( 100,100,50,50)
        #on let's say (100,100,200,200) you will see nothing got bigger or changed. image of character is same in size because rect only get bigger which is not seen.
        #we load our own images/sprites but we know they are not big so we only increase not visible rect,
        # which is why rect collision. because rects might collide but visually it won't be actually collision. that's why colliding by pixels is better
        #and mask helps us with that.


    def draw(self,win,offset_x):
        # self.sprite = self.SPRITES['idle_'+self.direction][0]#access to first frame of idle key in dict.
        #it is better to plus self.direction since now it will change animation based on where we are facing
        # instead of manually writing "idle_right" or "idle_left"which is worse

        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y))

        # pygame.draw.rect(win, self.COLOR, self.rect)#first parameter where we are drawing it, second color,third rectangle itself


#CREATING TERRAIN/BLOCKS
class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()

        self.rect = pygame.Rect(x,y,width,height)

        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        #When dealing with a sprite sheet or an image containing multiple terrain tiles or character animations combined,
        # creating separate surfaces for each individual tile or animation frame becomes essential.

        self.width = width
        self.height= height

        self.name=name

    def draw(self,win, offset_x):#surfaces are also good for putting multiple layers on top of one another, or to have several images on one surface or complex art.

        win.blit(self.image,(self.rect.x-offset_x,self.rect.y))



class Block(Object):
    def __init__(self,x,y,size):#block is like square,so we need only 1 dimension
        super().__init__(x,y,size, size)
        block = load_block(size)
        self.image.blit(block,(0,0))#we need this second surface because parents class has same variable so thus python can properly activate draw func
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height, 'fire')
        self.fire = load_sprite_sheets('Traps', 'Fire', width,height)

        self.image= self.fire['off'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = 'off'

    def on(self):
        self.animation_name='on'
    def off(self):
        self.animation_name = 'off'
    def loop(self):

        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

def get_background(name_of_color_of_background):
    image= pygame.image.load(join('assets','Background',name_of_color_of_background))#join method here is taken from os path module.
    # it is used in combination with pygame module to create correct path to a file we want to use

    #sometimes in python we use _ to show that we don't care about value/variable. for example-   a,_,c=1,2,3.
    # now we know that a is 1 and c is 3 and _ is 2 but we don't care about that. it is like we want to quickly skip smth
    _,_,width,height=image.get_rect()

    tiles=[]#we create loop below to fill screen with our background
    for i in range(WIDTH // width+1):#we add +1 so that we dont have any gaps on screen. so if for example there is some space let on screen without tiles,we add 1 to cover that too.
        for j in range(HEIGHT // height+1):# it will fill screen gradually. firstly first column ,then second and else
            pos = (i * width, j * height)#this will always change since this will denote the coordinates/position for each tile differently thus filling the screen
            #in python, objects are always drawn from top left corner
            tiles.append(pos)
    return tiles, image

def draw(window,background,bg_image,player,objects, offset_x):
    for tile in background:
        window.blit(bg_image,tile)#tile is already a tuple

    #NOTE: remember if an object is surface type, you can't iterate over it if it is single. if there are many of them, then yes
    #but if that single surface is in list like [surface], then you can iterate over single surface
    for obj in objects:
        obj.draw(window,offset_x)

    player.draw(window,offset_x)#creating character on screen
    pygame.display.update()

def handle_vertical_collision(player,objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):#this is it! that's all needed for checking if there is collision or not.
            #it is simple because our objects are from class which inherits class pygame.sprite.Sprite

            if dy > 0:#we have to handle differently how we are gonna collide when hitting top of the object and bottom of it
                player.rect.bottom = obj.rect.top#so if we hit top of object with player bottom(like character's feet) then they are going to be equal to each other(meaning collision happened)
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects
            #we make equal as to create limit like boundary. thus player won't go through objects

def collide (player, objects,dx):
    player.move(dx,0)
    player.update()
    collided_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            collided_objects = obj
            break
    player.move(-dx,0)
    player.update()
    return collided_objects

def handle_move(player,objects):#time for collision
    keys = pygame.key.get_pressed()#this gives us all keys that are being pressed on keyboard

    player.x_vel=0#we need this since in future code, if we once ,not even hold,
    # but just press left/right key, we will be moving in that direction until velocity =0 so that player doesnt move

    collide_left=collide(player,objects,-player_vel*2)
    collide_right=collide(player,objects,player_vel*2)
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(player_vel)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(player_vel)

    vertical_collide= handle_vertical_collision(player,objects,player.y_vel)
    to_check = [collide_left,collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def main_func(window): #this function will start our game

    clock =pygame.time.Clock()# DONT FORGET PARENTHESIS, IF YOU WRITE CLOCK WITHOUT(), IT WONT WORK!!
    #clock has two methods = get_fps and tick(timerate). first one shows how many fps are used , seconds uses limit of fps put by developer

    background,bg_image=get_background('Yellow.png')#tiles will be given to background variable while image to bg_image


    block_size = 96

    player= Player(100,100,50,50)

    fire = Fire(100,HEIGHT-block_size-64,16,32)
    fire.on()#activating fire

    #lets make floor of blocks
    floor= [Block(i * block_size,HEIGHT - block_size,block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    #the reason why we make range negative in first parameter and more than width of screen in second parameter
    # simply because to have blocks beyond screen in both left and right directions

    objects = [*floor, Block(0, HEIGHT - block_size*2, block_size),Block(block_size*3, HEIGHT - block_size*4, block_size),fire]#splat operator just copies all elements inside floor list to list objects. if list floor has objects, not primitive types
    #then objects will take references to those same elements, not create new ones.
    #objects list is for horizontal collision. we create blocks but horizontally

    offset_x = 0
    scroll_area_width =200

    # blocks = [Block(0,HEIGHT-block_size,block_size)]
    running = True
    while running:

        clock.tick(FPS)#sometimes without writing fps, strong computers will get very fast game.
        # so in order to regulate it, we try to limit frames per second.

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running=False
                #break
            if event.type == pygame.KEYDOWN:#the reason we don't write space key for jump in handle move function is
            # if we press space and hold,our player will continuously jump.
            # We need to jump once despite holding the key. that's why we write it here
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        player.loop(FPS)
        fire.loop()
        handle_move(player,objects)
        draw(window,background,bg_image,player,objects, offset_x)


        #scrolling background
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or(
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel<0):
            offset_x+=player.x_vel
            #if condition checks whether player's right position of x is closer to the boundary (> width - scroll area width which means if width say =800
            # then 800 -200) which gives 600 so if player's position is more than 600 which is basically close to boundary of screen(which is 800)
            # and if player moves in right direction(player.xvel>0) then offset x increases by how much you move. it counts how much distance you made so that scrolling background won't be continuous
            #thus when specific offset x limit is reached, scroll of background is stopped.
            #same for left side

    pygame.quit()#we need this for cleaning up after terminating the programm. without this, it will still be ok since python will automatically clean for us
    # quit()

if __name__ == '__main__':#this will check that we will start game only if this file is run directly but not from other files
    main_func(window)

#1)ADDING GRAVITY

#2)loading sprite sheets!









































#IDEAS -let the user put their custom background picture
#dont forget about player self.count variable in hit head function. it might be useless


#if smth doesnt work.change fall count in hit head func to self.count