import sys

from paypalcheckoutsdk.core  import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "ATUVrxgDp3-l_JRAndH5kkld1PjsbhejrlgLulKRX4fTaGgnZZM0aUAQPPKyYp7rSWj1K6uzfwnlviKo"
        self.client_secret = "EFIam1fcICiN7g7E63UkenjI9uFgGsqyJ629z-D32fGzq-er8uUN0yHIeQvZ8qnyAEQopM59tty5G2hZ"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)