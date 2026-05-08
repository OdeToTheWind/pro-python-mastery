# src/day_54_sending_email/main.py
"""
Day 54: Sending Email with Python and SMTP – Demo
"""

def main():
    print("Welcome to Day 54 – Sending Email with SMTP\n")
    print("Note: For real email sending, you need SMTP credentials (Gmail, etc.)")
    print("This is a demonstration only.\n")

    recipient = input("Enter recipient email (demo): ")
    subject = input("Subject: ")
    body = input("Message body: ")

    print("\nSimulated Email:")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print("\n✅ In real code, this would be sent via smtplib.")

    print("\nNext: Working with Date and Time (Day 55)\n")


if __name__ == "__main__":
    main()