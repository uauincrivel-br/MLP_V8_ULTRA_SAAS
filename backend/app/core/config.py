
import os

class Settings:
    PROJECT_NAME = "mlp-ultra-saas-v8"

    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev")

    # SaaS plans
    PLANS = {
        "free": {"rps": 1, "priority": 3},
        "pro": {"rps": 10, "priority": 2},
        "enterprise": {"rps": 50, "priority": 1},
    }

settings = Settings()
