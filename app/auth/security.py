import hashlib

# We hash refresh tokens before storing.
# If DB leaks → attacker cannot reuse them.
#If DB leaks → attacker cannot reuse them.
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()