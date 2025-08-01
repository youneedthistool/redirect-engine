import json
import os
import gspread
from google.oauth2.service_account import Credentials

# Path to your config.json that contains nested google_sheets credentials
CONFIG_FILE = r"G:\My Drive\YouNeedThisTool\CORE\config.json"

# Load the full config JSON
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

# Extract the google_sheets credentials dict
google_sheets_creds = config.get("google_sheets")
if not google_sheets_creds:
    raise ValueError("google_sheets credentials not found in config.json")

# Define spreadsheet info
SPREADSHEET_ID = "1cUlooMtvIgTnVzQnRJoF1x7txty-6MJ_uBsQOvaUs40"
SHEET_NAME = "Contents"

# Output file and directory
OUTPUT_DIR = r"G:\My Drive\YouNeedThisTool\DATA-INGESTION"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "redirects.json")

# Scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

# Create credentials from the extracted dict and scopes
credentials = Credentials.from_service_account_info(google_sheets_creds, scopes=SCOPES)

# Authorize gspread client
client = gspread.authorize(credentials)

# Open sheet and fetch data
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
data = sheet.get_all_records()

# Build redirects dict
redirects = {}
for row in data:
    short_link = row.get("Short Link")
    affiliate_link = row.get("Affiliate Link")
    if short_link and affiliate_link:
        slug = short_link.split("/")[-1].lower().strip()
        redirects[slug] = {
            "affiliateLink": affiliate_link,
            "shortLink": short_link
        }

# Final JSON structure
final_json = {
    "total": len(redirects),
    "links": redirects
}

# Save JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_json, f, indent=2, ensure_ascii=False)

print(f"File saved at '{OUTPUT_FILE}' with {len(redirects)} redirects.\n")

# Print JSON to console for easy copying
print("=== Generated JSON content ===\n")
print(json.dumps(final_json, indent=2, ensure_ascii=False))
print("\n=== End of JSON content ===")
