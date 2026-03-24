import imaplib
import email
from email.header import decode_header
from database import get_db

# --- CONFIGURATION ---
EMAIL_USER = "anirudhdhamodaran107@gmail.com"
EMAIL_PASS = "lggm mzwf tcfj sahv" # 16-character App Password
IMPORTANT_IDS = ["example@important.com", "bank@updates.com"]

def clean_text(text):
    if text:
        decoded, encoding = decode_header(text)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(encoding if encoding else "utf-8")
        return decoded
    return ""

def sync_emails():
    db = get_db()
    cursor = db.cursor()
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        _, messages = mail.search(None, 'UNSEEN')
        for num in messages[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            sender = email.utils.parseaddr(msg['From'])[1]
            subject = clean_text(msg['Subject'])
            if sender.lower() in [i.lower() for i in IMPORTANT_IDS]:
                cursor.execute("INSERT INTO emails (sender, subject, received_at) VALUES (%s, %s, NOW())", (sender, subject))
        db.commit()
        mail.logout()
    finally:
        cursor.close()
        db.close()