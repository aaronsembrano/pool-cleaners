#!/usr/bin/env python3
"""
Builds a pool company website from template + JSON config.
Usage: python3 build-site.py config.json
Or import and call build_site(config_dict) directly.
"""

import json, os, re, shutil, sys

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "index.html")
HERO_PERSON_PATH = os.path.join(TEMPLATE_DIR, "hero-person.png")

def build_site(config):
    """Build a site from a config dict. Returns the output folder path."""
    folder_name = config["folder_name"]
    output_dir = os.path.join(TEMPLATE_DIR, folder_name)
    os.makedirs(output_dir, exist_ok=True)

    # Copy hero person image
    hero_dest = os.path.join(output_dir, "hero-person.png")
    if os.path.exists(HERO_PERSON_PATH) and not os.path.exists(hero_dest):
        shutil.copy2(HERO_PERSON_PATH, hero_dest)

    # Read template
    with open(TEMPLATE_PATH, "r") as f:
        html = f.read()

    # --- Page Title ---
    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{config["company_name"]} — {config.get("tagline", "Professional Pool Service")}</title>',
        html
    )

    # --- Tailwind Colors ---
    colors = config.get("colors", {})
    color_map = {
        "primary": colors.get("primary", "#0891B2"),
        "primary-dark": colors.get("primary_dark", "#164E63"),
        "primary-deeper": colors.get("primary_deeper", "#0C3547"),
        "secondary": colors.get("secondary", "#22D3EE"),
        "cta": colors.get("cta", "#22C55E"),
        "cta-dark": colors.get("cta_dark", "#16A34A"),
    }
    for key, val in color_map.items():
        pattern = rf"({re.escape(key)}:\s*')#[0-9A-Fa-f]{{6}}(')"
        html = re.sub(pattern, rf"\g<1>{val}\2", html)

    # --- Phone ---
    phone = config.get("phone", "(555) 987-6543")
    phone_digits = re.sub(r'[^\d]', '', phone)
    html = html.replace("(555) 987-6543", phone)
    html = html.replace("tel:5559876543", f"tel:{phone_digits}")
    html = html.replace("Call (555) 987-6543", f"Call {phone}")

    # --- Email ---
    email = config.get("email", "info@poolservice-cleaners.com")
    html = html.replace("info@poolservice-cleaners.com", email)
    html = html.replace("mailto:info@poolservice-cleaners.com", f"mailto:{email}")

    # --- Logo (Nav) ---
    logo_path = config.get("logo_path", "")
    company_name = config["company_name"]
    if logo_path and os.path.exists(os.path.join(output_dir, logo_path)):
        logo_html = f'<img src="{logo_path}" alt="{company_name}" class="h-14 max-w-[200px] object-contain" />'
    else:
        name_parts = company_name.split()
        if len(name_parts) > 1:
            first_part = " ".join(name_parts[:-1])
            last_part = name_parts[-1]
            logo_html = f'<span class="font-heading text-xl font-bold text-primary-dark tracking-tight">{first_part} <span class="text-primary">{last_part}</span></span>'
        else:
            logo_html = f'<span class="font-heading text-xl font-bold text-primary-dark tracking-tight">{company_name}</span>'
    html = re.sub(
        r'<span class="font-heading text-2xl font-bold text-primary-dark tracking-tight">P<span class="text-primary">OO</span>L\.</span>',
        logo_html, html
    )

    # --- Logo (Footer) ---
    if len(company_name.split()) > 1:
        name_parts = company_name.split()
        first_part = " ".join(name_parts[:-1])
        last_part = name_parts[-1]
        footer_logo = f'<span class="font-heading text-xl font-bold text-white tracking-tight">{first_part} <span class="text-secondary">{last_part}</span></span>'
    else:
        footer_logo = f'<span class="font-heading text-xl font-bold text-white tracking-tight">{company_name}</span>'
    html = re.sub(
        r'<span class="font-heading text-2xl font-bold text-white tracking-tight">P<span class="text-secondary">OO</span>L\.</span>',
        footer_logo, html
    )

    # --- Top Bar Trust Badges ---
    trust_badges = config.get("trust_badges", {})
    if trust_badges.get("badge_1"):
        html = html.replace("Licensed & Insured", trust_badges["badge_1"])
    if trust_badges.get("badge_2"):
        html = re.sub(r'4\.9/5 from 200\+ Reviews', trust_badges["badge_2"], html, count=1)
    if trust_badges.get("badge_3"):
        html = html.replace("No Contracts Required", trust_badges["badge_3"])

    # --- Hero Section ---
    hero = config.get("hero", {})
    if hero.get("badge_1"):
        html = html.replace("4.9/5 from 200+ Google Reviews", hero["badge_1"])
    if hero.get("badge_2"):
        html = html.replace("No Contracts Ever", hero["badge_2"])

    if hero.get("headline"):
        html = re.sub(
            r'Enjoy a Perfect Pool <span class="text-secondary italic">Without<br>the Hassle</span>',
            hero["headline"], html
        )
    if hero.get("subheadline"):
        html = re.sub(
            r'Owning a pool should be the fun part\..*?just dive in\.',
            hero["subheadline"], html, flags=re.DOTALL
        )
    if hero.get("cta_text"):
        html = html.replace("Get My Free Quote", hero["cta_text"])

    # Hero checkmarks
    checkmarks = hero.get("checkmarks", [])
    if len(checkmarks) >= 3:
        html = html.replace("Free inspection", checkmarks[0])
        html = html.replace("Same-week service", checkmarks[1])
        html = html.replace("Satisfaction guaranteed", checkmarks[2])

    # --- Stats Bar ---
    stats = config.get("stats", {})
    if stats.get("stat_1_value"):
        html = re.sub(r'data-target="120"', f'data-target="{stats["stat_1_value"]}"', html)
    if stats.get("stat_1_label"):
        html = html.replace(">Happy Clients<", f'>{stats["stat_1_label"]}<')
    if stats.get("stat_2_value"):
        html = re.sub(r'data-target="15"', f'data-target="{stats["stat_2_value"]}"', html)
    if stats.get("stat_2_label"):
        html = html.replace(">Years Experience<", f'>{stats["stat_2_label"]}<')
    if stats.get("stat_3_value"):
        html = re.sub(r'data-target="2500"', f'data-target="{stats["stat_3_value"]}"', html)
    if stats.get("stat_3_label"):
        html = html.replace(">Pools Serviced<", f'>{stats["stat_3_label"]}<')
    if stats.get("stat_4_value"):
        html = re.sub(r'>100%<', f'>{stats["stat_4_value"]}<', html, count=1)
    if stats.get("stat_4_label"):
        html = html.replace(">Satisfaction Rate<", f'>{stats["stat_4_label"]}<')

    # --- Services Section ---
    services = config.get("services", {})
    if services.get("label"):
        html = html.replace(">What We Do<", f'>{services["label"]}<')
    if services.get("headline"):
        html = re.sub(
            r'Pool Care That Gives You<br class="hidden md:block">\s*Your Weekends Back',
            services["headline"], html
        )
    if services.get("subtitle"):
        html = re.sub(
            r'Stop spending hours on pool maintenance\..*?enjoying your backyard\.',
            services["subtitle"], html
        )

    # Service cards (6 cards)
    cards = services.get("cards", [])
    template_cards = [
        ("Weekly Pool Cleaning", "Surface skimming, vacuuming, chemical balancing, and filter cleaning. Your pool stays swim-ready every single week."),
        ("Repairs & Equipment", "Pumps, filters, heaters, salt systems — we diagnose and fix it fast. Most repairs completed same-visit."),
        ("Green-to-Clean Recovery", "Pool turned green? We'll have it crystal clear in 48-72 hours. Emergency same-day response available."),
        ("Water Chemistry", "Precise chemical balancing that keeps water safe, clear, and gentle on skin. No red eyes, no irritation."),
        ("Renovation & Upgrades", "New tile, resurfacing, LED lighting, automation systems. Transform your pool into a backyard resort."),
        ("New Pool Installation", "Custom-designed pools built to fit your space, style, and budget. From concept to first splash."),
    ]
    for i, (orig_title, orig_desc) in enumerate(template_cards):
        if i < len(cards):
            card = cards[i]
            if card.get("title"):
                html = html.replace(f">{orig_title}<", f'>{card["title"]}<')
            if card.get("description"):
                html = html.replace(orig_desc, card["description"])

    # --- How It Works ---
    how_it_works = config.get("how_it_works", {})
    if how_it_works.get("headline"):
        html = html.replace("Three Steps to a Stress-Free Pool", how_it_works["headline"])

    steps = how_it_works.get("steps", [])
    template_steps = [
        ("Request Your Free Quote", "Tell us about your pool. We'll provide an honest, no-pressure quote within 24 hours. No contracts, no commitments."),
        ("We Handle Everything", "Our background-checked, CPO-certified technicians arrive on schedule. Cleaning, chemicals, equipment checks — all covered."),
        ("Enjoy Your Pool", "Your pool stays crystal clear, swim-ready, and worry-free. If you're ever not satisfied, we come back and make it right — free."),
    ]
    for i, (orig_title, orig_desc) in enumerate(template_steps):
        if i < len(steps):
            step = steps[i]
            if step.get("title"):
                html = html.replace(f">{orig_title}<", f'>{step["title"]}<')
            if step.get("description"):
                html = html.replace(orig_desc, step["description"])

    # --- About Section ---
    about = config.get("about", {})
    if about.get("label"):
        html = html.replace("Why Pool Owners Trust Us", about["label"])
    if about.get("headline"):
        html = re.sub(
            r"""We're Not "Some Pool Guy" — We're Your Pool Care Team""",
            about["headline"], html
        )
    if about.get("description"):
        html = re.sub(
            r'Family-owned and serving the community for over 15 years\..*?treat your pool like their own\.',
            about["description"], html, flags=re.DOTALL
        )
    if about.get("badge"):
        html = html.replace("CPO Certified", about["badge"])

    # About features (3)
    about_features = about.get("features", [])
    template_features = [
        ("Background-Checked Technicians", "Every technician passes a thorough background check before stepping foot in your backyard."),
        ("No Contracts. Cancel Anytime.", "We earn your business every visit. No long-term commitments, no cancellation fees, no surprises."),
        ("Satisfaction Guaranteed", "Not happy with a visit? We'll come back and redo it at no charge. That's our promise."),
    ]
    for i, (orig_title, orig_desc) in enumerate(template_features):
        if i < len(about_features):
            feat = about_features[i]
            if feat.get("title"):
                html = html.replace(f">{orig_title}<", f'>{feat["title"]}<')
            if feat.get("description"):
                html = html.replace(orig_desc, feat["description"])

    # --- Pricing ---
    pricing = config.get("pricing", {})
    if pricing.get("headline"):
        html = html.replace("Honest Pricing. No Hidden Fees.", pricing["headline"])
    if pricing.get("subtitle"):
        html = html.replace("Pick the plan that fits. Upgrade, downgrade, or cancel anytime — no contracts.", pricing["subtitle"])

    # --- Testimonials ---
    testimonials = config.get("testimonials", [])
    template_testimonials = [
        ("Sarah J.", "Homeowner, 8 months", "SJ", "We switched from another service and the difference is night and day. Pool is always sparkling, they show up on time, and the price is fair. Best decision we made this year."),
        ("Liam R.", "Green pool recovery", "LR", "Had a green pool nightmare after vacation. Called them Monday morning, they were there by Tuesday, and by Thursday it was crystal clear. Absolute lifesavers."),
        ("Maria K.", "Property Manager", "MK", "We manage three resort properties and Pool handles all of them. Consistent, professional, and their monthly reports make my job easy. Highly recommend for commercial."),
    ]
    for i, (orig_name, orig_ctx, orig_init, orig_text) in enumerate(template_testimonials):
        if i < len(testimonials):
            t = testimonials[i]
            if t.get("name"):
                html = html.replace(f">{orig_name}<", f'>{t["name"]}<')
            if t.get("context"):
                html = html.replace(f">{orig_ctx}<", f'>{t["context"]}<')
            if t.get("initials"):
                html = html.replace(f"?text={orig_init}", f'?text={t["initials"]}')
            if t.get("text"):
                html = html.replace(orig_text, t["text"])

    # --- Review count in testimonials header ---
    review_count = config.get("review_count", "")
    review_rating = config.get("review_rating", "")
    if review_count:
        html = html.replace("200+ Five-Star Reviews", f"{review_count}+ Five-Star Reviews")
        html = html.replace("200+ Reviews", f"{review_count}+ Reviews")
        html = html.replace("200+ Google Reviews", f"{review_count}+ Google Reviews")
    if review_rating:
        html = re.sub(r'4\.9 out of 5 on Google', f'{review_rating} out of 5 on Google', html)
        html = re.sub(r'4\.9/5 on Google', f'{review_rating}/5 on Google', html)

    # --- Guarantee ---
    guarantee = config.get("guarantee", {})
    if guarantee.get("headline"):
        html = html.replace('Our "Perfect Pool" Guarantee', guarantee["headline"])
    if guarantee.get("description"):
        html = re.sub(
            r"If you're not 100% satisfied with any service visit.*?until it does\.",
            guarantee["description"], html, flags=re.DOTALL
        )

    # --- FAQ ---
    faqs = config.get("faqs", [])
    template_faqs = [
        ("How quickly can you start service?", "Most new clients are scheduled within 3-5 business days. For green pool emergencies, we offer same-day or next-day response. Just call us and we'll work with your schedule."),
        ("Do I need to be home during service?", "Nope! Most clients give us gate access and we take care of everything while you're out. You'll receive a service summary after each visit so you always know what was done."),
        ("Are your technicians background-checked?", "Yes, every single one. All technicians pass a comprehensive background check, are CPO-certified, and carry full liability insurance. Your safety and peace of mind come first."),
        ("What if I want to cancel?", "Cancel anytime with zero fees. No contracts, no cancellation penalties, no guilt trips. We believe in earning your business every single visit."),
        ("Do you service commercial pools?", "Absolutely. We service hotels, resorts, HOAs, fitness centers, and apartment communities. Commercial clients get dedicated account managers and flexible scheduling."),
    ]
    for i, (orig_q, orig_a) in enumerate(template_faqs):
        if i < len(faqs):
            faq = faqs[i]
            if faq.get("question"):
                html = html.replace(orig_q, faq["question"])
            if faq.get("answer"):
                html = html.replace(orig_a, faq["answer"])

    # --- Contact Section ---
    contact = config.get("contact", {})
    if contact.get("headline"):
        html = re.sub(
            r'Ready for a Pool You<br>Actually Enjoy\?',
            contact["headline"], html
        )
    if contact.get("subtitle"):
        html = re.sub(
            r'Get a free, no-pressure quote in 24 hours\. No contracts, no commitments — just honest pricing for great pool care\.',
            contact["subtitle"], html
        )

    contact_benefits = contact.get("benefits", [])
    template_benefits = [
        "Free pool inspection with every quote",
        "Response within 24 hours",
        "100% satisfaction guaranteed",
    ]
    for i, orig in enumerate(template_benefits):
        if i < len(contact_benefits):
            html = html.replace(orig, contact_benefits[i])

    # --- Footer ---
    footer = config.get("footer", {})
    if footer.get("description"):
        html = html.replace("Family-owned pool service. Serving your community for 15+ years.", footer["description"])
    if footer.get("service_area"):
        html = html.replace("Serving the Greater Metro Area", footer["service_area"])

    # Footer service links
    footer_services = footer.get("services", [])
    template_footer_services = ["Weekly Cleaning", "Repairs & Equipment", "Green Pool Recovery", "Renovation & Upgrades", "New Installation"]
    for i, orig in enumerate(template_footer_services):
        if i < len(footer_services):
            html = html.replace(f">{orig}<", f'>{footer_services[i]}<')

    # Copyright
    if footer.get("copyright"):
        html = re.sub(
            r'&copy; 2024 Pool\. All rights reserved\..*?#CPC1234567',
            footer["copyright"], html
        )

    # Write output
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(html)

    return output_dir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build-site.py config.json")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        config = json.load(f)
    output = build_site(config)
    print(f"Built: {output}")
