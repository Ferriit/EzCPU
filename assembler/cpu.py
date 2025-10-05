regs = {
    **{f"r{i}": "0" * 16 for i in range(15)},
    "funcret": "0" * 16,
    "cmpreg": "000",
    "pc": "0" * 16,
    "stackptr": "0" * 16,
    "dbg": "0" * 16,
    **{f"io{i}": "0" * 16 for i in range(4)}
}

memry = [0] * 512

stack = []