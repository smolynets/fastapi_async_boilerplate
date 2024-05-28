import os
from dotenv import load_dotenv

load_dotenv()


JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # 30 minutes by default
JWT_REFRESH_TOKEN_LIFETIME_MINUTES = int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_MINUTES", 10080))  # 7 days by default
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")  # should be kept secret

