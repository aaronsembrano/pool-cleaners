#!/bin/bash
# Usage: ./build-site.sh <company-json-file> <folder-name> <netlify-site-name>
# Clones the template, applies substitutions from a JSON config, and deploys to Netlify

set -e

COMPANY_JSON="$1"
FOLDER="$2"
NETLIFY_NAME="$3"
BASE_DIR="/Users/aaronsembrano/Desktop/Pool Cleaners"
TEMPLATE="$BASE_DIR/index.html"

if [ -z "$COMPANY_JSON" ] || [ -z "$FOLDER" ] || [ -z "$NETLIFY_NAME" ]; then
  echo "Usage: ./build-site.sh <company.json> <folder-name> <netlify-site-name>"
  exit 1
fi

# Read JSON values using python
read_json() {
  python3 -c "import json,sys; d=json.load(open('$COMPANY_JSON')); print(d$1)" 2>/dev/null
}

NAME=$(read_json "['name']")
PHONE=$(read_json "['phone']")
EMAIL=$(read_json "['email']")
ADDRESS=$(read_json "['address']")
TAGLINE=$(read_json "['tagline']")
RATING=$(read_json "['google_rating']")
COUNT=$(read_json "['google_count']")
LOGO_URL=$(read_json "['logo_url']")
CITY=$(read_json "['city']")
STATE=$(read_json "['state']")
YEARS=$(read_json "['years_in_business']")
PRIMARY=$(read_json "['colors']['primary']")
PRIMARY_DARK=$(read_json "['colors']['primary_dark']")
PRIMARY_DEEPER=$(read_json "['colors']['primary_deeper']")
SECONDARY=$(read_json "['colors']['secondary']")
HOURS_WD=$(read_json "['hours_weekday']")
HOURS_SAT=$(read_json "['hours_sat']")
HOURS_SUN=$(read_json "['hours_sun']")

echo "Building site for: $NAME ($CITY, $STATE)"

# Create folder and copy template
mkdir -p "$BASE_DIR/$FOLDER"
cp "$TEMPLATE" "$BASE_DIR/$FOLDER/index.html"

# Download logo
if [ -n "$LOGO_URL" ] && [ "$LOGO_URL" != "None" ]; then
  curl -sL "$LOGO_URL" -o "$BASE_DIR/$FOLDER/logo.png" 2>/dev/null || true
fi

cd "$BASE_DIR/$FOLDER"

# Apply substitutions
python3 << 'PYEOF'
import json, re, sys

with open(sys.argv[1] if len(sys.argv) > 1 else 'company.json') as f:
    c = json.load(f)

with open('index.html', 'r') as f:
    html = f.read()

# Title
html = html.replace(
    '<title>Pool — Enjoy a Perfect Pool Without the Hassle</title>',
    f'<title>{c["name"]} — {c["tagline"][:60]}</title>'
)

# Colors
html = html.replace("primary: '#0891B2'", f"primary: '{c['colors']['primary']}'")
html = html.replace("'primary-dark': '#164E63'", f"'primary-dark': '{c['colors']['primary_dark']}'")
html = html.replace("'primary-deeper': '#0C3547'", f"'primary-deeper': '{c['colors']['primary_deeper']}'")
html = html.replace("secondary: '#22D3EE'", f"secondary: '{c['colors']['secondary']}'")

# Phone (all instances)
html = html.replace('(555) 987-6543', c['phone'])
html = html.replace('tel:5559876543', 'tel:' + re.sub(r'[^0-9]', '', c['phone']))

# Email
html = html.replace('info@poolservice-cleaners.com', c['email'])

# Logo - nav
html = html.replace(
    """<span class="font-heading text-2xl font-bold text-primary-dark tracking-tight">P<span class="text-primary">OO</span>L.</span>""",
    f'<img src="logo.png" alt="{c["name"]}" class="h-10" />'
)

# Reviews
html = html.replace('4.9/5 from 200+ Reviews', f'{c["google_rating"]}/5 from {c["google_count"]}+ Reviews')
html = html.replace('4.9/5 from 200+ Google Reviews', f'{c["google_rating"]}/5 from {c["google_count"]}+ Google Reviews')
html = html.replace('200+ Five-Star Reviews', f'{c["google_count"]}+ Five-Star Reviews')
html = html.replace('4.9 out of 5 on Google', f'{c["google_rating"]} out of 5 on Google')
html = html.replace('4.9/5 on Google', f'{c["google_rating"]}/5 on Google')

# Address
html = html.replace('Serving the Greater Metro Area', c['address'])

# Hours
html = html.replace('7:00 am – 6:00 pm', c.get('hours_weekday', '8:00 am – 5:00 pm'))
html = html.replace('8:00 am – 2:00 pm', c.get('hours_sat', '9:00 am – 1:00 pm'))

# Footer copyright
html = html.replace(
    '© 2024 Pool. All rights reserved. Licensed & Insured. FL License #CPC1234567',
    f'© 2024 {c["name"]}. All rights reserved. Licensed & Insured.'
)

# About section
html = html.replace(
    'Family-owned and serving the community for over 15 years.',
    f'Serving {c["city"]} and surrounding areas for over {c["years_in_business"]} years.'
)

with open('index.html', 'w') as f:
    f.write(html)

print(f'Substitutions applied for {c["name"]}')
PYEOF

echo "✅ Site built for $NAME"
echo "Folder: $BASE_DIR/$FOLDER"
