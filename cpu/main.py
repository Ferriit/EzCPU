import pygame as pg
import sys
import ROM_Emulator as ROMe
from cpu import regs

# Make sure execution is paused when the window is created
ROMe.OPCODES.HALTFLAG = True

pg.init()

WIDTH, HEIGHT = 800, 600

ctx = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("EzCPU sim (FMBYAS)")

class register:
    def __init__(self, value: str, x: int, y: int, size: int, name: str, fontLength: int):
        self.value = value
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        self.fontLength = fontLength

        self.font = pg.font.SysFont("Consolas", self.size)
    
    def render(self):
        for i in range(len(self.value)):
            color = (255, 255, 255) if self.value[i] == "1" else (0, 0, 0)
            pg.draw.rect(ctx, color, (self.x + i * self.size, self.y, self.size, self.size))

            textSurface = self.font.render(self.name, True, (255, 255, 255))
            ctx.blit(textSurface, (self.x - self.fontLength, self.y))

            pg.draw.line(ctx, (255, 255, 255), (self.x - self.fontLength, self.y), (WIDTH, self.y))
            pg.draw.line(ctx, (255, 255, 255), (self.x - self.fontLength, self.y + self.size), (WIDTH, self.y + self.size))

registers = {}

windowFont = pg.font.SysFont("Consolas", 20)

run = True
while run:    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                ROMe.OPCODES.HALTFLAG = False

    ctx.fill((0, 0, 0))

    for i in range(len(list(regs.keys()))):
        registers[list(regs.keys())[i]] = register(regs[list(regs.keys())[i]], WIDTH - 160, i * 15, 10, list(regs.keys())[i], 55)
        registers[list(regs.keys())[i]].render()

    if ROMe.OPCODES.freezecycles > 0:
        ROMe.OPCODES.freezecycles -= 1

    elif not ROMe.OPCODES.HALTFLAG and int(ROMe.internal_pc, 2) < len(ROMe.bytecode):
        ROMe.stepInstruction()

    elif int(ROMe.internal_pc, 2) < len(ROMe.bytecode):
        # Display HALT message
        textSurface = windowFont.render(
            "HALTED! PRESS [C] TO CONTINUE EXECUTION", True, (255, 255, 255)
        )
        ctx.blit(textSurface, (5, HEIGHT - 25))
    
    else:
        # Display STOPPED message
        textSurface = windowFont.render(
            "PROGRAM RAN SUCCESSFULLY", True, (255, 255, 255)
        )
        ctx.blit(textSurface, (5, HEIGHT - 25))
    

    pg.display.flip()