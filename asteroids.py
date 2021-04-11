"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random


# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_DRAW_RADIUS = 3

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
SHIP_MAX_SPEED = 10

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

#Load all of the images:
ship_image = "images/playerShip1_orange.png"
ship = arcade.load_texture(ship_image)

laser_image = "images/laserBlue01.png"
laser = arcade.load_texture(laser_image)

Large_Asteroid_image = "images/meteorGrey_big1.png"
Large_Asteroid = arcade.load_texture(Large_Asteroid_image)

Medium_Asteroid_image = "images/meteorGrey_med1.png"
Medium_Asteroid = arcade.load_texture(Medium_Asteroid_image)

Small_Asteroid_image = "images/meteorGrey_small1.png"
Small_Asteroid = arcade.load_texture(Small_Asteroid_image)

Lost_image = "images/lost.png"
Lost = arcade.load_texture(Lost_image)

Win_image = "images/win.jpg"
Win = arcade.load_texture(Win_image)



class Point:
    """
    point has an x and a y
    """
    def __init__(self):
        self.x=0
        self.y=0
        
class Velocity:
    """
    speed has a horizontal and vertical factor
    """
    def __init__(self):
        self.dx=0
        self.dy=0
        
class Picture:
    """
    this will be a class for the objects with an image
    """
    def __init__(self,name="",width=0,height=0):
        self.name=name
        self.width=width
        self.height=height
        
class Flying_object:
    """
    base class that is used for bullet and target class.
    """   
    def __init__(self):
        self.center=Point()
        self.velocity=Velocity()
        self.radius=0
        self.angle=0
        self.picture=Picture()
        self.alive=True

    def advance (self):
        """
        adds velocity to x and y and wraps all elements
        """
        if self.center.x>=(SCREEN_WIDTH-self.radius/2):
            self.center.x=SHIP_RADIUS
        elif self.center.x<=(self.radius/2):
            self.center.x=SCREEN_WIDTH-self.radius
        else:
            self.center.x+=self.velocity.dx
        
        if self.center.y>=(SCREEN_HEIGHT-self.radius/2):
            self.center.y=SHIP_RADIUS
        elif self.center.y<=(self.radius/2):
            self.center.y=SCREEN_HEIGHT-self.radius
        else:
            self.center.y+=self.velocity.dy
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.picture.width, self.picture.height, self.picture.name, self.angle, 255)

class Ship(Flying_object):
    """
    the class for the flying ship
    """
    def __init__(self):
        super().__init__()
        self.radius=SHIP_RADIUS
        self.picture.name=ship
        self.spin=SHIP_TURN_AMOUNT
        self.center.x=SCREEN_WIDTH/2
        self.center.y=SCREEN_HEIGHT/2
        self.picture.width=75
        self.picture.height=99
        self.angle_changed=False
    
    def rotate_ship(self,amount):
        """
        rotates the ship when asked
        """
        self.angle+=amount
        self.angle_changed=True
    
    def change_speed(self):
        """
        The up arrow will increase the velocity in the direction the ship is pointed by 0.25 pixels/frame.
        """
        powered=self.velocity.dx*self.velocity.dx+self.velocity.dy*self.velocity.dy
        #Here I make sure that if you go in one only direction, the speed can't surpass the max
        if math.sqrt(powered)<SHIP_MAX_SPEED:
            self.velocity.dx+=math.cos(math.radians(self.angle))*SHIP_THRUST_AMOUNT
            self.velocity.dy+=math.sin(math.radians(self.angle))*SHIP_THRUST_AMOUNT
        
        #but if you changed directions, you can change the speed. This sometimes makes it go too fast, but luckily
        #you will have changed angle enough
        elif self.angle_changed:
            self.velocity.dx+=math.cos(math.radians(self.angle))*SHIP_THRUST_AMOUNT
            self.velocity.dx=self.velocity.dx*9/10
            self.velocity.dy+=math.sin(math.radians(self.angle))*SHIP_THRUST_AMOUNT
            self.velocity.dy=self.velocity.dy*9/10
            self.angle_changed=False
         
        
class Bullet(Flying_object):
    """
    Inherits from Flying_object. Has a radius, draws and fires.
    """  
    def __init__(self):
        super().__init__()
        self.radius=BULLET_RADIUS
        self.life=BULLET_LIFE        
        
    def draw (self):
        """
        Draws the bullet
        """
        arcade.draw_circle_filled(self.center.x,self.center.y,BULLET_DRAW_RADIUS,arcade.color.WHITE)
    

    def fire(self,point,velocity,angle):
        """
        Positions the bullet in the right place and initializes the speed depending on the angle of the rifle
        """
        #I copy the details of the ship and I add the bullets speed
        self.center.x=point.x
        self.center.y=point.y
        self.angle=angle
        self.velocity.dx=velocity.dx
        self.velocity.dy=velocity.dy
        self.velocity.dx+=math.cos(math.radians(angle))*BULLET_SPEED
        self.velocity.dy+=math.sin(math.radians(angle))*BULLET_SPEED
    
    def advance(self):
        """
        wraps the ship
        """
        super().advance()
        self.life-=1
        if self.life<=0:
            self.alive=False
              

class Large(Flying_object):
    """
    Inherits from Flying_Object. Has #of hits and method hit
    """    
    def __init__(self):
        super().__init__()
        self.center.x=random.uniform(self.radius/2+1,SCREEN_WIDTH)
        self.center.y=random.uniform(0,SCREEN_HEIGHT)
        self.angle=random.uniform(0,360)
        self.velocity.dx=math.cos(math.radians(self.angle))*BIG_ROCK_SPEED
        self.velocity.dy=math.sin(math.radians(self.angle))*BIG_ROCK_SPEED
        self.picture.name=Large_Asteroid
        self.radius=BIG_ROCK_RADIUS
        self.spin=BIG_ROCK_SPIN
        self.picture.width=101
        self.picture.height=88
    
    def Has_been_hit (self,list):
        """
        modifies the status self.alive if the target can be hit only one more time and discounts one hit
        returns true if the asteroid has to be removed
        """
        medium1=Medium(self.center.x,self.center.y,self.velocity.dx,self.velocity.dy+2,self.angle)
       
        medium2=Medium(self.center.x,self.center.y,self.velocity.dx,self.velocity.dy-2,self.angle)
        
        small=Small(self.center.x,self.center.y,self.velocity.dx+5,self.velocity.dy,self.angle)       
        
        list.extend([medium1,medium2,small])
    
        self.alive=False
    
    def advance(self):
        """
        rotates the object and wraps it
        """
        super().advance()
        self.angle+=self.spin
        

class Medium(Flying_object):
    """
    Inherits from Flying_Object. Has #of hits and method hit
    """    
    def __init__(self,x,y,dx,dy,angle):
        super().__init__()
        self.picture.name=Medium_Asteroid
        self.radius=MEDIUM_ROCK_RADIUS
        self.spin=MEDIUM_ROCK_SPIN
        self.picture.width=43
        self.picture.height=43
        self.center.x=x
        self.center.y=y
        self.angle=angle
        self.velocity.dx=dx
        self.velocity.dy=dy
        
    
    def Has_been_hit (self,list):
        """
        modifies the status self.alive if the target can be hit only one more time and discounts one hit
        
        """
        small1=Small(self.center.x,self.center.y,self.velocity.dx+1.5,self.velocity.dy+1.5,self.angle)
        
        small=Small(self.center.x,self.center.y,self.velocity.dx-1.5,self.velocity.dy-1.5,self.angle)
   
        list.extend([small,small1])

        self.alive=False
        
    def advance(self):
        """
        rotates the object and wraps it
        """
        super().advance()
        self.angle+=self.spin
        if self.center.x>=(SCREEN_WIDTH-self.radius):
            self.center.x=self.radius

class Small(Flying_object):
    """
    Inherits from Flying_Object. Has #of hits and method hit
    """    
    def __init__(self,x,y,dx,dy,angle):
        super().__init__()
        self.picture.name=Small_Asteroid
        self.radius=SMALL_ROCK_RADIUS
        self.spin=SMALL_ROCK_SPIN
        self.picture.width=28
        self.picture.height=28
        self.center.x=x
        self.center.y=y
        self.angle=angle
        self.velocity.dx=dx
        self.velocity.dy=dy
    
    def Has_been_hit (self,list):
        """
        modifies the status self.alive if the target can be hit only one more time and discounts one hit
        
        """
        self.alive=False
        
    def advance(self):
        """
        rotates the object and wraps it
        """
        super().advance()
        self.angle+=self.spin

def revive(ship,asteroids):
    #I restart the ship
    ship.alive=True
    ship.picture.width=75
    ship.picture.height=99
    ship.center.x=SCREEN_WIDTH/2
    ship.center.y=SCREEN_HEIGHT/2
    ship.angle_changed=False
    ship.angle=0
    ship.velocity.dx=0
    ship.velocity.dy=0
    #I draw the asteroids again
    while len(asteroids)<(INITIAL_ROCK_COUNT):
        asteroid=Large()
        asteroids.append(asteroid)
    
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """
    
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        #I'll keep a list of asteroids and bullets on screen
        self.asteroids=[]
        self.bullets=[]
        
        for i in range(INITIAL_ROCK_COUNT):
            asteroid=Large()
            self.asteroids.append(asteroid)
       
        #my cute ship:
        self.ship=Ship()
        
        self.won=False 

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # TODO: draw each object
        self.ship.draw()
        
        for asteroid in self.asteroids:
            asteroid.draw()
        
        for bullet in self.bullets:
            bullet.draw()



    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        
        if self.ship.alive:
            # clear the screen to begin drawing
            #Check if you won and set the boolean to true
            arcade.start_render()
            if len(self.asteroids)==0:
                self.ship.alive=False
                self.won=True
                             
            #You play
            else:
                self.check_keys()

                # TODO: Tell everything to advance or move forward one step in time
                self.ship.advance()
                
                for asteroid in self.asteroids:
                    if asteroid.alive==False:
                        self.asteroids.remove(asteroid)
                    else:
                        asteroid.advance()
                        
                for bullet in self.bullets:
                    if bullet.alive==False:
                        self.bullets.remove(bullet)
                    else:
                        bullet.advance()
                        
                # TODO: Check for collisions
                #this was a pain because as I add elements to the asteroid list, I had to use indexes.
                #It checks if a bullet has destroyed an asteroid. 
                for b in range(len(self.asteroids)):
                    for a in range(len(self.bullets)):
                        x=self.bullets[a].center.x-self.asteroids[b].center.x
                        y=self.bullets[a].center.y-self.asteroids[b].center.y
                        h=self.bullets[a].radius+self.asteroids[b].radius
                        #I verify that the bullet is alive because I don't remove dead bullets until later in update.
                        if math.sqrt(x*x+y*y)<=h and self.bullets[a].alive:
                            self.bullets[a].alive=False
                            self.asteroids[b].Has_been_hit(self.asteroids)
                
                
                #Now let's check if our ship was hit:
                for asteroid in self.asteroids:
                    x=self.ship.center.x-asteroid.center.x
                    y=self.ship.center.y-asteroid.center.y
                    h=self.ship.radius+asteroid.radius
                    if math.sqrt(x*x+y*y)<=h:
                        self.ship.alive=False
                        
        else:
            # clear the screen to begin drawing
            arcade.start_render()
            #Banner for winning 
            if self.won:
                arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 626, 417, Win, 0, 255)
            else:
                #Banner for Losing
                arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 216*2, 233*2, Lost, 0, 255)
            #I remove everything else from screen
            for asteroid in self.asteroids:
                self.asteroids.remove(asteroid)
            for bullet in self.bullets:
                self.bullets.remove(bullet)
            #And I hide the ship
            self.ship.picture.width=0
            self.ship.picture.height=0
    
            arcade.draw_text("If you want to play again, press Y", 0, 0, arcade.color.WHITE,25)
            self.check_keys()
        

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.SPACE in self.held_keys:
            bullet=Bullet()
            velocity=self.ship.velocity
            bullet.fire(self.ship.center,velocity,self.ship.angle)
            self.bullets.append(bullet)    

        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_ship(SHIP_TURN_AMOUNT)

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_ship(-SHIP_TURN_AMOUNT)

        if arcade.key.UP in self.held_keys:
            self.ship.change_speed()

        if arcade.key.DOWN in self.held_keys:
            #this key does nothing because the assignment said nothing about it.
            pass
        
        
        if arcade.key.Y in self.held_keys:
            if self.ship.alive==False:
                revive(self.ship,self.asteroids)
                self.won=False

      #  """
        
      #  """
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        self.held_keys.add(key)

       

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()