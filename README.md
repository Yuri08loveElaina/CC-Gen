# ELAINA CUTE | Credit Card Generator & BIN Checker

> Made with 💜 by `Yuri08loveElaina`  
> Watermarked by `# yuri08loveelaina`  
> For educational & cybersecurity research only.

---

## 🔮 Features

- ✅ Generate valid test credit card numbers using Luhn algorithm  
- 🔍 Check BINs and card data using **multiple real-time APIs**  
- 🌐 Proxy support for stealth mode and rate limit avoidance  
- ⏱️ Randomized delay between API calls to bypass block detection  
- 📂 Check bulk cards from `.txt` file  
- 🧠 Automatic card structure validation (Luhn, format, brand)  
- ✨ All requests are branded with `User-Agent: ELAINA/1.0`  

---

## 🛠 Requirements

- Python 3.6+
- Module: `requests`

Install via pip:
```bash
pip install requests
```

---

## 🚀 Usage

### 1. Clone this repo:
```bash
git clone https://github.com/Yuri08loveElaina/CC-Gen.git
cd CC-Gen
```

### 2. Run the tool:
```bash
python elaina.py
```

### 3. Menu Options:
```
[1] Generate valid cards using BIN
[2] Check cards from file (pan|mm|yy|cvv)
[0] Exit
```

### 4. Input Format (for bulk check):
- One card per line
- Format: `4111111111111111|12|26|123`

---

## 📁 Output Files

- `live_cards.txt` → Valid or confirmed cards  
- `dead_cards.txt` → Invalid or failed validation  
- `check_log.txt` → Logs of each operation  

---

## 🔐 Proxy Support

You can input:
- `http://ip:port`
- `http://user:pass@ip:port`

Useful for rotating IPs or bypassing rate limits.

---

## ⚠️ Disclaimer

> This tool is created for **educational, auditing, and red-team research** only.  
> ❌ **Do not** use this tool for illegal or malicious purposes.

Author is **not responsible** for any misuse.

---

## 🧬 Signature

```
# Built with love by Yuri08 & Elaina
# yuri08loveelaina
```

---

## 💫 Stay ethical. Stay stealthy. Stay ELAINA.
