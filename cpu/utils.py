LOG_LINES = []

def log(msg):
    LOG_LINES.append(msg)
    if len(LOG_LINES) > 100:
        LOG_LINES.pop(0)