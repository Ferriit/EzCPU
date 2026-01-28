import os
import pygame as pg
import assembler as asm
from utils import log, LOG_LINES
import EzCPU_ROM as ROMe
from cpu import regs, memry, stack
from EzCPU_ROM import OPCODES, stepInstruction

pg.init()
OPCODES.HALTFLAG = True

info = pg.display.Info()
WIDTH, HEIGHT = info.current_w - 100, info.current_h - 100
ctx = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("EzCPU Simulator")

FONT = pg.font.SysFont("Consolas", 20)
SMALL_FONT = pg.font.SysFont("Consolas", 14)

# Fucking colors
BLACK = (15, 15, 15)
WHITE = (240, 240, 240)
GREEN = (0, 200, 0)
YELLOW = (255, 220, 0)
RED = (255, 80, 80)
GRAY = (50, 50, 50)
BLUE = (0, 160, 255)
DARK_BLUE = (10, 10, 50)

CELL_WIDTH = max(32, WIDTH // 50)
CELL_HEIGHT = max(24, HEIGHT // 35)
MEM_COLS = 16
MEM_ROWS = min(16, (HEIGHT - 250) // CELL_HEIGHT)
STACK_ROWS = min(10, (HEIGHT - 300) // CELL_HEIGHT)
LOG_ROWS = 6

# GET YO FILE BRUH
tests_path = os.path.join(os.path.dirname(__file__), "..", "tests")
asm_files = [f for f in os.listdir(tests_path) if f.endswith(".asm")]
if not asm_files:
    print("No .asm files found in tests/")
    exit(1)

# IM SELECTIN ITTTTT
def select_program():
    selected = None
    while selected is None:
        ctx.fill(DARK_BLUE)
        ctx.blit(FONT.render("Select a program to run:", True, WHITE), (50, 30))
        file_rects = []
        for i, f in enumerate(asm_files):
            y = 80 + i * 30
            surf = FONT.render(f"{i+1}. {f}", True, WHITE)
            ctx.blit(surf, (50, y))
            file_rects.append((pg.Rect(50, y, surf.get_width(), surf.get_height()), f))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if pg.K_1 <= event.key <= pg.K_9:
                    idx = event.key - pg.K_1
                    if idx < len(asm_files):
                        selected = asm_files[idx]
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for rect, fname in file_rects:
                    if rect.collidepoint(mx, my):
                        selected = fname
    return os.path.join(tests_path, selected)

def render_memory(scroll_offset):
    start = scroll_offset * MEM_COLS
    mem_x, mem_y = WIDTH // 3, 50
    for row in range(MEM_ROWS):
        for col in range(MEM_COLS):
            idx = start + row * MEM_COLS + col
            if idx >= len(memry):
                break
            val = memry[idx]
            rect = pg.Rect(mem_x + col * CELL_WIDTH, mem_y + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            color = RED if idx == int(regs["pc"], 2) else GREEN
            pg.draw.rect(ctx, color, rect)
            pg.draw.rect(ctx, WHITE, rect, 1)
            ctx.blit(SMALL_FONT.render(f"{val}", True, WHITE), (rect.x + 4, rect.y + 2))
    ctx.blit(FONT.render("Memory", True, BLUE), (mem_x, mem_y - 30))

def render_stack():
    stack_x, stack_y = 50, 50
    top_items = stack[-STACK_ROWS:]
    for i, val in enumerate(reversed(top_items)):
        y = stack_y + i * CELL_HEIGHT
        ctx.blit(FONT.render(f"{val}", True, YELLOW), (stack_x, y))
        ctx.blit(FONT.render(f"({int(val,2)})", True, WHITE), (stack_x + 200, y))
    ctx.blit(FONT.render("Stack (Top)", True, BLUE), (stack_x, stack_y - 30))

def render_registers():
    reg_x, reg_y = WIDTH - 400, 50
    max_rows = (HEIGHT - 100) // CELL_HEIGHT
    for i, (name, val) in enumerate(regs.items()):
        if i >= max_rows:
            break
        rect = pg.Rect(reg_x, reg_y + i * CELL_HEIGHT, 350, CELL_HEIGHT)
        pg.draw.rect(ctx, GRAY, rect)
        pg.draw.rect(ctx, WHITE, rect, 1)
        display_val = val if isinstance(val, str) else format(val, "016b")
        ctx.blit(FONT.render(f"{name}: {display_val} ({int(display_val,2)})", True, WHITE), (rect.x + 4, rect.y + 2))
    ctx.blit(FONT.render("Registers", True, BLUE), (reg_x, reg_y - 30))

STATUS_HEIGHT = CELL_HEIGHT + 10

def render_status():
    pc_int = int(regs["pc"], 2)
    status_y = HEIGHT - STATUS_HEIGHT

    if OPCODES.HALTFLAG:
        if pc_int >= len(ROMe.bytecode):
            text = "PROGRAM RAN SUCCESSFULLY"
        else:
            text = "HALTED! Press [C] or [SPACE] to continue..."
    elif OPCODES.freezecycles > 0:
        text = f"PROGRAM WAITING - PC={pc_int} (cycles left: {OPCODES.freezecycles})"
        OPCODES.freezecycles -= 1
    elif pc_int < len(ROMe.bytecode):
        stepInstruction()
        text = f"PROGRAM RUNNING - PC={pc_int}"
    elif not OPCODES.HALTFLAG and int(regs["pc"], 2) < len(ROMe.bytecode):
        stepInstruction()
        pc_int = int(regs["pc"], 2)
        text = f"PROGRAM RUNNING - PC={pc_int:04X}"
    else:
        text = "PROGRAM RAN SUCCESSFULLY"
        OPCODES.HALTFLAG = True 

    status_rect = pg.Rect(0, status_y, WIDTH, STATUS_HEIGHT)
    pg.draw.rect(ctx, DARK_BLUE, status_rect)
    pg.draw.rect(ctx, WHITE, status_rect, 2)
    ctx.blit(FONT.render(text, True, BLUE), (10, status_y + 2))

def render_log():
    log_height = LOG_ROWS * CELL_HEIGHT + 10
    log_x = 50
    log_y = HEIGHT - STATUS_HEIGHT - log_height - 10
    log_rect = pg.Rect(log_x-10, log_y-5, WIDTH//3+20, log_height)
    pg.draw.rect(ctx, DARK_BLUE, log_rect)
    pg.draw.rect(ctx, WHITE, log_rect, 2)
    start_line = max(0, len(LOG_LINES) - LOG_ROWS)
    for i, line in enumerate(LOG_LINES[start_line:]):
        ctx.blit(SMALL_FONT.render(line, True, WHITE), (log_x, log_y + i*CELL_HEIGHT))
    ctx.blit(FONT.render("Log", True, BLUE), (log_x, log_y - 25))

def main():
    program_file = select_program()
    bytecode = asm.assemble([program_file])
    ROMe.bytecode = bytecode
    ROMe.regs["pc"] = format(0, "016b")
    clock = pg.time.Clock()
    scroll_offset = 0
    running = True

    while running:
        ctx.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_c, pg.K_SPACE]:
                    OPCODES.HALTFLAG = not OPCODES.HALTFLAG

        render_memory(scroll_offset)
        render_stack()
        render_registers()
        render_status()
        render_log()

        pg.display.flip()
        clock.tick(15)

    pg.quit()


if __name__ == "__main__":
    main()