def send_otp_email(to_email: str, otp_code: str, purpose: str) -> None:
    subject = {
        "email_verification": "Verify your HomeMart email",
        "password_reset": "Reset your HomeMart password",
    }.get(purpose, "Your HomeMart verification code")

    print("=" * 50)
    print("📧  MOCK EMAIL SENT (no real email was sent)")
    print(f"To:      {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:    Your HomeMart OTP code is: {otp_code}")
    print(f"         This code expires in 10 minutes.")
    print("=" * 50)
