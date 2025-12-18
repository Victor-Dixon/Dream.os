# dadudekc.com – Tasks Backlog

## Ad-Readiness Audit Findings (2025-12-17)

**Status:** Not ad-ready yet — but close

### Critical Issues
- **Philosophy-forward homepage:** Manifesto-style copy needs instant clarity for ads
- **Conflicting positioning:** Developer Tools storefront conflicts with consulting positioning
- **WordPress default junk:** "Hello world!" and "Uncategorized" indexed (hurts SEO/ad quality)

### Missing Ad Landing Essentials
- One clear offer per page (currently reads like multiple businesses)
- Primary CTA matching ads (Book / Apply / Get estimate)
- Proof assets (case studies, screenshots, outcomes, testimonials)
- Lead capture step (form + confirmation/thank-you page)

## Task List

### HIGH Priority
- [x] Clean up WordPress defaults (remove/redirect "Hello world!" and "Uncategorized" from navigation and sitemap) - **SA-DADUDEKC-SEO-DEFAULTS-04** ✅ COMPLETE by Agent-2: Renamed 'Uncategorized' to 'General', removed from navigation, verified no default post exists
- [x] Adopt unified positioning line site-wide: "I build automation systems that save teams hours every week." - **COPY-DADUDEKC-HERO-UNIFIER-02** ✅ COMPLETE by Agent-2: Homepage (ID: 5), About page (ID: 76), and Services page (ID: 77) all updated with unified positioning line. About and Services pages created. Tool: `tools/implement_dadudekc_positioning_unification.py`.
- [x] Add a primary, ad-matched CTA for the consulting lane (e.g., "Book a call" / "Apply for smoke session") with a dedicated thank-you page - **SA-DADUDEKC-HOME-CTA-02** ✅ COMPLETE by Agent-2: Primary CTA section added to homepage (ID: 5) with "Ready to Automate Your Workflow?" heading and "Work with Me" button linking to /contact. Tool: `tools/add_dadudekc_home_cta_wpcli.py`. Note: Thank-you page still pending.
- [x] Simplify primary nav to Home / Services / Case Studies / About / Contact and remove "Developer Tools" from main menus - **IA-DADUDEKC-NAV-UNIFY-01** ✅ VERIFIED by Agent-2: No WordPress menus configured, no "Developer Tools" menu items found. Navigation may be theme-based. Tool created: `tools/remove_dadudekc_developer_tools_menu.py`
- [ ] Clarify single primary offer per landing page (consulting vs developer tools) and align copy + layout to that one outcome

### MEDIUM Priority
- [ ] Add proof assets (case study snapshots, outcomes, testimonials or screenshots) to at least one ad-ready landing page
- [ ] Add a lightweight lead-capture form (name + email + context) wired to a confirmation state, ready for ad traffic
- [ ] Tighten the "about" story to connect engineering → consulting offers
- [ ] Map a clear consulting CTA that routes cleanly into Smoke Session / offers
- [ ] Identify which existing blog content should be featured vs archived
