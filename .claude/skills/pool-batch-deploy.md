# Pool Batch Deploy Skill

Mass-clone the pool website template for a list of pool companies from a CSV lead sheet. For each company: research, clone, deploy to GitHub + Netlify, and enrich the CSV with the live URL.

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

## Process Per Company

For each row in the CSV:

### 1. Skip Check
- Skip if `Company Website` is empty or missing
- Skip duplicate companies (same `Company Website` already processed)
- Skip if the company is clearly not a pool company (e.g., swim schools)

### 2. Run the Pool Site Cloning Skill
Execute the `/pool-site-cloning` skill process:
- Research the company from their website URL
- Download their logo
- Copy the base template into a new folder named after the company (sanitized: lowercase, hyphens, no special chars)
- Apply all substitutions (brand, colors, contact, services, reviews, testimonials, pricing, FAQ, images)
- Verify all images return HTTP 200

### 3. Commit to GitHub
```bash
cd "/Users/aaronsembrano/Desktop/Pool Cleaners"
git add "{folder-name}/"
git commit -m "Add site for {Company Name}"
git push origin main
```

### 4. Deploy to Netlify
```bash
cd "/Users/aaronsembrano/Desktop/Pool Cleaners/{folder-name}"
npx netlify-cli deploy --prod --dir=. --site-name={sanitized-company-name}
```
Capture the production URL from the output.

### 5. Enrich the CSV Row
Add these new columns to the CSV (create them if they don't exist):
- `Website_Clone_URL` — the Netlify production URL (e.g., `https://cool-pool-people.netlify.app`)
- `Website_Clone_Status` — `live`, `failed`, or `skipped`
- `Website_Clone_Date` — ISO date when deployed (e.g., `2026-06-03`)
- `Personalized_Loom_Hook` — a suggested opener referencing their site: "Hey {casual_first_name}, I noticed {casual_company_name} in {casual_city_name} and put together a quick website concept for you — {Website_Clone_URL}"

### 6. Save Progress
After each company, write the updated CSV back to disk so progress isn't lost if the process is interrupted.

## Output

When complete, report:
1. Total companies processed vs skipped
2. List of live URLs with company names
3. Path to the enriched CSV
4. Any failures with reasons

## Enriched CSV Example

```csv
First Name,Last Name,...,Website_Clone_URL,Website_Clone_Status,Website_Clone_Date,Personalized_Loom_Hook
Todd,Gustafson,...,https://cool-pool-people.netlify.app,live,2026-06-03,"Hey Todd, I noticed Cool Pool People in Richardson and put together a quick website concept for you — https://cool-pool-people.netlify.app"
```

## Rate Limiting & Error Handling

- If a company website is unreachable, mark as `failed` and move to the next
- If logo download fails, use a text-based logo fallback
- If Netlify deploy fails, still commit to GitHub and note the failure
- If a Netlify site name is taken, append a random 3-digit suffix
- Process companies sequentially (not in parallel) to avoid GitHub push conflicts

## Important Notes

- The base template is at `/Users/aaronsembrano/Desktop/Pool Cleaners/index.html`
- The GitHub repo is `aaronsembrano/pool-cleaners`
- Use `sed -i ''` for macOS BSD sed
- Prefer targeted `Edit` tool over `sed` for URL replacements to avoid mangling
- Always verify image URLs return HTTP 200 before finalizing
- The enriched CSV should be saved back to the same path as the input, or to a new file like `{original_name}_enriched.csv`
- When processing large batches, report progress every 5 companies: "Completed 5/50 — latest: {company name} → {url}"
