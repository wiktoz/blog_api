def is_valid_length(password: str):
    return True if (len(password)>8 and len(password) <= 64) else False

def contains_pii(password: str, data: list):
    for k in data:
        if (k in password):
            return True
    return False

def is_on_blacklist(password: str):
    with open('weak_pass.txt', 'r') as f:
        if password in f.read():
            return True
    return False