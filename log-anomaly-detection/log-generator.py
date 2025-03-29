import random
from datetime import datetime, timedelta

components = ["AuthService", "Database", "API", "PaymentGateway", "UserService"]
log_levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
users = [f"user_{i}" for i in range(1000)]
transactions = [f"txn_{i:04x}" for i in range(1000)]

timestamp = datetime(2023, 10, 5, 8, 0, 0)

with open("app.log", "w") as f:
    for _ in range(1000):
        timestamp += timedelta(seconds=random.randint(1,5))
        component = random.choice(components)
        log_level = random.choices(log_levels, weights=[6, 2, 1.5, 0.5])[0]

        # Generate log message
        if component == "AuthService":
            msg = f"User {random.choice(users)} {'logged in' if random.random() > 0.1 else 'failed login'}"
        elif component == "Database":
            msg = random.choice(["Connection established", "Query executed", "Connection timeout", "Deadlock detected"])
        elif component == "PaymentGateway":
            msg = f"Transaction {random.choice(['processed', 'failed'])}: {random.choice(transactions)}"
        elif component == "API":
            status = random.choices([200, 404, 500], weights=[8, 1, 1])[0]
            msg = f"{random.choice(['GET', 'POST'])} /api/v1/{random.choice(['users', 'products'])} {status}"

        line = f"[{timestamp.isoformat()}] {log_level} {component} - {msg}\n"
        f.write(line)
