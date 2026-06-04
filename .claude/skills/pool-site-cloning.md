# Pool Site Cloning Skill

Clone the conversion-optimized pool company website template for a new pool business. The user provides a company website URL, and you produce a fully branded site with unique copy in a new folder.

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

### Step 2: Write Unique Copy

**CRITICAL: Do NOT reuse the template's generic copy.** Every section must be rewritten for this specific company's brand voice, differentiators, and services. Generate ALL of the following unique to this company:

- **Hero headline** — emotional, outcome-focused, max 8 words. Use their differentiator (e.g., "18 Years of Showing Up, No Exceptions" not "Enjoy a Perfect Pool")
- **Hero sub-headline** — 2-3 sentences about THEIR specific value proposition
- **Hero badges** — 2 trust badges specific to them (e.g., "RAIL Certified" not generic "No Contracts")
- **Hero checkmarks** — 3 items unique to their selling points
- **CTA button text** — tailored to their brand (e.g., "Get Your Pool Dialed In", "Talk to a Local Pro", "Join the Family")
- **Services section headline & subtitle** — about THEIR approach
- **How It Works** — 3 steps matching THEIR actual workflow
- **About section** — headline, description, and 3 features about THEIR specific story, credentials, and team
- **About badge** — their top credential for the floating badge on the image
- **Guarantee section** — their specific promise, not generic satisfaction guarantee
- **FAQ** — 5 questions relevant to THEIR services and common objections for their market
- **Contact section** — headline, subtitle, and 3 benefits specific to them
- **Pricing headlines** — if they show pricing, use their tiers; if not, use consultation-focused language

**Match the company's tone:** tech-forward companies get sharp, modern copy; family businesses get warm, personal copy; expertise-driven companies get authority-focused copy.

### Step 3: Download the Logo

```bash
curl -sL "{logo_url}" -o "{folder}/logo.png"
file "{folder}/logo.png"
```

**LEARNED:** Many pool company websites are JS-rendered (React/Next.js) and return HTML error pages instead of images when you curl their logo URL. Always verify the downloaded file with `file` — if it says "HTML document" instead of "PNG/JPEG image data", the download failed.

**Logo fallback strategy:**
1. Try the URL from the research
2. Try common paths: `/logo.png`, `/images/logo.png`, `/wp-content/uploads/logo.png`
3. If all fail, use a **styled text logo** instead:
   - Nav: `<span class="font-heading text-xl font-bold text-primary-dark tracking-tight">Company <span class="text-primary">Name</span></span>`
   - Footer: Same but with `text-white` and `text-secondary` for the accent word

### Step 4: Create the Folder & Copy Template

```bash
mkdir -p "/Users/aaronsembrano/Desktop/Pool Cleaners/{Folder Name}"
cp "/Users/aaronsembrano/Desktop/Pool Cleaners/index.html" "/Users/aaronsembrano/Desktop/Pool Cleaners/{Folder Name}/index.html"
```

### Step 5: Apply All Substitutions

**PREFERRED METHOD:** Use a single Python script to do ALL replacements at once. This avoids the sed URL-mangling issues we hit when chaining multiple sed commands on URLs with `&` and `?` characters.

Work through these categories in order:

#### 5a. Page Title
Replace `<title>` with: `{Company Name} — {Their Tagline or Primary Headline}`

#### 5b. Color Scheme (Tailwind config)
Replace these values:
- `primary` — their primary brand color
- `primary-dark` — darker variant (darken primary by 20-30%)
- `primary-deeper` — deepest variant (darken primary by 40-50%)
- `secondary` — their secondary/accent color

**ALSO:** Replace the CTA color to match their brand:
- `cta` — use their primary or accent color, NOT the default green `#22C55E`
- `cta-dark` — darker variant of their CTA color

#### 5c. Contact Info (appears 6+ times)
Replace ALL occurrences of:
- Phone number: `(555) 987-6543` and `tel:5559876543`
- Email: `info@poolservice-cleaners.com` and `mailto:info@poolservice-cleaners.com`
- Address in footer

#### 5d. Logo — Nav Bar
Replace the text logo span with an img tag:
```html
<img src="logo.png" alt="{Company Name}" class="h-14 max-w-[200px] object-contain" />
```

**LEARNED — Square logos:** If the logo is nearly square (height ≈ width), reduce to `h-12 object-contain` to prevent it from looking oversized. Do NOT add `rounded-lg` — it makes square logos look like profile pictures.

**LEARNED — Logo sizing:** `h-14` works for horizontal/wide logos. Square logos need `h-12` max. Always check the logo's aspect ratio with `file` before choosing the size.

#### 5e. Logo — Footer
**DO NOT use `brightness-0 invert` on footer logos.** This was tried and fails badly — logos with white/light backgrounds become invisible white boxes on the dark footer.

**Instead, use styled text for ALL footer logos:**
```html
<span class="font-heading text-xl font-bold text-white tracking-tight">Company <span class="text-secondary">Name</span></span>
```
Split the company name so the last word (or a key word) uses the `text-secondary` accent color.

#### 5f. Reviews & Trust Signals
- Star rating and review count (appears in: top bar, hero badges, testimonials header, footer)
- Trust badge text in top bar and hero section — use THEIR specific credentials, not generic text
- Certification badge on about section image

#### 5g. Stats Bar — MUST BE UNIQUE PER COMPANY
**LEARNED:** The stats bar (120+ Happy Clients, 15+ Years, etc.) was not getting updated because the Python script wasn't replacing them. These MUST be customized:
- Update `data-target="120"` → their actual review count or client count
- Update `data-target="15"` → their years in business
- Update `data-target="2500"` → their estimated pools serviced
- Update the `>100%<` stat → their satisfaction rate or Google rating
- Update ALL label text (`>Happy Clients<`, `>Years Experience<`, etc.)

#### 5h-5q. All Copy Sections
Apply the unique copy from Step 2 to:
- Hero (headline, sub, badges, checkmarks, CTA text)
- Services section (headline, subtitle)
- Service cards (6 titles + 6 descriptions)
- How It Works (title + 3 steps)
- About section (label, headline, description, 3 features, badge)
- Pricing (headline, subtitle)
- Guarantee (headline, description)
- FAQ (5 questions + 5 answers)
- Contact section (headline, subtitle, 3 benefits)
- Testimonials (3 names, 3 review texts, 3 contexts, 3 avatar initials)
- Footer (description, service links, copyright)

### Step 6: Replace Stock Images

Use the same pool images from the base template — they are pre-verified working Unsplash URLs showing premium backyard pools. No need to find new images per company unless the user requests it.

**If replacing images:** Always use the `Edit` tool for URL replacements, NEVER `sed`. Sed mangles URLs by concatenating old and new strings when they contain `&` and `?` characters.

After any image changes, verify ALL URLs:
```bash
grep -oP 'photo-[0-9a-f-]+' index.html | sort -u | while read id; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/$id?w=200&q=10")
  echo "$id → $code"
done
```

### Step 7: Verify & Deploy

```bash
# Start local server
cd "{folder}" && npx serve . -l {next_available_port} &>/dev/null &
```

Or deploy to Netlify:
```bash
cd "{folder}" && rm -rf .netlify && npx netlify-cli deploy --prod --dir=. --site-name={sanitized-name}
```

**LEARNED:** Always `rm -rf .netlify` before deploying a new site, otherwise Netlify reuses the previously linked site and deploys to the wrong URL.

## Checklist Before Reporting Done

- [ ] Logo downloads and displays correctly in nav (check for HTML error pages, square logo sizing)
- [ ] Footer uses styled text logo (NOT img with invert filter)
- [ ] All phone numbers updated (top bar, nav, hero, CTA section, footer, mobile sticky — 6+ places)
- [ ] All email addresses updated
- [ ] Color scheme applied including CTA button color (not default green)
- [ ] Stats bar numbers are unique to this company (not template defaults)
- [ ] Hero copy is unique and tailored to this company's brand voice
- [ ] About section tells THIS company's story
- [ ] How It Works matches THEIR workflow
- [ ] FAQ questions are relevant to THEIR services
- [ ] Guarantee section reflects THEIR specific promise
- [ ] All image URLs return HTTP 200 (if any were changed)
- [ ] No mangled URLs (grep for `q=80q=80`, `w=600photo`, etc.)
- [ ] 3 real testimonials with names and context
- [ ] Site deployed and accessible

## Key Learnings / Gotchas

1. **NEVER use `sed` for URL replacements** — use Python or the `Edit` tool. Sed concatenates instead of replacing when URLs contain `&` and `?`.
2. **NEVER use `brightness-0 invert` on footer logos** — logos with white backgrounds become invisible. Use styled text instead.
3. **NEVER use `rounded-lg` on square logos** — they look like profile pictures. Check aspect ratio first.
4. **Always verify logo downloads with `file`** — JS-rendered sites return HTML instead of images.
5. **Always `rm -rf .netlify`** before deploying a new Netlify site to avoid reusing a previous site's config.
6. **Copy MUST be unique per company** — the single biggest quality issue is reusing template copy. Every headline, about paragraph, FAQ, guarantee, and how-it-works must be rewritten.
7. **Stats bar must be customized** — this is easy to miss because the data-target attributes are buried in the HTML.
8. **CTA color should match brand** — don't leave all buttons as the default green. Use the company's primary or accent color.

## Notes

- The base template is at `/Users/aaronsembrano/Desktop/Pool Cleaners/index.html`
- Use port 3000 + N for the Nth cloned site (3001, 3002, etc.)
- If the company doesn't list certain info (email, hours, pricing), use reasonable placeholders and tell the user what needs to be filled in
- Always use `sed -i ''` (macOS BSD sed) not `sed -i` (GNU sed) for any non-URL replacements
- The GitHub repo is `aaronsembrano/pool-cleaners`
