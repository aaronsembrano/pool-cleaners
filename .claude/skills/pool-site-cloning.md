# Pool Site Cloning Skill

Clone the conversion-optimized pool company website template for a new pool business. The user provides a company website URL, and you produce a fully branded site in a new folder.

## Trigger

When the user says any of: "clone site for", "create site for", "new pool website", "pool site clone", or provides a pool company URL and asks you to build/clone a site for them.

## Inputs

- **Company website URL** (required) — the pool company to clone for
- **Folder name** (optional) — defaults to the company name

## Process

### Step 1: Research the Company

Use a subagent to fetch the company's website and search the web for their business info. Gather ALL of the following:

1. **Business name** (exact, including any trademark)
2. **Phone number(s)** — primary and any office-specific numbers
3. **Email address** — if not listed, use a placeholder format: info@{domain}
4. **Physical address(es)** and service areas/cities served
5. **Business hours** (Mon-Fri, Sat, Sun)
6. **Tagline / headline copy** they use on their site
7. **Services offered** — full list, identify the top 6 to feature as cards
8. **Google review rating and count** — search "{company name} Google reviews"
9. **Testimonials** — grab 3 real reviews with reviewer first name + last initial and context
10. **Color scheme** — identify primary, secondary, and accent colors (hex codes)
11. **Logo URL** — find the direct URL to their logo image file (usually in /wp-content/uploads/ or similar)
12. **Certifications, awards, years in business** — any trust signals (BBB, industry awards, licenses)
13. **Pricing** — if shown, capture tiers/ranges; if not, use "Schedule a Consultation" instead of prices
14. **Key differentiators** — what they emphasize (family-owned, years experience, guarantees, etc.)

### Step 2: Download the Logo

```bash
curl -sL "{logo_url}" -o "{folder}/logo.png"
```

Verify the file downloaded correctly with `file`. If the logo URL doesn't work, try alternative paths or ask the user.

### Step 3: Create the Folder & Copy Template

```bash
mkdir -p "/Users/aaronsembrano/Desktop/Pool Cleaners/{Folder Name}"
cp "/Users/aaronsembrano/Desktop/Pool Cleaners/index.html" "/Users/aaronsembrano/Desktop/Pool Cleaners/{Folder Name}/index.html"
```

### Step 4: Apply All Substitutions

Work through these categories in order. Use `sed` for bulk replacements and targeted `Edit` for complex changes.

#### 4a. Page Title
Replace `<title>` with: `{Company Name} — {Their Tagline or Primary Headline}`

#### 4b. Color Scheme
Replace these values in the Tailwind config block:
- `primary` — their primary brand color
- `primary-dark` — darker variant (darken primary by 20-30%)
- `primary-deeper` — deepest variant (darken primary by 40-50%)
- `secondary` — their secondary/accent color
- `bg-light` — very light tint of primary (5-10% opacity equivalent)
- `bg-section` — slightly different light tint for alternating sections
- `card-border` — light border color matching the palette
- `text-heading` — dark variant of primary for headings

#### 4c. Contact Info (appears 6+ times)
Replace ALL occurrences of:
- Phone number: `(555) 987-6543` and `tel:5559876543`
- Email: `info@poolservice-cleaners.com` and `mailto:info@poolservice-cleaners.com`
- Address in footer

#### 4d. Logo
Replace ALL occurrences of the text logo span with:
```html
<img src="logo.png" alt="{Company Name}" class="h-10" />
```
The footer logo needs `brightness-0 invert` for visibility on dark background:
```html
<img src="logo.png" alt="{Company Name}" class="h-10 brightness-0 invert" />
```
**Watch out:** The nav and footer logos have different HTML structures. Check both.

#### 4e. Reviews & Trust Signals
- Star rating and review count (appears in top bar, hero badges, testimonials header, footer)
- Trust badge text ("No Contracts Required" → their differentiator, "Licensed & Insured" → their credential)
- Certification badge on about section image

#### 4f. Stats Bar
- 4 numbers: clients/reviews, years experience, pools built/serviced, satisfaction rate
- Update both `data-target` attributes AND the label text

#### 4g. Hero Copy
- Main headline (emotional, outcome-focused)
- Sub-headline paragraph (their value proposition)
- CTA button text (e.g., "Schedule Free Consultation" vs "Get My Free Quote")
- Sub-CTA trust checkmarks (3 items)

#### 4h. Services (6 cards)
For each of the 6 service cards, update:
- Card title
- Description paragraph
- Alt text on image

#### 4i. How It Works (3 steps)
Customize the 3-step process titles and descriptions to match their workflow.

#### 4j. About / Why Choose Us
- Section header and subheader
- Description paragraph
- 3 trust bullet points (title + description each)

#### 4k. Pricing (3 tiers)
- Tier names, prices (or "Custom Quote"), descriptions
- Feature bullet points for each tier
- If company doesn't show pricing, use ranges or "Starting from" language

#### 4l. Testimonials (3 reviews)
- Reviewer name (first name + last initial)
- Review text (from their actual Google/Yelp reviews)
- Context line ("Homeowner", "Pool renovation", etc.)

#### 4m. Guarantee Section
Customize the guarantee headline and description to match their promise.

#### 4n. FAQ (5 questions)
Rewrite questions and answers relevant to their specific services and common objections.

#### 4o. Contact Form
- Form header text
- Service type dropdown options (match their services)
- CTA button text

#### 4p. Footer
- Company description
- Service links (match the 6 services)
- Business hours
- Contact details
- Copyright with company name and any license numbers

#### 4q. Mobile Sticky CTA
Update phone number and CTA text.

### Step 5: Replace Stock Images

Find 8 working Unsplash image URLs relevant to their services:
1. Hero background
2. About section main image
3. About section detail/overlay image
4. Service cards (6 images matching their services)
5. CTA section background

**IMPORTANT:** After replacing URLs, verify EVERY image returns HTTP 200:
```bash
grep -oP 'photo-[0-9a-f-]+' index.html | sort -u | while read id; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/$id?w=200&q=10")
  echo "$id → $code"
done
```

Replace any 404s before proceeding.

**ALSO IMPORTANT:** When using `sed` to replace URLs, be careful with special characters (`&`, `?`, `/`). Test that URLs don't get concatenated/mangled. After sed replacements, grep for patterns like `q=80q=80` or `w=600photo` to catch mangled URLs.

### Step 6: Verify & Deploy

```bash
# Start local server
cd "{folder}" && npx serve . -l {next_available_port} &>/dev/null &
```

Tell the user the localhost URL and summarize what was customized.

## Checklist Before Reporting Done

- [ ] Logo downloads and displays in nav AND footer
- [ ] All phone numbers updated (check top bar, nav, hero, CTA section, footer, mobile sticky)
- [ ] All email addresses updated
- [ ] Color scheme applied in Tailwind config
- [ ] All 8+ image URLs return HTTP 200
- [ ] No mangled URLs (grep for `q=80q=80`, `w=600photo`, etc.)
- [ ] Reviews show correct rating and count
- [ ] 3 real testimonials with names
- [ ] Pricing reflects their actual tiers/ranges
- [ ] FAQ answers are relevant to their business
- [ ] Site deployed on localhost and accessible

## Notes

- The base template is at `/Users/aaronsembrano/Desktop/Pool Cleaners/index.html`
- Use port 3000 + N for the Nth cloned site (3001, 3002, etc.)
- If the company doesn't list certain info (email, hours, pricing), use reasonable placeholders and tell the user what needs to be filled in
- Always use `sed -i ''` (macOS BSD sed) not `sed -i` (GNU sed)
- For sed replacements on URLs, prefer targeted `Edit` tool over sed to avoid mangling
