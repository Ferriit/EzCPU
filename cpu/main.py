import os
import pygame as pg
import assembler as asm
import ROM_Emulator as ROMe
from cpu import regs, memry, stack
from ROM_Emulator import OPCODES, stepInstruction

pg.init()
pg.display.set_caption("EzCPU Simulator")

VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1200, 800
VIRTUAL_SURF = pg.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

WINDOW = pg.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

FONT = pg.font.SysFont("Consolas", 20)
SMALL_FONT = pg.font.SysFont("Consolas", 14)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (255, 60, 60)
YELLOW = (255, 220, 0)
GRAY = (50, 50, 50)
BLUE = (0, 150, 255)
DARK_BLUE = (20, 20, 60)

CELL_WIDTH, CELL_HEIGHT = 32, 24
MEM_ROWS, MEM_COLS = 16, 16
STACK_ROWS = 16

tests_path = os.path.join(os.path.dirname(__file__), "..", "tests")
asm_files = [f for f in os.listdir(tests_path) if f.endswith(".asm")]

if not asm_files:
    print("No .asm files found in tests/")
    exit(1)

def select_program():
    global WINDOW
    selected = None
    while selected is None:
        VIRTUAL_SURF.fill(BLACK)
        VIRTUAL_SURF.blit(FONT.render("Select a program to run:", True, WHITE), (50, 30))

        for i, f in enumerate(asm_files):
            VIRTUAL_SURF.blit(FONT.render(f"{i + 1}. {f}", True, WHITE), (50, 80 + i * 30))

        win_w, win_h = WINDOW.get_size()
        scale = min(win_w / VIRTUAL_WIDTH, win_h / VIRTUAL_HEIGHT)
        scaled_surf = pg.transform.smoothscale(VIRTUAL_SURF, (int(VIRTUAL_WIDTH * scale), int(VIRTUAL_HEIGHT * scale)))
        x_offset = (win_w - int(VIRTUAL_WIDTH * scale)) // 2
        y_offset = (win_h - int(VIRTUAL_HEIGHT * scale)) // 2
        WINDOW.fill(BLACK)
        WINDOW.blit(scaled_surf, (x_offset, y_offset))
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
            elif event.type == pg.VIDEORESIZE:
                WINDOW = pg.display.set_mode(event.size, pg.RESIZABLE)

    return os.path.join(tests_path, selected)

def render_memory(scroll_offset=0):
    start = scroll_offset * MEM_COLS
    for row in range(MEM_ROWS):
        for col in range(MEM_COLS):
            idx = start + row * MEM_COLS + col
            if idx >= len(memry):
                break
            val = memry[idx]
            x, y = 300 + col * CELL_WIDTH, 50 + row * CELL_HEIGHT
            rect = pg.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
            color = RED if idx == int(regs["pc"], 2) else GREEN
            pg.draw.rect(VIRTUAL_SURF, color, rect)
            pg.draw.rect(VIRTUAL_SURF, WHITE, rect, 1)
            VIRTUAL_SURF.blit(SMALL_FONT.render(f"{val}", True, WHITE), (x + 4, y + 2))

def render_stack():
    top_items = stack[-STACK_ROWS:]
    for i, val in enumerate(reversed(top_items)):
        y = 50 + i * CELL_HEIGHT
        VIRTUAL_SURF.blit(FONT.render(f"{val}", True, YELLOW), (50, y))
        VIRTUAL_SURF.blit(FONT.render(f"({int(val, 2)})", True, WHITE), (50 + 100, y))

def render_registers():
    max_rows = (VIRTUAL_HEIGHT - 100) // CELL_HEIGHT
    for i, (name, val) in enumerate(regs.items()):
        if i >= max_rows:
            break
        rect = pg.Rect(750, 50 + i * CELL_HEIGHT, CELL_WIDTH * 6, CELL_HEIGHT)
        pg.draw.rect(VIRTUAL_SURF, GRAY, rect)
        pg.draw.rect(VIRTUAL_SURF, WHITE, rect, 1)
        display_val = val if isinstance(val, str) else format(val, "016b")
        VIRTUAL_SURF.blit(FONT.render(f"{name}: {display_val} ({int(display_val,2)})", True, WHITE), (754, 50 + i * CELL_HEIGHT + 2))

def render_status():
    pc_int = int(regs["pc"],2)
    if OPCODES.HALTFLAG:
        text = "HALTED! Press [C] or [SPACE] to continue..."
    elif OPCODES.freezecycles > 0:
        text = f"PROGRAM WAITING - PC={pc_int} (cycles left: {OPCODES.freezecycles})"
        OPCODES.freezecycles -= 1
    elif not OPCODES.HALTFLAG and int(regs["pc"], 2) < len(ROMe.bytecode):
        text = f"PROGRAM RUNNING - PC={pc_int}"
        stepInstruction()
    else:
        text = "PROGRAM RAN SUCCESSFULLY"
    VIRTUAL_SURF.blit(FONT.render(text, True, BLUE), (50, VIRTUAL_HEIGHT - 50))


def main():
    global WINDOW

    program_file = select_program()
    bytecode = asm.assemble([program_file])

    ROMe.bytecode = bytecode
    ROMe.regs["pc"] = format(0, "016b")
    OPCODES.HALTFLAG = True

    scroll_offset = 0
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_c, pg.K_SPACE):
                    OPCODES.HALTFLAG = not OPCODES.HALTFLAG
            elif event.type == pg.VIDEORESIZE:
                WINDOW = pg.display.set_mode(event.size, pg.RESIZABLE)

        VIRTUAL_SURF.fill(DARK_BLUE)

        render_memory(scroll_offset)
        render_stack()
        render_registers()
        render_status()
        
        win_w, win_h = WINDOW.get_size()
        scale = min(win_w / VIRTUAL_WIDTH, win_h / VIRTUAL_HEIGHT)
        scaled_w = int(VIRTUAL_WIDTH * scale)
        scaled_h = int(VIRTUAL_HEIGHT * scale)
        x_offset = (win_w - scaled_w) // 2
        y_offset = (win_h - scaled_h) // 2
        scaled_surf = pg.transform.smoothscale(VIRTUAL_SURF, (scaled_w, scaled_h))
        WINDOW.fill(BLACK)
        WINDOW.blit(scaled_surf, (x_offset, y_offset))

        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == "__main__":
    main()