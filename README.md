# francophone-companies-data-extractor

Automation agent to extract sales/commercial director contacts from African francophone companies via LinkedIn Sales Navigator.

---

## 📁 Project Structure

```
francophone-companies-data-extractor/
├── main.py                      ← Main orchestration script
├── config.py                    ← Configuration (no credentials)
├── requirements.txt             ← Python dependencies
├── input_companies.xlsx         ← 1,000+ Ivory Coast companies (input)
├── output_results.xlsx          ← Extracted contacts (auto-generated)
├── automation.log               ← Run log (auto-generated)
├── utils/
│   └── excel_handler.py         ← Excel read/write helpers
└── automation/
    └── linkedin_navigator.py    ← LinkedIn Sales Navigator automation
```

---

## ⚙️ Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.9 or later |
| Google Chrome | Latest stable |
| LinkedIn Sales Navigator | Active subscription, already logged in via Chrome |

> **No email/password is stored or used.** The tool reuses your existing Chrome profile where you are already logged in to LinkedIn.

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/MAmineJelassi/francophone-companies-data-extractor.git
cd francophone-companies-data-extractor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> `webdriver-manager` automatically downloads the correct ChromeDriver – no manual installation needed.

### 3. Configure your Chrome profile path

Open `config.py` and verify (or override) `CHROME_PROFILE_DIR`:

```python
# Default profile directory inside User Data
CHROME_PROFILE_DIR = 'Default'   # change to 'Profile 1', 'Profile 2', etc. if needed
```

The script auto-detects your operating system and uses the standard Chrome User Data directory:

| OS | Default path |
|---|---|
| **Windows** | `%LOCALAPPDATA%\Google\Chrome\User Data` |
| **macOS** | `~/Library/Application Support/Google/Chrome` |
| **Linux** | `~/.config/google-chrome` |

### 4. Log in to LinkedIn Sales Navigator

Open Chrome **with the same profile** and make sure you are logged in to [LinkedIn Sales Navigator](https://www.linkedin.com/sales/home).

---

## ▶️ Running the agent

```bash
python main.py
```

The agent will:

1. Read `input_companies.xlsx` (1,050 Ivory Coast companies)
2. Launch Chrome with your existing profile
3. Navigate to LinkedIn Sales Navigator
4. Search each company and extract director-level contacts
5. Save all results to `output_results.xlsx`

---

## 🎯 Target Roles

| Language | Roles |
|---|---|
| English | Sales Director, Commercial Director, General Director, IT Director |
| French | Directeur des Ventes, Directeur Commercial, Directeur Général, Directeur IT |

---

## 📊 Output Format (`output_results.xlsx`)

| Company | Name | Role | Email | Phone | LinkedIn Profile | Extracted At |
|---|---|---|---|---|---|---|
| Orange CI | Jean Dupont | Directeur Commercial | N/A | N/A | https://… | 2025-01-15T10:30:00 |

---

## 🛠️ Customisation

### Add or change companies

Edit `input_companies.xlsx` – add company names in column A (header row is `Company Name`).

### Change target roles

Edit the `TARGET_ROLES` dictionary in `config.py`.

### Run headless (no visible browser window)

In `config.py` set:

```python
BROWSER_SETTINGS = {
    'headless': True,
    ...
}
```

---

## 📋 Logging

All events are written to `automation.log` and printed to the console.

---

## 🔒 Privacy & Compliance

- No credentials are stored anywhere in this project.
- The tool uses your **existing, authenticated** Chrome session.
- Respect LinkedIn's Terms of Service and rate limits when running at scale.
