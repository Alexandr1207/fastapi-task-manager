from pwdlib import PasswordHash


pass_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    hashed_password = pass_hash.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pass_hash.verify(
        password=password,
        hash=hashed_password
    )

my_pass = "12345"
hashed = hash_password(my_pass)
print(hashed)
print(verify_password(hashed, "my_pass"))
