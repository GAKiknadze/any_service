class FakePasswordService:
    def __init__(self):
        self._hash = "hashed"

    def verify_password(self, plain, hashed):
        return hashed == self._hash and plain == "password"

    def hash_password(self, password):
        return self._hash
