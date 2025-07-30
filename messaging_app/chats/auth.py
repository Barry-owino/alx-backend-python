# chats/auth.py

# Placeholder for custom authentication logic (if needed in future)
🔐 What auth.py can do:
It can contain:

Custom authentication classes – e.g., extending JWTAuthentication to customize how tokens are validated.

Custom permission checks – extra logic to allow or deny access based on your rules.

User identification logic – tweak how the user is fetched from a token or request.

🧠 Example Use Case:
If you're using JWT and want to log token access, reject expired tokens with custom messages, or attach extra user data, you'd put that logic in auth.py.

