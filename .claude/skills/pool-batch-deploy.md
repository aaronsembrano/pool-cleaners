# Pool Batch Deploy Skill

Mass-clone the pool website template for a list of pool companies from a CSV lead sheet. For each company: research, write unique copy, clone, deploy to GitHub + Netlify, and enrich the CSV with the live URL.

## Trigger

When the user says any of: "batch deploy", "deploy for all", "clone all these", "process the lead list", "enrich the sheet", or provides a CSV of pool companies and asks to build sites and/or enrich the data.

## Inputs

- **CSV file path** (required) — a lead sheet with columns including: `First Name`, `Last Name`, `Email`, `Company Name`, `Company Website`, `Company Phone`, `City`, `State`, `Company Description`, and optionally `casual_first_name`, `casual_company_name`
- **Count** (optional) — how many to process. Defaults to all rows. User may say "do the first 5" etc.

## CSV Column Mapping

The lead sheet follows this structure:
```
First Name, Last Name, Full Name, Email, Personal Email, Mobile Number, Job Title, Seniority Level, LinkedIn, Company Name, Company Website, Company Phone, Company LinkedIn, Industry, Company Size, City, State, Country, Company Description, Headline, casual_first_name, casual_company_name, casual_city_name
```

## Parallelization Strategy

**Research phase:** Launch up to 5 research subagents in parallel. Each agent researches one company (website scrape + Google reviews search). This is the slowest step and benefits most from parallelization.

**Copy writing phase:** After research completes for a batch, send all company data to a single subagent that writes unique copy for all companies in that batch at once.

**Build phase:** Use a single Python script to build all sites in a batch simultaneously (string replacements are instant).

**Deploy phase:** Sequential — Netlify deploys and git pushes must be sequential to avoid conflicts.

## Process Per Batch (5 companies at a time)

### 1. Extract & Deduplicate
- Parse CSV, skip rows with no `Company Website`
- Skip duplicate companies (same URL already processed)
- Skip non-pool companies (swim schools, etc.)
- Save each company's CSV data to a JSON config

### 2. Parallel Research (5 subagents)
Launch one subagent per company to gather:
- Phone, email, address, hours
- Google rating + review count (search "{company name} google reviews")
- Logo URL
- Brand colors (hex codes from their website)
- Services list (top 6)
- 3 real testimonials with names
- Trust signals, certifications, years in business
- Key differentiators

### 3. Write Unique Copy (1 subagent for whole batch)
**CRITICAL — this was the #1 quality issue in our first run.** Send all 5 company profiles to a single subagent and request unique copy for each:
- Hero headline + sub-headline (tailored to their brand voice)
- Hero badges and checkmarks (their specific credentials)
- CTA button text (unique per company)
- Services section headline + subtitle
- How It Works (3 steps matching their workflow)
- About section (headline, description, 3 features, badge text)
- Pricing headline + subtitle
- Guarantee headline + description (their specific promise)
- FAQ (5 questions relevant to their services)
- Contact section headline + subtitle + 3 benefits

**Tone matching rules:**
- Tech-forward companies → sharp, modern copy
- Family businesses → warm, personal copy
- Expertise-driven companies → authority-focused copy
- Community-focused companies → local pride copy

### 4. Build All Sites (Python script)
Use a single Python script that reads all research JSON + custom copy JSON and builds all sites at once. The script must handle:

**Brand substitutions:**
- Page title, Tailwind color config (primary, primary-dark, primary-deeper, secondary)
- **CTA color** — MUST match their brand, not default green. Replace `cta` and `cta-dark` in config.
- Phone (6+ occurrences), email, address
- Reviews (rating + count appears in 5+ places)
- Trust badges in top bar and hero

**Logo handling:**
- Download with `curl`, verify with `file` command
- If download returns HTML (JS-rendered site), use styled text fallback
- Nav: `class="h-14 max-w-[200px] object-contain"` for wide logos, `class="h-12 object-contain"` for square logos
- **Footer: ALWAYS use styled text, never img.** `brightness-0 invert` fails on logos with white backgrounds. Use: `<span class="font-heading text-xl font-bold text-white tracking-tight">Company <span class="text-secondary">Name</span></span>`

**Stats bar — MUST be unique per company:**
- `data-target="120"` → their review count or client count
- `data-target="15"` → their years in business
- `data-target="2500"` → their estimated pools serviced
- `>100%<` → their satisfaction rate or Google rating
- ALL label text must be updated too

**All copy sections from Step 3** (hero, about, how-it-works, services, guarantee, FAQ, contact, pricing, testimonials, footer)

### 5. Commit to GitHub (batch)
```bash
cd "/Users/aaronsembrano/Desktop/Pool Cleaners"
git add folder1/ folder2/ folder3/ folder4/ folder5/
git commit -m "Add sites for {Company 1}, {Company 2}, ... {Company 5}"
git push origin main
```

### 6. Deploy to Netlify (sequential)
```bash
for folder in folder1 folder2 folder3 folder4 folder5; do
  cd "/Users/aaronsembrano/Desktop/Pool Cleaners/$folder"
  rm -rf .netlify  # IMPORTANT: prevents reusing previous site config
  npx netlify-cli deploy --prod --dir=. --site-name={sanitized-name}
done
```

**LEARNED:** Always `rm -rf .netlify` before deploying. Without this, Netlify reuses the previously linked site and deploys to the wrong URL.

**LEARNED:** If a site name is taken, append `-tx` or a state abbreviation suffix.

### 7. Enrich the CSV
Add these columns (create if they don't exist):
- `Website_Clone_URL` — the Netlify production URL
- `Website_Clone_Status` — `live`, `failed`, or `skipped`
- `Website_Clone_Date` — ISO date when deployed
- `Personalized_Loom_Hook` — ready-to-use cold email opener: "Hey {casual_first_name}, I noticed {casual_company_name} in {casual_city_name} and put together a quick website concept for you — {Website_Clone_URL}"

### 8. Save Progress
Write the updated CSV after each batch so progress isn't lost if interrupted.

## Output

When complete, report:
1. Total companies processed vs skipped
2. Table of live URLs with company names
3. Path to the enriched CSV
4. Any failures with reasons

## Key Learnings / Gotchas

1. **Copy MUST be unique per company** — the #1 quality issue. Every headline, about paragraph, FAQ, guarantee, and how-it-works must be rewritten for each company's brand voice.
2. **NEVER use `sed` for URL replacements** — use Python or the `Edit` tool. Sed concatenates URLs containing `&` and `?`.
3. **NEVER use `brightness-0 invert` on footer logos** — use styled text instead. White-background logos become invisible.
4. **NEVER use `rounded-lg` on square logos** — they look like profile pictures.
5. **Always verify logo downloads with `file`** — JS-rendered sites return HTML instead of images.
6. **Always `rm -rf .netlify`** before deploying a new Netlify site.
7. **Stats bar MUST be customized** — easy to miss because data-target attributes are buried in HTML.
8. **CTA buttons should match brand color** — don't leave all buttons as default green.
9. **Footer logos should always be styled text** — image logos on dark backgrounds are unreliable.
10. **Batch git commits** — commit all sites in a batch together, then push once. Don't push after each site.

## Important Notes

- The base template is at `/Users/aaronsembrano/Desktop/Pool Cleaners/index.html`
- The GitHub repo is `aaronsembrano/pool-cleaners`
- Always use `sed -i ''` for macOS BSD sed (non-URL replacements only)
- The enriched CSV should be saved as `{original_name}_enriched.csv`
- Report progress every 5 companies: "Completed 5/50 — latest: {company name} → {url}"
- Stock images from the base template are pre-verified and can be reused across all clones
