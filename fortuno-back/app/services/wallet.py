from app.models.wallet import Transaction

class WalletService:
    def __init__(self, wallet):
        self.wallet = wallet