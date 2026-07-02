# ATM PIN Checker

correct_pin = "1234"

print("===== ATM PIN Checker =====")

for attempt in range(1, 4):
    pin = input(f"Attempt {attempt}/3 - Enter your 4-digit PIN: ")

    if pin == correct_pin:
        print("✅ PIN is correct.")
        print("Welcome! Transaction Successful.")
        break
    else:
        print("❌ Incorrect PIN.")

else:
    print("\n🚫 Your account has been blocked.")
    print("Please contact your bank.")