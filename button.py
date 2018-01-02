import pygame.ftfont

class Button():

    def __init__(self, ai_settings, screen, msg):
        '''Initializes attributes'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Sets dimensions of button
        self.width, self.height = 250,75
        self.button_color = (0, 255, 0)
        self.text_color = (255,255,255)
        self.font = pygame.ftfont._SysFont(None, 48)

        #Builds rect and centers
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Message
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''Turns message into image'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draws button with message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)