regs = {
    **{f"r{i}": "0" * 16 for i in range(16)},
    "funcret": "0" * 16,
    "cmpreg": "000",
    "pc": "0" * 16,
    "stackptr": "0" * 16,
    "dbg": "0" * 16,
    **{f"io{i}": "0" * 16 for i in range(8)},
    "intreg": "0" * 16
}

memry = [0] * 4096

stack = []