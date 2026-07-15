---
name: Course Details - Spring 2026
description: All 4 courses with professor names, textbooks, topics covered, and folder structure
type: project
sessions:
  - 8f6ef573-a64c-4918-834c-5b7d6ea634c0
  - 54dd4efb-7e00-469d-9b2d-02e160e3af35
  - 175baf0c-4ac0-41df-9dcf-a91817b08ca9
  - 2647beef-45ea-4577-992c-5fbd449f92e1
  - e0693d1a-b371-41de-91da-a441ee01e70e
  - 19b3e1b6-0b26-4a32-91c2-6600006039e7
  - e22a61ad-77d5-4374-a719-b7d8db5eac49
  - 9769868f-55d5-45b1-9481-1a8f7281a0b3
  - d5d0c714-5601-4191-862f-d17eb982e133
  - 6efb2481-b890-4754-95b7-49de6ac05f9b
  - 983fedaf-c4fb-41ed-a452-635feada0d8e
  - ead3e4eb-2e2e-4268-824e-15b9aaf8318b
  - 0070da2d-b09f-4ebf-a589-6397a83f8c59
  - 8616969f-68b5-4942-805f-9f73aa6135fb
---

# Course Details - Spring 2026

## Econ 241 - Money, Banking & Financial Markets
- **Professor**: Imai
- **Textbook**: Mishkin, *The Economics of Money, Banking, and Financial Markets*, 13th ed.
- **Notes file**: `Econ 241 - Money, Banking/Econ 241 Notes.md`
- **Textbook PDF**: `Econ 241 - Money, Banking/Econ 241 Textbook.pdf`
- **Syllabus**: `Econ 241 - Money, Banking/syllabus_Econ241_2026.pdf`
- **Exam format**: 16 questions, 2 points each, closed-book
- **Topics covered so far**:
  - Ch 4: Meaning of Interest Rates (PV, YTM, 4 credit instruments, Fisher equation)
  - Ch 5: Behavior of Interest Rates (bond supply/demand, loanable funds, liquidity preference, Fisher effect)
  - Ch 6: Risk & Term Structure of Interest Rates (default risk, risk premium, yield curve, expectations theory, liquidity premium theory, segmented markets)
  - Ch 8: Economic Analysis of Financial Structure (adverse selection, moral hazard, lemons problem)
  - Ch 9: Banking and Management of Financial Institutions
  - Ch 10: Economic Analysis of Financial Regulation
  - Ch 11: Banking Industry Structure

## Econ 333 - Financial Intermediation
- **Professor**: Unknown (course materials use lecture slide PDFs numbered by lecture)
- **Textbook**: Lectures + slides (no single textbook)
- **Notes file**: `Econ 333 - Financial Intermediation/Econ 333 Notes.md`
- **Key readings**: Yorulmazer (2014) case studies on 2008 crisis disruptions
- **Topics covered so far**:
  - Lecture 1: Introduction & why study bank runs (amplification of shocks, 2008 crisis)
  - Lecture 2: Finance preliminaries, bank balance sheets, liquidity, maturity, solvency
  - Lecture 3: Functions of banks (delegated monitoring, secret keepers, maturity transformation)
  - Lecture 4: Optimization (utility, MRS, Lagrangian, consumption-savings choice)
  - Lecture 5: Diamond-Dybvig model setup (autarky vs efficient allocation)
  - Lecture 6: Banking & bank runs (good/bad Nash equilibria, maturity transformation fragility)
- **Key model**: Diamond-Dybvig (1983) — why banks exist and why they're fragile

## Econ 349 - Economic Growth
- **Professor**: Kuenzel
- **Textbook**: Jones & Vollrath, *Introduction to Economic Growth*, 3rd/4th ed.
- **Notes file**: `Econ 349 - Economic Growth/Econ 349 Notes.md`
- **Syllabus**: `Econ 349 - Economic Growth/Econ 349 Spring 2026 Syllabus.pdf`
- **Textbook PDF**: `Econ 349 - Economic Growth/Textbook Econ 349 Jones and Vollrath (2013) Introduction to Economic Growth, 3rd edition.pdf`
- **Key readings folder**: `Econ 349 - Economic Growth/Readings/` containing:
  - Mankiw, Romer & Weil (1992) — augmented Solow model
  - Kremer, Willis & You (2022) — "Converging to Convergence"
  - Frankel & Romer (1999), Feyrer (2019) — trade & growth
  - Acemoglu, Johnson & Robinson (2001) — institutions & growth
  - Hall & Jones (1999) — differences in income
  - Bloom et al. (2020), Romer (1990, 1994) — ideas/innovation
- **Topics covered so far**:
  - JV Ch 2.3-2.4: Solow model dynamics, steady state, transition dynamics, convergence
  - JV Ch 3.2-3.3, 3.5: Technology & growth, growth accounting
  - JV Ch 7.1: Human capital model (h = e^(mu*E)), development accounting
  - Lectures 4-5: Comparative statics, golden rule, growth/development accounting
  - Lectures 6-7: MRW (1992) empirics, convergence (unconditional vs conditional)
  - Lectures 8-9: Innovation function dA = theta*L_R^lambda*A^phi, endogenous growth
- **Term paper**: Empirical paper with own regressions (Stata). Naomi's topic: education & GDP growth in Nigeria (out-of-school children)

## QAC 386 - Text Mining
- **Professor**: Unknown (uses Google Colab, provides OpenAI API access under QAC386 organization)
- **Textbook**: No single textbook; Python/pandas/regex taught via Colab notebooks
- **Notes file**: `Qac 386 - Text Mining/QAC 386 Notes.md`
- **Platform**: Google Colab with Google Drive integration
- **API setup**: OpenAI API key stored in Colab secrets as `OpenAI_Spring_2026`, must use QAC386 organization
- **Topics covered so far**:
  - Python basics: list comprehensions, dictionaries, tuples
  - Pandas: DataFrames, `.loc`, `.iloc`, `.str.extract()`, `.str.contains()`, `.groupby()`, `.rolling()`, Boolean slicing
  - Regex: capture groups `()`, raw strings `r''`, backreferences `\1`, `.sub()`, lookbehinds `(?<=)`, `re.findall`, `re.search`
  - OpenAI API: `[REDACTED:sensitive-label]()` with gpt-5-nano/gpt-4.1-mini
  - PDF text extraction with PyMuPDF (fitz)
  - Class data: Wesleyan Argus newspapers (1964-1988), CT COVID data, weather data

## Folder Structure
```
~/Library/CloudStorage/OneDrive-wesleyan.edu/Classes/
├── Econ 241 - Money, Banking/
│   ├── Econ 241 Notes.md
│   ├── Econ 241 Textbook.pdf
│   ├── syllabus_Econ241_2026.pdf
│   ├── Problem Set 2-4.pdf + Solution Keys
│   └── Lessons/ (lesson scans, notes.md)
├── Econ 333 - Financial Intermediation/
│   ├── Econ 333 Notes.md
│   ├── Lecture #1-6 S26 Moodle.pdf
│   ├── Problem set #2 Spring 2026.pdf
│   └── Readings (Yorulmazer 2014, etc.)
├── Econ 349 - Economic Growth/
│   ├── Econ 349 Notes.md
│   ├── Lecture 1-8 handout.pdf
│   ├── Problem Set 1-2.pdf + PS2 Answers.md
│   ├── Econ 349 Paper Assignment.pdf
│   └── Readings/ (MRW 1992, Kremer 2022, AJR 2001, etc.)
├── Qac 386 - Text Mining/
│   ├── QAC 386 Notes.md
│   ├── qac386_s26_hw1.ipynb
│   └── Classes/ (day1-day3 notebooks)
├── Transcripts/ (Tactiq auto-save destination)
│   └── Econ 241/ (class recording transcripts)
└── Social Impact/
```
