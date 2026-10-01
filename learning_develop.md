# Learning Development Plan – From 100 Days to a High-Impact Learning Repository

> **Scope.** This plan starts *after* all 100 syllabus days are complete. It
> describes how to turn `pro-python-mastery` from a personal challenge into a
> public, sponsor-backed Python course that learners trust, contributors
> improve and companies want to support.
>
> **Status when this plan was written (Oct 2026):** Days 01–63 are complete
> (code + tests + reflection, kept in sync by CI). Days 64–100 are planned.

---

## 1. Vision and success criteria

**Vision:** *The most trustworthy free path from "first variable" to
"production-ready Python engineer" – every lesson is runnable, tested and
honest about what it covers.*

**Who it serves**

| Audience | What they need | What we give them |
|---|---|---|
| Self-taught beginners | A clear path, small wins, no setup pain | One-click environment, 15–45 min days, instant feedback from tests |
| Career switchers / bootcamp grads | Proof of skill for job applications | Graded exercises, capstone portfolio projects, completion certificate |
| Working developers | Fill gaps (typing, async, testing, packaging) | Advanced track (Days 64–100) usable à la carte |
| Teachers and mentors | Ready-made, reliable material | Licence to reuse, slides/notes per day, cohort guide |
| Companies (sponsors) | Brand trust, hiring pipeline, upskilling content | Sponsorship tiers with transparent, ethical benefits |

**North-star metric:** *learners who finish a capstone (Day 83+) per month.*

**Supporting metrics (reported publicly every quarter)**

| Area | Metric | 6-month target | 12-month target |
|---|---|---|---|
| Reach | GitHub stars / unique docs visitors per month | 1 000 / 5 000 | 5 000 / 25 000 |
| Engagement | Learners passing Day 24 / Day 56 / Day 100 exercises (opt-in progress badge) | 500 / 150 / 30 | 3 000 / 900 / 250 |
| Quality | Content-error issues closed within 7 days | ≥ 80 % | ≥ 90 % |
| Community | Monthly active contributors (merged PRs) | 10 | 40 |
| Sustainability | Recurring sponsorship per month | $500 | $3 000 |

---

## 2. Baseline – what already makes this repo strong

Build on these; don't rebuild them.

1. **A single source of truth that CI enforces.** `tests/test_syllabus_sync.py`
   fails the build if a *Covered* day lacks code, tests that import it,
   resolvable `DELIVERABLES`, or an up-to-date reflection. Status can't lie.
2. **A unique scenario per day** (badge printer, bill splitter, REST to-do API
   and so on), with a uniqueness check in CI.
3. **Tests as documentation:** more than 1 000 tests at 99 % line coverage,
   run on Python 3.12–3.14, plus ruff and mypy in CI.
4. **Security hygiene by default:** no `eval` on input, secrets only from the
   environment, `secrets` for passwords, sandboxed file operations, atomic
   writes, network and SMTP always mocked in tests.

**Gaps to close for public use**

| Gap | Why it matters |
|---|---|
| All work lives on `master`, while the default branch `main` is empty | Visitors see an empty repo and the CI badge has nothing to report |
| No exercises – learners read solutions | Reading isn't learning; we need "your turn" tasks with automatic feedback |
| No docs website | GitHub file browsing is a poor reading experience on mobile |
| No community files (CONTRIBUTING, Code of Conduct, templates) | Contributors don't know how to help safely |
| No funding or governance model | Sponsors need clarity on what they fund and what they can't influence |

---

## 3. Phased roadmap

| Phase | Window (after Day 100) | Theme | Exit criteria |
|---|---|---|---|
| **A** | Weeks 0–4 | Foundation hardening | Default branch fixed, v1.0.0 tagged, security scanning, contributor docs |
| **B** | Months 1–3 | Learner experience | Docs site live, exercises for Days 1–56, Codespaces one-click, progress CLI |
| **C** | Months 2–6 | Community engine | 40+ "good first issues", review rota, monthly release cadence, Discussions active |
| **D** | Months 3–6 | Sponsorship and sustainability | FUNDING.yml, GitHub Sponsors and Open Collective, first 3 sponsors, public budget |
| **E** | Months 6–12 | Scale and impact | Exercises for all 100 days, cohort programme, 2 translations, certificate, annual impact report |

### Phase A – Foundation hardening (weeks 0–4)

1. **Fix the branch layout.** Merge `master` into `main` with
   `--allow-unrelated-histories` (or make `master` the default), protect the
   default branch, require CI and one review, and delete stale branches.
2. **Tag `v1.0.0`** when Day 100 lands; follow semantic versioning:
   - *major*: syllabus restructure
   - *minor*: new day or exercise set
   - *patch*: fixes
3. **Supply-chain and security tooling:**
   - Dependabot (pip + GitHub Actions), `pip-audit` in CI, CodeQL, `bandit -r src`
   - pin Actions by SHA
   - `SECURITY.md` with a private reporting route
4. **Quality ratchet:**
   - `pre-commit` (ruff, ruff-format, mypy, end-of-file fixer)
   - coverage gate raised from 85 % to 95 %
   - mutation testing (`mutmut`) on a weekly schedule, to find tests that assert too little
   - `hypothesis` property tests for numeric and parsing days (5, 7, 40, 43, 52)
5. **Community files:**
   - `CONTRIBUTING.md` covering the day structure, `DELIVERABLES` rules and running `./propython.sh`
   - `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
   - issue templates: *content error*, *bug*, *new exercise*, *new scenario idea*
   - a PR template
6. **Licensing clarity:** keep code under MIT and put lesson prose under
   CC BY 4.0, so teachers can reuse the text with attribution.

### Phase B – Learner experience (months 1–3)

**B1. Exercises with automatic feedback**

Add an `exercises/` tree that mirrors `src/`:

```text
exercises/day_18_dictionaries_lists/
├── README.md          # the task, hints (collapsed), acceptance criteria
├── starter.py         # function signatures + docstrings, bodies raise NotImplementedError
└── test_exercise.py   # imports starter.py; marked @pytest.mark.exercise
```

* `pytest -m exercise exercises/day_18*` gives instant pass/fail feedback.
* Three tiers per day:
  - **Practice:** repeat the concept in a new context.
  - **Stretch:** combine it with an earlier day.
  - **Challenge:** open-ended, with no tests, solved in Discussions.
* Reference solutions live in `src/` already, so exercise scenarios must
  differ from the lesson scenario. Extend the CI uniqueness check to cover
  exercise scenarios too.

**B2. Progress CLI (`ppm`)**

* `ppm start 18` copies the starter files into a git-ignored `workspace/`.
* `ppm check 18` runs the exercise tests and shows friendly hints on failure.
* `ppm progress` prints a 100-cell heat-map of completed days, stored locally
  only (no telemetry).
* `ppm badge` writes an SVG badge learners can put on their own profile; it is
  self-reported and honest about that.

**B3. Documentation site**

* MkDocs Material, generated from `docs/progress/*`, the module docstrings
  (via `mkdocstrings`) and the exercise READMEs.
* In-browser runnable examples with Pyodide (JupyterLite) for Days 1–24, so
  beginners can start without installing anything.
* Search, dark mode, "previous / next day" navigation, and estimated time and
  difficulty per day.
* Accessibility: alt text for every diagram, contrast-checked palette, and
  keyboard-only navigation tested.

**B4. Zero-setup environments**

* `.devcontainer/` for GitHub Codespaces and VS Code, with Tk installed for
  Days 37 and 48.
* A "Open in Codespaces" badge per day in the README index.

**B5. Learning-science upgrades**

* **Retrieval practice:** a five-question quiz at the end of each day,
  stored as YAML, rendered on the site and checked by `ppm quiz 18`.
* **Spaced repetition:** "flashback" questions that resurface Day N
  concepts on Days N+3, N+10 and N+30.
* **Cumulative projects:** Days 24, 56, 63 and 100 become checkpoint
  projects that reuse earlier days' code, so learners see the pieces fit
  together.
* **Common-mistakes gallery:** each reflection's "Pitfalls" section links
  to a runnable snippet that reproduces the mistake, plus its fix.

### Phase C – Community engine (months 2–6)

| Practice | Implementation |
|---|---|
| Good first issues | Seed 40+ small, well-specified tasks: an extra edge-case test, a clearer hint, an exercise for a single day |
| Review rota | 3–5 maintainers rotating weekly; first response target 72 h, documented in `MAINTAINERS.md` |
| Content RFCs | Changes to the syllabus or teaching approach go through a short RFC in `docs/rfcs/` and are discussed for 7 days |
| Recognition | The `all-contributors` bot, monthly "contributor spotlight" in Discussions, and contributors listed in release notes |
| Release cadence | Monthly minor release with a changelog (`CHANGELOG.md`, Keep a Changelog format) |
| Communication | GitHub Discussions categories: Q&A (per phase), Show & Tell (capstones), Ideas, Announcements |
| Mentorship | "Study buddy" threads per cohort; experienced learners answer Day 1–24 questions to earn a *Mentor* role |
| Translations | Crowdin or Weblate for the docs site; start with Hindi and Spanish, plus one more chosen by contributor demand |

**Content quality gate**

Every new or changed day must pass:

1. the CI sync test;
2. a pedagogy checklist (a new scenario, every deliverable mapped, ≥ 5 tests,
   pitfalls from real mistakes);
3. a technical review by one maintainer;
4. a "fresh eyes" review by someone who hasn't seen the topic before.

### Phase D – Sponsorship and sustainability (months 3–6)

**D1. Principles (published as `SPONSORS.md`)**

1. Sponsors **never** influence lesson content, rankings or recommendations.
2. Every sponsor is disclosed; there are no paid placements inside lessons.
3. Funds are spent transparently through Open Collective; the budget and
   spending are public.
4. No learner data is ever shared or sold. The project collects no tracking
   data beyond privacy-friendly, aggregate docs analytics (Plausible or
   GoatCounter).

**D2. Funding channels**

| Channel | Purpose |
|---|---|
| GitHub Sponsors (individual) | Recurring small support from learners and developers |
| Open Collective (fiscal host, e.g. Open Source Collective) | Company invoices, transparent ledger, tax handling |
| Grants | PSF grants, GitHub Accelerator, education programmes, local tech-community funds |
| Corporate training licence (optional, later) | Companies run private cohorts using the material, which stays free and public |

Add `.github/FUNDING.yml`:

```yaml
github: [OdeToTheWind]
open_collective: pro-python-mastery
```

**D3. Sponsor tiers**

| Tier | Monthly | Benefits (none affect content) |
|---|---|---|
| Supporter | $5 | Name in `SPONSORS.md`, sponsor badge on GitHub |
| Backer | $25 | Above, plus early access to new exercise sets (one-week preview) |
| Bronze (company) | $250 | Small logo in README and on the docs site footer, thank-you in release notes |
| Silver (company) | $750 | Medium logo, a "Sponsored track" credit on one capstone (for example "Day 93 async service, supported by …"), quarterly impact report |
| Gold (company) | $2 000 | Large logo, a hiring-board post per quarter in Discussions (clearly labelled), co-hosted live session per year, and naming of a scholarship cohort |
| Scholarship sponsor | One-off | Funds devices, data plans or certification fees for learners from under-represented groups |

**D4. Where the money goes**

The ledger is published on Open Collective.

| Share | Use |
|---|---|
| 40 % | Maintainer time: reviews, new content, releases |
| 20 % | Learner scholarships and community events |
| 15 % | Accessibility and translation work |
| 15 % | Infrastructure (docs hosting, CI minutes, domain) and security audits |
| 10 % | Contributor bounties for priority issues |

**D5. Pitch outline for sponsors**

This reads well as a one-page PDF or a 6-slide deck.

1. **Problem:** learners can't tell which free Python material is accurate
   and current.
2. **Solution:** a course that CI keeps honest, with tests for every lesson.
3. **Proof:**
   - completed days
   - test and coverage numbers
   - learner growth chart
   - three learner stories
4. **Audience:** where the learners come from and the levels they reach
   (from privacy-friendly aggregates only).
5. **Benefits:** the tiers above, plus the ethics guarantee.
6. **Ask:** the tier, the duration and the contact.

**D6. Outreach plan**

* **Warm start:** companies whose libraries the course already teaches.
  Days 44 and 57–63 use pandas, requests, BeautifulSoup and Selenium; the
  planned Days 76 and 79 add aiohttp and packaging tools. The same goes for
  developer-tool companies (editors, CI, hosting such as PythonAnywhere for
  Day 56).
* **Community:** local Python user groups, PyCon India, PyCon US and
  EuroPython; give a lightning talk on the CI sync guard and how it keeps
  course status accurate.
* **Cadence:** 10 personalised emails per month; track them in a simple CRM
  board (a GitHub Project); follow up after 10 days.
* **Retention:** send each sponsor a quarterly impact report covering the
  north-star metric, content shipped and community growth.

### Phase E – Scale and impact (months 6–12)

1. **Exercises for all 100 days**, with each capstone (Days 83–100) graded
   by a rubric in addition to tests.
2. **Cohort programme:** four cohorts per year, 12 weeks each, run through
   Discussions with weekly office hours and peer code review.
3. **Certificate of completion:** issued when a learner's public
   capstone repo passes an automated checker (tests, coverage, lint,
   packaging) plus a human review of the README. Use Open Badges 3.0 so
   certificates are verifiable.
4. **Teacher kit:** slides per phase, a 12-week syllabus mapping, and
   assessment rubrics for classroom use.
5. **Annual impact report:** learners, completions, scholarships funded,
   contributor growth and money in and out.

---

## 4. Content standards (apply to every day, old and new)

| Standard | Rule | Enforced by |
|---|---|---|
| Unique scenario | Each day models a different real-world situation; exercises use yet another one | `test_scenarios_are_unique_per_day` (extend it to exercises) |
| Complete deliverables | Every syllabus item maps to code in `DELIVERABLES` | `test_covered_day_has_code_with_resolvable_deliverables` |
| Tests teach | ≥ 5 tests per day, covering boundaries and failures, with no placeholder assertions | `test_covered_day_tests_exercise_src` |
| Honest reflections | Generated from code + notes; no hand-typed metrics | `test_reflection_is_generated_from_current_code` |
| Safe by default | No `eval` on input, no real network/SMTP in tests, secrets only from env, `tmp_path` for files | Code review checklist + `bandit` |
| Readable | Type-hinted, docstrings with an example where useful, ≤ ~180 lines per day module | ruff, mypy, review |
| Accessible | Plain English, short sentences, glossary links for jargon, alt text | Docs review checklist |

---

## 5. Engineering roadmap (CI/CD and tooling)

| Item | Phase | Notes |
|---|---|---|
| Branch protection + required checks | A | CI matrix 3.12–3.14 must pass |
| Dependabot + `pip-audit` + CodeQL + `bandit` | A | Weekly schedule; fail on high-severity issues |
| `pre-commit` hooks | A | Same tools as CI, so feedback happens before push |
| Coverage ratchet 85 → 95 % | A | Never allow it to decrease |
| Mutation testing (`mutmut`) | A–B | Weekly job; publish the surviving mutants as issues |
| Docs build + link checker (`lychee`) | B | Runs on every PR touching `docs/` |
| Notebook/JupyterLite build | B | Generated from day modules; never hand-edited |
| Exercise test runner (`pytest -m exercise`) | B | Separate CI job; starters must *fail* their tests, solutions must pass |
| Release automation | C | `release-please` or manual tags plus a generated changelog |
| Performance benchmarks | E | `pytest-benchmark` for Days 80, 90 and 95 to keep perf lessons accurate |

---

## 6. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Maintainer burnout | High | High | Review rota, sponsor-funded maintainer time, scope freeze before releases |
| Content drifts from Python releases | Medium | Medium | CI on the newest Python plus a yearly "Python version" review issue |
| Third-party sites used in lessons change (httpbin, quotes.toscrape) | Medium | Medium | Lessons never depend on them in tests; mirror the practice pages in `tests/fixtures/` |
| Sponsor conflict of interest | Low | High | Published sponsorship principles; maintainers can decline any sponsor |
| Low-quality or AI-generated drive-by PRs | Medium | Medium | Templates requiring tests and a stated motivation; the sync test rejects incomplete days |
| Security issue in examples copied into real projects | Low | High | Safe defaults, `SECURITY.md`, explicit "for learning" notes where shortcuts exist |
| Learners stall after the beginner phase | High | Medium | Checkpoint projects, cohort support, spaced-repetition flashbacks |

---

## 7. Twelve-month timeline

| Month | Milestones |
|---|---|
| 0 | Day 100 merged · v1.0.0 tagged · default branch fixed · security tooling on |
| 1 | CONTRIBUTING / CoC / templates · 20 good-first-issues · FUNDING.yml · Sponsors page live |
| 2 | Docs site v1 (Days 1–56) · Codespaces devcontainer · exercises for Days 1–24 |
| 3 | `ppm` CLI · exercises for Days 25–56 · first sponsor outreach wave · Open Collective live |
| 4 | Quizzes + flashbacks · first cohort (beta, 30 learners) · first quarterly impact report |
| 5 | Exercises for Days 57–82 · first translation (Hindi or Spanish) · conference talk submitted |
| 6 | Checkpoint projects at Days 24/56/63 · coverage gate 95 % · mutation testing in CI |
| 7–8 | Capstone rubric + automated checker · second cohort · scholarship programme launched |
| 9–10 | Certificate (Open Badges) · teacher kit · second translation |
| 11 | Exercises for Days 83–100 complete · performance benchmarks |
| 12 | Annual impact report · v2.0.0 (exercises + certificate) · roadmap for year two |

---

## 8. First two weeks after Day 100 – action checklist

- [ ] Make the branch with the course content the default branch; protect it; require CI
- [ ] Tag `v1.0.0` and publish release notes listing all 100 days
- [ ] Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SPONSORS.md`, `.github/FUNDING.yml`
- [ ] Add issue and PR templates; label 20 good-first-issues
- [ ] Enable Dependabot, CodeQL, `pip-audit`, `bandit` in CI
- [ ] Add `.devcontainer/` and an "Open in Codespaces" badge
- [ ] Draft the one-page sponsor pitch and the first outreach list (10 companies)
- [ ] Create GitHub Discussions with the four categories in Phase C
- [ ] Write the first three exercises (Days 1–3) to validate the exercise format end to end

---

## Appendix A – Per-phase enhancement backlog

| Phase of the course | Enhancement ideas |
|---|---|
| Beginner (1–24) | Pyodide "run in browser" for every day · visual explainers (memory diagrams for Day 06 aliasing, LEGB diagram for Day 23) · beginner glossary · a "debug this" exercise for each day |
| Intermediate (25–56) | Pair-programming katas · a refactoring exercise per OOP day (27–39) · a mini-project tying files, CSV, JSON and persistence (41–53) together · a deployable app gallery for Day 56 |
| API & automation (57–63) | Local mock servers (pytest-httpserver) for offline practice · rate-limit and retry simulations · scraping ethics quiz · a recorded Selenium run for learners without a browser |
| Advanced (64–82) | Visual generator/async timelines · profiling challenges with leaderboards · a typed-API exercise checked by mypy in CI |
| Capstone (83–100) | Rubric-graded projects · peer review guide · "ship it" checklist (packaging, docs, CI) · showcase page for learner capstones |

## Appendix B – Sponsor impact report template (quarterly)

1. Headline numbers (north-star metric, completions by phase, scholarships funded)
2. Content shipped (days, exercises, translations) with links
3. Community health (contributors, response times, issues closed)
4. Learner stories (with consent)
5. Finances (income, spending by category, balance)
6. Next quarter's goals and where help is needed
