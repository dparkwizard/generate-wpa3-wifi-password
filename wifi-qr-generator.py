import random
import string
import argparse
import emoji
import sys
from wifi_qrcode_generator import generator
import qrcode
from PIL import Image

def get_random_emoji():
    """Get a random single-character emoji"""
    all_emojis = [c for c in emoji.EMOJI_DATA if len(c) == 1 and c not in ['️', '⃣']]
    return random.choice(all_emojis) if all_emojis else "📶"

def generate_wpa3_password(length=63):
    """Generate a WPA3-compatible password"""
    while True:
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?`~")
        ]
        password += [random.choice(
            string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?`~"
        ) for _ in range(length - 4)]
        random.shuffle(password)
        password = ''.join(password)
        
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(not c.isalnum() for c in password)):
            return password

def display_qr_in_terminal(data):
    """Display QR code in terminal using ASCII art"""
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    
    print("\nScan this QR code with your phone:\n")
    for line in qr.get_matrix():
        print(''.join(['██' if module else '  ' for module in line]))
    print()

def generate_wifi_qr(ssid, password, output_file="wifi_qr.png"):
    """Generate WiFi QR code, display it, and save to file"""
    wifi_config = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    
    # Display in terminal
    display_qr_in_terminal(wifi_config)
    
    # Save to file
    try:
        qr_code = generator.wifi_qrcode(
            ssid=ssid,
            authentication_type='WPA',
            password=password,
            hidden=False
        )
        qr_code.make_image().save(output_file)
        return True
    except Exception as e:
        print(f"Error saving QR code: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate WiFi QR code with emoji SSID")
    parser.add_argument("-l", "--length", type=int, default=63,
                      help="Password length (8-63, default: 63)")
    parser.add_argument("-o", "--output", type=str, default="wifi_qr.png",
                      help="Output filename (default: wifi_qr.png)")
    
    args = parser.parse_args()
    
    if args.length < 8 or args.length > 63:
        print("Error: Password length must be between 8 and 63 characters")
        sys.exit(1)
    
    ssid = get_random_emoji()
    password = generate_wpa3_password(args.length)
    
    print(f"\nWiFi Connection Details:")
    print(f"SSID: {ssid}")
    print(f"Password: {password}")
    
    if generate_wifi_qr(ssid, password, args.output):
        print(f"\nQR code also saved to {args.output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        sys.exit(0)
