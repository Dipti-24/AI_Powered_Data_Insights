from streamlit_authenticator.utilities.hasher import Hasher

password = "Dipti2025@ai"  # your chosen password as a string

hashed_password = Hasher.hash(password)

print("Your hashed password:")
print(hashed_password)
