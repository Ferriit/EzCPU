import os
import pygame as pg
import assembler as asm
import ROM_Emulator as ROMe
from cpu import regs, memry, stack
from ROM_Emulator import OPCODES, stepInstruction

pg.init()
OPCODES.HALTFLAG = True

windowFont = pg.font.SysFont("Consolas", 20)
WIDTH, HEIGHT = 1200, 800
ctx = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("EzCPU Simulator")

FONT = pg.font.SysFont("Consolas", 20)
SMALL_FONT = pg.font.SysFont("Consolas", 14)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
GRAY = (50, 50, 50)
BLUE = (0, 100, 255)

CELL_WIDTH, CELL_HEIGHT = 32, 24
MEM_ROWS, MEM_COLS = 16, 16
STACK_ROWS = 16

tests_path = os.path.join(os.path.dirname(__file__), "..", "tests")
asm_files = [f for f in os.listdir(tests_path) if f.endswith(".asm")]

if not asm_files:
    print("No .asm files found in tests/")
    exit(1)


def select_program():
    selected = None
    while selected is None:
        ctx.fill(BLACK)
        ctx.blit(FONT.render("Select a program to run:", True, WHITE), (50, 30))

        for i, f in enumerate(asm_files):
            ctx.blit(FONT.render(f"{i + 1}. {f}", True, WHITE), (50, 80 + i * 30))

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
    return os.path.join(tests_path, selected)


def render_memory(scroll_offset):
    start = scroll_offset * MEM_COLS
    for row in range(MEM_ROWS):
        for col in range(MEM_COLS):
            idx = start + row * MEM_COLS + col
            if idx >= len(memry):
                break
            val = memry[idx]
            rect = pg.Rect(300 + col * CELL_WIDTH, 50 + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            color = RED if idx == int(regs["pc"], 2) else GREEN
            pg.draw.rect(ctx, color, rect)
            pg.draw.rect(ctx, WHITE, rect, 1)
            ctx.blit(SMALL_FONT.render(f"{val}", True, WHITE), (300 + col * CELL_WIDTH + 4, 50 + row * CELL_HEIGHT + 2))


def render_stack():
    top_items = stack[-STACK_ROWS:]
    for i, val in enumerate(reversed(top_items)):
        y = 50 + i * CELL_HEIGHT
        ctx.blit(FONT.render(f"{val}", True, YELLOW), (50, y))
        ctx.blit(FONT.render(f"({int(val, 2)})", True, WHITE), (50 + 16*10 + 10, y))



def render_registers():
    max_rows = (HEIGHT - 100) // CELL_HEIGHT
    for i, (name, val) in enumerate(regs.items()):
        if i >= max_rows:
            break
        rect = pg.Rect(750, 50 + i * CELL_HEIGHT, CELL_WIDTH * 6, CELL_HEIGHT)
        pg.draw.rect(ctx, GRAY, rect)
        pg.draw.rect(ctx, WHITE, rect, 1)
        display_val = val if isinstance(val, str) else format(val, "016b")
        ctx.blit(FONT.render(f"{name}: {display_val} ({int(display_val,2)})", True, WHITE), (754, 50 + i * CELL_HEIGHT + 2))

def render_status():
    pc_int = int(regs["pc"],2)

    if OPCODES.HALTFLAG:
        text = "HALTED! Press [C] or [SPACE] to continue..."

    elif OPCODES.freezecycles > 0:
        text = f"PROGRAM WAITING - PC={pc_int} (cycles left: {OPCODES.freezecycles})"
        OPCODES.freezecycles -= 1

    elif not ROMe.OPCODES.HALTFLAG and int(regs["pc"], 2) < len(ROMe.bytecode):
        text = f"PROGRAM RUNNING - PC={pc_int}"
        stepInstruction()
    else:
        text = "PROGRAM RAN SUCCESSFULLY"

    ctx.blit(FONT.render(text, True, BLUE), (50, HEIGHT - 50))


def main():
    program_file = select_program()
    bytecode = asm.assemble([program_file])

    import ROM_Emulator as ROMe
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
                if event.key == pg.K_c or event.key == pg.K_SPACE:
                    if OPCODES.HALTFLAG:
                        OPCODES.HALTFLAG = False
                    elif OPCODES.HALTFLAG == False:
                        OPCODES.HALTFLAG = True

        render_memory(scroll_offset)
        render_stack()
        render_registers()
        render_status()

        pg.display.flip()
        clock.tick(15)

    pg.quit()


if __name__ == "__main__":
    main()
