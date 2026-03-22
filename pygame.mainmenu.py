import pygame
import random

pygame.init()

input_text = ""
inputing = False
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Projects")
font = pygame.font.Font(None,50)
clock = pygame.time.Clock()

# program state
state = "menu"
running = True

# title typing
Text = "Nabil's Python Projects"
displayed_letters = []
index = 0
letter_delay = 100
last_update = pygame.time.get_ticks()

# line animation
line_length = 0
max_line_length = 550
line_speed = 2

# menu
options = {
    "Todo List": (0,255,0),
    "Guessing Game": (0,0,255),
    "Calculator": (255,0,255),
    "Password Gen": (255,255,0),
    "Password Gen With Words": (0,255,255),
    "Quit": (255,0,0)
}

options_list = list(options.items())
selected = 0
selector_x = 25


while running:

    screen.fill((123,166,180))
    now = pygame.time.get_ticks()

    # events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == "menu" and line_length >= max_line_length:

                if event.key == pygame.K_UP:
                    selected = max(0, selected-1)

                if event.key == pygame.K_DOWN:
                    selected = min(len(options_list)-1, selected+1)

                if event.key == pygame.K_RETURN:


                    if selected == 0:
                        state = "todo"

                    elif selected == 1:
                        state = "guess"

                    elif selected == 2:
                        state = "calc"

                    elif selected == 3:
                        state = "pass"

                    elif selected == 4:
                        state = "pass_words"

                    elif selected == 5:
                        running = False

            # ESC always returns to menu
            if event.key == pygame.K_ESCAPE:
                state = "menu"
            if inputing == True:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]

                    elif event.key == pygame.K_RETURN:
                        print("User typed:", input_text)

                    else:
                        input_text += event.unicode


    # ================= MENU =================
    if state == "menu":

        # type title
        if index < len(Text) and now - last_update > letter_delay:

            char = Text[index]

            if index < 7:
                color = (255,255,255)
            else:
                color = random.choice([
                    (255,0,0),(0,255,0),(0,0,255),
                    (255,255,0),(255,0,255),(0,255,255)
                ])

            displayed_letters.append((char,color))
            index += 1
            last_update = now


        # draw title
        x = 50
        y = 50

        for char,color in displayed_letters:

            surf = font.render(char,True,color)
            screen.blit(surf,(x,y))
            x += surf.get_width()


        # animate lines
        if index == len(Text) and line_length < max_line_length:
            line_length += line_speed

        if line_length > 0:

            pygame.draw.line(screen,(255,255,255),(50,90),(50+line_length,90),3)
            pygame.draw.line(screen,(255,255,255),(75,100),(75+line_length-50,100),3)


        # menu options
        if line_length >= max_line_length:

            for i,(text,color) in enumerate(options_list):

                option = font.render(text,True,color)
                screen.blit(option,(50,150+i*50))


            selector_y = 150 + selected*50
            selector_color = options_list[selected][1]

            arrow = font.render(">",True,selector_color)
            screen.blit(arrow,(selector_x,selector_y))


    # ================= PLACEHOLDER SCREENS =================

    elif state == "todo":

        text = font.render("Todo List (ESC to return)",True,(255,255,255))
        screen.blit(text,(150,10))

    elif state == "guess":

        text = font.render("Guessing Game (ESC to return)",True,(255,255,255))
        screen.blit(text,(150,10))

    elif state == "calc":

        text = font.render("Calculator (ESC to return)",True,(255,255,255))
        screen.blit(text,(150,10))

    elif state == "pass":

        text = font.render("Password Generator",True,(255,255,255))
        screen.blit(text,(150,10))
        chars = {
        "symbols":["!","£","$","%","^","&","*","(",")"],
        "letters":["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
        "numbers":["0","1","2","3","4","5","6","7","8","9"]
        }
        all_chars = chars["symbols"]+chars["letters"]+chars["numbers"]
        while True:
            try:
                print("something")
                break
            except():
                print("nothin")


    elif state == "pass_words":

        text = font.render("Password Generator Words",True,(255,255,255))
        screen.blit(text,(150,10))


    pygame.display.update()
    clock.tick(60)

pygame.quit()