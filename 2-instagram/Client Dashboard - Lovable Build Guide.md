# Client Dashboard — Lovable Build Guide

## What You're Building

A custom client-facing dashboard for The Coach Consultant that acts as a single hub for coaching clients. Based on your spec document, this dashboard has **seven core modules**, each of which we'll break down below with exactly how to build it in Lovable, what data it needs, and what to watch out for.

---

## Architecture Overview

Before diving into individual modules, here's how the whole thing fits together. In Lovable, you'll be building a React + Supabase app. The recommended structure is:

- **Authentication**: Each client logs in and sees only their own dashboard. Use Supabase Auth.
- **Database**: Supabase (Postgres) stores all client data — objectives, reporting scores, KPIs, finance records, call recordings, and SOP progress.
- **Navigation**: A sidebar or tabbed layout with these main sections:
  1. North Star Objectives
  2. Monthly Objectives & Deliverables
  3. 1-1 Call Vault
  4. EOM Reporting Vault (Subjective + KPIs)
  5. Motherboard Dashboard (Live Data)
  6. Monthly Finance Reporting
  7. Titan IP & SOP Bank

---

## Module 1: North Star Objectives

### What It Does
Displays the client's three overarching objectives front and centre at the top of the dashboard. These are the big-picture goals that everything else feeds into.

### How to Build It in Lovable

Prompt Lovable with something like:

> "Create a section at the top of the dashboard called 'North Star Objectives'. It should display exactly 3 objectives as editable card components. Each card has a title field (e.g. 'Objective 1') and a text area for the objective description. Store these in a Supabase table called `north_star_objectives` with columns: `id`, `client_id`, `objective_number` (1–3), `description`, `updated_at`. Only the admin (you/Beth) should be able to edit these. The client sees them as read-only."

### Database Table

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients table |
| objective_number | int | 1, 2, or 3 |
| description | text | The objective itself |
| updated_at | timestamp | Auto-updated |

### Considerations
- Decide whether clients can edit their own objectives or only you can. If it's collaborative, add a "last edited by" field.
- Keep these visually prominent — they should anchor the entire dashboard experience.

---

## Module 2: Monthly Objectives & Deliverables

### What It Does
A month-by-month workspace showing the client's action plans across 13 categories (Onboarding Forms, Claude AI Setup, Personal Media, Company Media, Lead Magnets, Offer Dev, Outreach, Sales, Emails, Paid Media, Operations, Leadership, Mindset) plus their individual action plans (Overview, Personal Media, Lead Generation, Offer Impact, Sales, Emails, Paid Ads, Operations, Leadership, Mindset).

### How to Build It in Lovable

This is one of the more complex modules. Break it into two parts:

**Part A — Monthly Category Checklist:**

> "Create a monthly deliverables section with a month/year selector at the top. Below that, show a checklist of 13 deliverable categories (list them). Each item has a checkbox for completion status, and optionally a link field for a Google Drive URL. Store in a Supabase table `monthly_deliverables` with: `id`, `client_id`, `month_year` (e.g. '2026-04'), `category`, `is_complete` (boolean), `drive_link` (text, nullable). Add a Google Drive link field at the top of the section for the monthly folder."

**Part B — Action Plans:**

> "Below the checklist, create an accordion or tab set for 10 action plan areas (Overview, Personal Media, Lead Generation, Offer Impact, Sales, Emails, Paid Ads, Operations, Leadership, Mindset). Each area expands to show a rich text editor or structured task list. Store in `action_plans` table with: `id`, `client_id`, `month_year`, `plan_area`, `content` (text/json), `updated_at`."

### Database Tables

**monthly_deliverables:**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| month_year | text | e.g. "2026-04" |
| category | text | One of the 13 categories |
| is_complete | boolean | Default false |
| drive_link | text | Nullable, Google Drive URL |

**action_plans:**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| month_year | text | e.g. "2026-04" |
| plan_area | text | e.g. "Personal Media" |
| content | jsonb | Structured plan content |
| updated_at | timestamp | Auto-updated |

### Considerations
- The Google Drive link at the top should open in a new tab. You might want to embed a Google Drive preview, but be aware this can be unreliable — a simple link is more dependable.
- Consider whether action plans should carry forward month to month (copy previous month's plan as a starting template).
- Rich text vs. structured tasks: a simple bullet-point task list with checkboxes is easier to build in Lovable than a full rich text editor. Start simple.

---

## Module 3: 1-1 Call Vault

### What It Does
A repository of all coaching call recordings and notes, automatically fed from Fathom AI (your call recording tool and Beth's).

### How to Build It in Lovable

> "Create a 'Call Vault' section that displays a list of past coaching calls. Each call entry shows: date, duration, coach name (Ben or Beth), a summary/notes field, and a link to the Fathom recording. Display calls in reverse chronological order with search and date-range filtering. Store in a Supabase table `call_vault` with: `id`, `client_id`, `call_date`, `coach_name`, `duration_minutes`, `summary`, `fathom_link`, `created_at`."

### The Fathom Integration Question

This is a **critical consideration**. Fathom doesn't have a public API that lets you automatically push recordings into a custom app. Your realistic options are:

1. **Manual Entry (Simplest)**: After each call, you or Beth paste the Fathom link and summary into the dashboard. Quick to build, but requires discipline.
2. **Zapier/Make Automation**: If Fathom has a Zapier integration, you could set up a zap that triggers when a new recording is created and posts the data to your Supabase database via a webhook. Check Fathom's integration options.
3. **Fathom → Google Drive → Dashboard**: Fathom can export to Google Drive. You could store links to the Google Drive copies.
4. **Webhook Endpoint**: Build a simple Supabase Edge Function that receives data via webhook, so any automation tool can push call data in.

**Recommendation**: Start with manual entry plus a Zapier automation if available. Don't let this block the rest of the build.

### Considerations
- Add a tag or filter for "Ben's calls" vs "Beth's calls."
- Consider adding AI-generated action items from each call (Fathom often provides these — you could paste them in).
- Search functionality should cover the summary/notes text.

---

## Module 4: EOM Reporting Vault

### What It Does
This is your end-of-month check-in system with two sub-sections: **Subjective Ratings** (how the client feels about each area, 1–10 with written feedback) and **Key KPIs** (hard numbers).

### Part A — Subjective Ratings

The 12 categories to rate are: AI Adoption, Personal Media, Company Media, Lead Generation, Offer Impact, Outreach, Sales, Emails, Paid Media, Operations/Organisation, Leadership, and Mindset.

> "Create an 'End of Month Report' section. At the top, add a month/year selector. Below that, create a form with 12 categories (list them). Each category has: a slider or number input (1–10) for the rating score, and a text area for written feedback. Add a 'Submit Report' button that saves all 12 ratings to Supabase. Below the form, show a trend chart that displays how each category's score has changed month over month (use Recharts). Store in a `subjective_ratings` table."

**Also add the overall 'Subjective Feeling' score at the very top — a single 1–10 rating that captures how the client feels overall that month, tracked as a trend line.**

### Database Table — subjective_ratings

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| month_year | text | e.g. "2026-04" |
| category | text | One of the 12 areas |
| rating | int | 1–10 |
| feedback | text | Written commentary |
| submitted_at | timestamp | When submitted |

### Part B — Key KPIs

Your document notes that KPIs may need to be custom-built per client. The default KPIs you've listed are:

- Total Personal Follower Growth (all platforms)
- Total Company Follower Growth (all platforms)
- Total Leads Generated
- Total Website Page Visits
- Total Calls Booked
- Close Rate
- Total Outreach Sales
- Total Client Cancellations
- Total Revenue Collected
- Total Net Profit
- Total Cash In Bank
- Average Email Open Rate
- Ads: Cost Per Acquisition

> "Below the subjective ratings, create a 'Key KPIs' section. Display a form where the client inputs monthly figures for each KPI. Use number inputs. Store in a `monthly_kpis` table. Below the input form, show a data table and trend charts for each KPI over time. Make the KPI list configurable per client — store the KPI definitions in a `kpi_definitions` table so you can add/remove KPIs for different clients."

### Database Tables

**kpi_definitions:**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients (nullable = global) |
| kpi_name | text | e.g. "Total Revenue Collected" |
| kpi_unit | text | e.g. "£", "%", "count" |
| display_order | int | Ordering |
| is_active | boolean | Toggle on/off per client |

**monthly_kpis:**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| kpi_definition_id | uuid | FK to kpi_definitions |
| month_year | text | e.g. "2026-04" |
| value | numeric | The actual figure |
| submitted_at | timestamp | When submitted |

### Considerations
- The "!" markers next to Calls Booked and Close Rate in your doc suggest these are high-priority KPIs. Consider highlighting them visually (colour-coded, or pinned at the top).
- Trend charts are essential here. Lovable supports Recharts out of the box — use line charts for scores over time, and bar charts for volume metrics like revenue.
- For the custom-per-client KPI setup: build an admin panel where you can toggle which KPIs each client sees. This avoids a gym owner seeing "Ads: Cost Per Acquisition" if they don't run ads.
- Consider adding month-on-month percentage change indicators (green up arrow / red down arrow) next to each KPI.

---

## Module 5: Motherboard Dashboard

### What It Does
A live data dashboard that pulls from an external Google Sheet (your "Motherboard" spreadsheet) and provides AI-powered feedback/recommendations.

### How to Build It in Lovable

This has two layers:

**Layer 1 — Data Display:**

> "Create a 'Motherboard' section that displays key business metrics in a dashboard grid layout. Use card components showing the most important numbers, with trend indicators. Pull data from the `motherboard_data` Supabase table."

**Layer 2 — The Google Sheets Connection:**

This is where it gets technical. Your options:

1. **Google Sheets API → Supabase Edge Function**: Write a Supabase Edge Function that reads from the Google Sheet on a schedule (e.g. every hour) and writes the data into your Supabase tables. This is the most robust approach.
2. **Google Apps Script Push**: Add a Google Apps Script to the spreadsheet that pushes data to a Supabase webhook whenever the sheet is updated.
3. **Manual Sync (MVP)**: For launch, clients or you manually input the data. Automate later.
4. **SheetDB or similar middleware**: Services like SheetDB turn Google Sheets into a JSON API, which you can fetch from directly.

**Layer 3 — AI Intelligence Feed:**

Your doc mentions "intelligence to give feedback on what they need to do as a live feed." This is ambitious but achievable:

> "Add an 'AI Insights' card below the Motherboard data. Use a Supabase Edge Function that takes the client's latest KPI data, sends it to the OpenAI/Claude API with a prompt like 'Based on these business metrics for a coaching client, provide 3 actionable recommendations', and displays the response. Refresh this weekly or on-demand when the client clicks a 'Get Insights' button."

### Considerations
- **Start without the API connection.** Build the dashboard UI first with manual data entry, then layer in the Google Sheets sync later. Don't let the integration block the entire build.
- The AI insights feature is a genuine differentiator for your product. But it needs good prompt engineering — the recommendations should reference the client's actual numbers and the Titan IP framework.
- API costs: If you're using Claude or GPT to generate insights per client per month, the cost is minimal (pennies per request), but budget for it.
- Your doc says "the API data stuff can come through later" — this confirms the phased approach. Build the container now, wire up live data in phase 2.

---

## Module 6: Monthly Finance Reporting

### What It Does
A simple income vs. expenses tracker that calculates monthly profit margin, with potential insights on areas to review.

### How to Build It in Lovable

> "Create a 'Finance' section with two sub-areas: Income and Expenses. Each has an 'Add Entry' button that opens a form with: date, description, category, and amount (£). Display entries in a table grouped by month. At the top, show summary cards: Total Income, Total Expenses, Net Profit, and Profit Margin %. Use a bar chart comparing income vs expenses month over month. Store in `finance_entries` table with: `id`, `client_id`, `entry_type` (income/expense), `date`, `description`, `category`, `amount`, `created_at`."

### Database Table

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| entry_type | text | "income" or "expense" |
| entry_date | date | Date of transaction |
| description | text | What it was |
| category | text | e.g. "Coaching Revenue", "Software", "Ads" |
| amount | numeric | In pounds |
| created_at | timestamp | When recorded |

### Pre-Set Categories

Define sensible defaults so clients aren't starting from scratch:

**Income categories**: Coaching Revenue, Consulting Fees, Course Sales, Membership Income, Affiliate Income, Speaking Fees, Other Income

**Expense categories**: Software & Tools, Advertising, Contractor/VA Costs, Rent/Facility Costs, Insurance, Professional Development, Travel, Admin/Office, Other Expenses

### Considerations
- Your doc mentions "areas they need to review" — you could add conditional formatting or alerts. For example: if expenses in any category exceed 30% of revenue, flag it in red. If profit margin drops below a threshold, show a warning.
- CSV import would be a powerful addition (clients export from their bank and upload). Lovable can handle CSV parsing with Papaparse.
- This is sensitive financial data. Make sure Row Level Security (RLS) in Supabase is airtight — no client should ever see another client's finances.
- Consider whether you want rolling 12-month views, quarterly summaries, or just monthly snapshots.

---

## Module 7: Titan IP & SOP Bank

### What It Does
A library of your intellectual property — the Titan framework of SOPs, guides, and systems — organised by category, with progress tracking so clients can see what they've worked through.

### The Titan IP Structure

From the linked document, your IP is organised into 7 pillars:

1. **Architecture & Scale** — Org design, systemising delivery, delegation, productising services
2. **Financial Mastery** — Revenue intelligence, pricing, recurring revenue, P&L, exit strategy
3. **Founder Psychology & Identity** — Practitioner-to-CEO shift, decision-making, energy management, vision
4. **Growth & Client Acquisition** — Sales systems, high-ticket offers, referrals, partnerships
5. **Influence & Authority** — Positioning, content, speaking, community
6. **Advanced Operations** — Tech stack, facility ops, dashboards, legal, remote teams
7. **Team & Talent** — Hiring, front-of-house, culture, performance management

Plus a recommended 8-phase build sequence.

### How to Build It in Lovable

> "Create a 'Titan SOP Bank' section. Display the 7 IP pillars as collapsible categories in a sidebar or accordion. Each pillar contains a list of SOPs/topics. Each topic has: a title, a description, a link to the full resource (Google Doc/Drive), and a completion status (not started / in progress / completed). Show an overall progress bar per pillar and a master progress bar across all pillars. Store in `sop_topics` (the master list) and `client_sop_progress` (per-client completion status)."

### Database Tables

**sop_topics (master list, shared across clients):**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| pillar | text | e.g. "Architecture & Scale" |
| title | text | e.g. "Systemising Your Delivery" |
| description | text | Short summary |
| resource_link | text | Google Drive URL |
| display_order | int | Ordering within pillar |
| applicable_to | text[] | e.g. ["coaches", "consultants", "facility_owners"] |

**client_sop_progress:**

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| client_id | uuid | FK to clients |
| sop_topic_id | uuid | FK to sop_topics |
| status | text | "not_started", "in_progress", "completed" |
| notes | text | Client's notes |
| completed_at | timestamp | Nullable |

### Considerations
- The "applicable_to" field is important — your doc distinguishes between content for coaches/consultants vs. facility owners. Filter the SOP list based on the client's business type.
- Progress tracking is a powerful engagement tool. Consider adding it to the main dashboard home screen as a summary widget.
- You might want to gate access — only unlock certain pillars once previous ones are complete (following your recommended build sequence). This prevents overwhelm and ensures clients build foundations first.
- Your doc mentions a progress tracker with "???" — this confirms it's something you want but haven't fully defined. The approach above gives you a clean, scalable way to do it.

---

## Admin Panel

You'll also need a back-end view for yourself and Beth to manage all clients.

> "Create an admin section (accessible only to users with admin role) that shows: a list of all clients, the ability to click into any client's dashboard and see/edit their data, a way to add new clients, manage KPI definitions per client, manage SOP topics, and view all EOM reports across clients in a summary view."

This is essential for your business operations — without it, you'll be editing Supabase tables directly, which isn't sustainable.

---

## Recommended Build Order in Lovable

Build this in phases. Don't try to ship everything at once.

**Phase 1 — Foundation (Week 1–2):**
Set up the Supabase project, auth system, client database, and basic layout with sidebar navigation. Get one client able to log in and see an empty dashboard.

**Phase 2 — Core Modules (Week 2–4):**
Build North Star Objectives, Monthly Deliverables, and the EOM Reporting Vault (subjective ratings + KPIs). These are the most-used daily features.

**Phase 3 — Finance & Call Vault (Week 4–5):**
Add the Finance Reporting module and Call Vault. These are self-contained and don't depend on external integrations.

**Phase 4 — SOP Bank (Week 5–6):**
Build the Titan IP library and progress tracking. This requires populating the SOP content — plan time for data entry.

**Phase 5 — Motherboard & AI (Week 6–8):**
Wire up the Motherboard dashboard with Google Sheets integration and add the AI insights feature. This is the most technically complex phase.

**Phase 6 — Polish & Admin (Week 8–10):**
Build the admin panel, refine the UI, add CSV import for finance, and iron out mobile responsiveness.

---

## Key Considerations & Potential Pitfalls

### 1. Supabase Row Level Security (RLS)
This is non-negotiable. Every single table must have RLS policies ensuring clients can only see their own data. One client accidentally seeing another's financials or KPIs would be a serious trust breach. Test this thoroughly.

### 2. Lovable's Limitations
Lovable is excellent for building React + Supabase apps quickly, but be aware of these constraints:
- **Complex state management**: If a page has lots of interdependent data (like the EOM report form with 12 categories), you may need to prompt Lovable carefully to manage state correctly.
- **Custom integrations**: The Google Sheets API connection and AI insights will likely require writing Supabase Edge Functions directly — Lovable may not scaffold these automatically.
- **Styling consistency**: As you add modules, keep prompting Lovable to maintain a consistent design system (colours, spacing, typography). Things can drift.

### 3. Mobile Responsiveness
Your clients will check their dashboard on their phones. Make sure every module works on mobile. Test early and often. Trend charts and data tables are notoriously tricky on small screens — consider simplified mobile views.

### 4. Data Entry Burden
The biggest risk to adoption isn't the tech — it's whether clients actually fill in their EOM reports, KPIs, and finance data each month. Consider:
- Email/SMS reminders when reports are due
- Making the forms as quick as possible (pre-fill where you can)
- Showing the value immediately (trend charts that only work if they input data)

### 5. Google Drive Links vs. Embedded Content
Your deliverables section links to Google Drive. Embedding Google Docs inside your dashboard is possible but unreliable (Google's embed policies change). Stick with clean links that open in new tabs.

### 6. Fathom Integration Uncertainty
Don't build the dashboard architecture around a Fathom API that may not exist or may change. Build the Call Vault as a standalone module with manual entry, then add automation as a bonus.

### 7. AI Insights — Prompt Engineering Matters
When you build the Motherboard AI feed, the quality depends entirely on the prompt. Incorporate context about the Titan framework, the client's business type, and their historical data. A generic "here are some tips" response won't impress. Make it specific: "Your close rate dropped from 45% to 32% this month. Based on the Titan Sales Systems framework, consider reviewing your discovery call script and objection handling process."

### 8. Scalability
If you plan to offer this dashboard to many clients, consider:
- **Multi-tenancy**: Supabase handles this well with RLS, but plan your table structure accordingly.
- **Customisation per client**: The KPI definitions and SOP filtering already handle this, but think about whether different clients need different dashboard layouts entirely.
- **Pricing**: If this becomes a product, the Supabase and AI API costs will scale with client numbers. Budget accordingly.

### 9. Backup & Export
Clients may want to export their data (KPIs, finance reports). Build CSV export functionality into each module. This also protects you — if a client leaves, they can take their data with them cleanly.

### 10. Authentication & Onboarding
First impressions matter. When a new client logs in for the first time, they should see a guided setup flow — not an empty dashboard. Pre-populate their North Star Objectives, set up their KPI definitions, and have their first month's deliverables ready.

---

## Prompt Strategy for Lovable

When building in Lovable, break your prompts into small, specific requests rather than trying to describe the whole dashboard at once. For example:

1. "Set up a Supabase-connected app with authentication. Create a clients table and a login page."
2. "Add a sidebar navigation with these sections: Dashboard Home, Objectives, Call Vault, Monthly Report, Finance, SOP Bank."
3. "Create the North Star Objectives component..." (as described above)
4. Continue module by module.

After each prompt, review what Lovable generated, test it, and course-correct before moving to the next module. Lovable works best iteratively.

---

## Summary

You're building a genuinely powerful client management tool. The key is to resist the urge to build everything at once. Start with the modules your clients will use daily (Objectives, Deliverables, EOM Reporting), validate that the experience works, and then layer in the more complex features (Motherboard API, AI insights, Fathom integration) once the foundation is solid.

The Titan IP & SOP Bank with progress tracking is a standout feature — it turns your intellectual property into a structured journey rather than a folder of documents. That alone could be a significant differentiator for your coaching practice.
