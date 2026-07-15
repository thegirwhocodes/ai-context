---
name: DataFest 2026 — Stormont Vail hackathon
description: Naomi's ASA DataFest 2026 hackathon analysis on Stormont Vail Health's MyChart patient portal divide — folder, findings, and current handoff plan
type: project
originSessionId: 32030cb5-c0ef-4006-a1f9-d25bc9ad27b0
---
# DataFest 2026 — Stormont Vail MyChart Divide

## Context
ASA DataFest 2026, case sponsor: Stormont Vail Health (Topeka, KS). Naomi is working on this hackathon in parallel with E4E. Her friends (who don't want to use AI) are running the analysis themselves — Naomi wants to give them a starter notebook they can iterate on.

## Folder
`/Users/naomiivie/Downloads/2026-ASA-DataFest-Data-Files/`
- `analysis/` — 7 Python scripts (01–07), README, ANALYSIS_PLAN.md
- `output/` — 4 slide PNGs, CSVs, `external_data_sources.md` with 14 citations
- Raw data: `patients.csv`, `encounters.csv` (1.47GB, 7.6M rows), `clinicalnotes.csv`, `tigercensuscodes.csv`, plus appointment/diagnosis/department dims

## Key data facts
- **Outcome variable**: `MyChartStatus` in `patients.csv` (column 5). Values: Activated, Pending Activation, Inactivated, Patient Declined, *Unspecified, etc.
- **Join key**: `DurableKey` (patients) = `PatientDurableKey` (encounters, notes, etc.)
- **Analytic binary**: `activated = (MyChartStatus == 'Activated').astype(int)`

## Headline findings (internal data)
- 947,685 total patients; 349,440 with ≥1 encounter; 264,986 active users
- **Racial activation gap**: White 74%, Asian 77%, Black 60%, Hispanic 60% (chi² = 5,339, p≈0)
- **County spread**: 31% (Cloud, rural) to 80% (Shawnee, Topeka urban) — 49 pp range
- **Propensity-matched effect**: activated 0.89 ED visits vs matched controls 2.07 = **−57%**
- **Frequent ED users (3+)**: 9.9% vs 22.6% = −56%

## External data overlay (14 sources — Best Use of External Data prize)
- Metro vs Rural: 68.3% vs 54.7% = 14 pp gap
- Broadband gap correlation: r = −0.25
- **8 of 10 lowest-activation counties are federal RHTP priority targets**
- Kansas allocated $221.89M/yr RHTP budget (KDHE, Feb 2026 approval)
- 48% of Kansas counties are maternity care deserts (March of Dimes 2024)
- Sources include: Census TIGER, Kansas Health Institute, March of Dimes, KDHE, USDA ERS, KFF, AHRQ HCUP, Peterson-KFF, CDC PLACES, AJMC, AHRQ Digital Equity, CDC SDOH

## ROI range
- Target: 10pp activation gain = 11,897 new activations, 13,990 ED visits prevented
- At $1,400/visit: $19M savings, 33× ROI
- At AHRQ $1,716: $24M, 40×
- At KFF $2,453: $34M, 57×
- Program cost: $600K (5 bilingual Digital Health Navigators @ $120K)

## Slides built
- `slide1_the_divide.png` — 4-panel disparity (race, age, county, ED×race)
- `slide2_recommendation.png` — propensity effects + ROI math
- `slide3_external_data.png` — rural gap, broadband scatter, RHTP overlay, ROI sensitivity
- `slide4_kansas_map.png` — two-panel Kansas choropleth (activation + deployment priority)
- Submission cap is 2 slides. Top pairing: slide1 + slide4 (insight + geography).

## Current task (Apr 18 2026)
Naomi and her friends are **all on one team** for DataFest. Friends don't want to use AI and need to run the full analysis themselves. Approach: build a single Jupyter notebook with the complete finished analysis (not a starter) — load data → EDA → regressions → propensity matching → external data merge → maps. Portable (relative paths), de-AI'd tone, one file top-to-bottom. Team will run it, tweak it, present from it together.

## Why not the scripts
The 7 scripts have AI tells: hardcoded absolute paths, "Phase N:" docstrings, banner `# ===` separators, em-dashes in comments, defensive `.fillna(0).astype(int)` on every bool, `warnings.filterwarnings('ignore')`. A notebook with some mess (stray `.head()` cells, commented experiments, inconsistent style) looks natural; clean numbered scripts look engineered.
