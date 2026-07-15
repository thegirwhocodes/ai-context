---
name: Academic Reference - Professors, Textbooks, Tools & Links
description: Quick reference for professor info, textbook names, course tools, and key paths
type: reference
sessions:
  - 8f6ef573-a64c-4918-834c-5b7d6ea634c0
  - 54dd4efb-7e00-469d-9b2d-02e160e3af35
  - 983fedaf-c4fb-41ed-a452-635feada0d8e
  - e22a61ad-77d5-4374-a719-b7d8db5eac49
  - 6efb2481-b890-4754-95b7-49de6ac05f9b
  - ead3e4eb-2e2e-4268-824e-15b9aaf8318b
---

# Academic Reference

## Professors
| Course | Professor | Notes |
|--------|-----------|-------|
| Econ 241 | Prof. Imai | Money, Banking & Financial Markets |
| Econ 333 | Unknown | Financial Intermediation; uses numbered lecture PDFs |
| Econ 349 | Prof. Kuenzel | Economic Growth; requires term paper with empirical regressions |
| QAC 386 | Unknown | Text Mining; provides OpenAI API access under QAC386 org |

## Textbooks
| Course | Textbook | Location |
|--------|----------|----------|
| Econ 241 | Mishkin, *The Economics of Money, Banking, and Financial Markets*, 13th ed. | `Econ 241 - Money, Banking/Econ 241 Textbook.pdf` |
| Econ 349 | Jones & Vollrath, *Introduction to Economic Growth*, 3rd ed. (2013) | `Econ 349 - Economic Growth/Textbook Econ 349 Jones and Vollrath (2013)...pdf` |
| Econ 333 | No single textbook — lecture slides + case study papers | Lecture PDFs in course folder |
| QAC 386 | No textbook — class Colab notebooks | `Qac 386 - Text Mining/Classes/` |

## Key Paths
- **OneDrive root**: `~/Library/CloudStorage/OneDrive-wesleyan.edu/`
- **Classes folder**: `~/Library/CloudStorage/OneDrive-wesleyan.edu/Classes/`
- **Transcripts**: `~/Library/CloudStorage/OneDrive-wesleyan.edu/Classes/Transcripts/`
- **Old Classes path** (pre-Feb 17 2026): `~/Downloads/Classes/` (migrated to OneDrive)

## Tools & Platforms
| Tool | Purpose |
|------|---------|
| **Google Colab** | QAC 386 homework and class notebooks |
| **Moodle** | Course materials, assignment submission (all 4 courses) |
| **Tactiq** | Class recording transcription (Pro account, auto-saves to OneDrive) |
| **Apple Notes** | iOS 18 built-in recording + transcription for class recordings |
| **OpenAI API** | QAC 386 — key stored in Colab secrets as `OpenAI_Spring_2026`, use QAC386 org |
| **Penn World Table** | Econ 349 term paper data (rgdpna, hc, pop, csh_i, etc.) |
| **World Bank WDI** | Econ 349 term paper supplementary data (SE.PRM.UNER.ZS, etc.) |
| **Stata** | Econ 349 term paper regressions |

## Key Readings (Econ 349)
| Paper | Topic | In Folder |
|-------|-------|-----------|
| Mankiw, Romer & Weil (1992) | Augmented Solow model, human capital | Yes |
| Kremer, Willis & You (2022) | Converging to Convergence | Yes (pp. 337-357 required) |
| Acemoglu, Johnson & Robinson (2001) | Institutions & growth | Yes |
| Hall & Jones (1999) | Income differences | Yes |
| Frankel & Romer (1999) | Trade & growth | Yes |
| Bloom et al. (2020) | Ideas/innovation | Yes |

## Key Readings (Econ 333)
| Paper | Topic |
|-------|-------|
| Yorulmazer (2014) | Case studies on disruptions during 2008 crisis |
| Diamond & Dybvig (1983) | Bank runs model (core of course) |

## OpenClaw Setup
- Installed on Mac and Oracle Cloud Ubuntu server
- Server IP: 129.213.57.108
- Using Moonshot Kimi K2.5 as primary model
- Claude as backup
- Config: `~/.openclaw/openclaw.json`