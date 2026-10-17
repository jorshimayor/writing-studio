---
topic: What the Next.js 15 caching defaults change for existing apps
user_need: Update Me
domain: Web2
channel: blog
profile: jorshimayor
reader: React and Next.js developers upgrading an app from Next.js 14
level: intermediate
primary_keyword: next.js 15 caching
secondary_keywords: [route handlers, client router cache, fetch caching]
title: Next.js 15 Caching Changes: What Breaks And How To Fix It
seo_title: Next.js 15 Caching Changes: What Breaks and How to Fix It
meta_description: Next.js 15 stopped caching fetch requests, GET Route Handlers and page navigations by default. See what changes for your app and how to opt back in.
slug: nextjs-15-caching-changes
cta: Subscribe for upgrade notes on the frameworks you use
target_length: 900 to 1,300 words
keyword_source: autocomplete + SERP
status: example
---

# Next.js 15 Caching Changes: What Breaks And How To Fix It

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | Next.js 15 Caching Changes: What Breaks And How To Fix It | 56 | Update + fix | Covers the full worry |
| 2 | Next.js 15 Stopped Caching By Default: What To Do Now | 52 | News | Urgent framing |
| 3 | Upgrading To Next.js 15? Check These 3 Caching Changes | 53 | Number | Skimmable checklist |
| 4 | Next.js 15 Caching Explained For Next.js 14 Developers | 54 | Audience | Upgrade audience |
| 5 | Why Your Next.js 15 App Got Slower After Upgrading | 49 | Problem-first | Matches symptom searches |
| 6 | Next.js 15 Route Handlers Are No Longer Cached: The Fix | 54 | Specific | Exact change |
| 7 | What Next.js 15 Caching Means For Your Data Fetching | 51 | Implication | Practical |
| 8 | Next.js 15 Caching: Opt-In Patterns That Replace Old Defaults | 59 | Keyword: payoff | Solution searches |

## Reader desires
- I want the change in the first lines.
- I want to know whether it affects my app.
- I want the exact fix.

## Search intent
- Format that ranks: the official release post and upgrade guides.
- Questions to answer: is fetch cached in next 15, are route handlers cached, how to enable caching again.
- Gap: the release post lists the changes, but few pieces map them to "what breaks in my app".

## Intro plan
- Setup: one sentence: Next.js 15 changed three caching defaults from cached to uncached.
- Why it matters now: apps upgraded from 14 may make more requests or feel slower without code changes.
- Transition: here is exactly what changed.

## Outline
### H2: What Changed in Next.js 15 Caching?
- Purpose: the news first, with versions.
- Key points: fetch requests, GET Route Handlers and client navigations are no longer cached by default in Next.js 15. In Next.js 14 they were.
- Keywords: next.js 15 caching; route handlers; client router cache
- Links: [the Next.js 15 release notes](https://nextjs.org/blog/next-15)
#### H3: GET Route Handlers
- Key points: uncached by default in 15; cached by default in 14 unless dynamic.
#### H3: The Client Router Cache
- Key points: page components are no longer reused from the client cache on navigation by default.
#### H3: Fetch Caching
- Key points: fetch requests are no longer cached by default.

### H2: What Next.js 15 Caching Means for Your App
- Purpose: practical impact.
- Key points: more requests to APIs and databases, possibly slower pages, but fresher data and fewer stale-cache bugs. How to check whether your routes are affected.
- Keywords: fetch caching
- Links: [my projects](https://jorshimayor.is-a.dev/projects)

### H2: How To Restore Caching in Next.js 15 Where You Need It
- Purpose: what to do next.
- Key points: opt GET Route Handlers back in with a static route config such as export const dynamic = 'force-static'; opt individual fetch calls into caching; tune the client router cache with the experimental staleTimes flag.
- Links: [the Next.js caching docs](https://nextjs.org/docs/app/building-your-application/caching), [more upgrade notes](https://jorshimayor.is-a.dev/work), [the newsletter](https://jorshimayor.substack.com)

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| my projects | https://jorshimayor.is-a.dev/projects | What It Means |
| more upgrade notes | https://jorshimayor.is-a.dev/work | How To Restore Caching |
| the newsletter | https://jorshimayor.substack.com | How To Restore Caching |

## Sources
- https://nextjs.org/blog/next-15 (the changed defaults, force-static and staleTimes)
- https://nextjs.org/docs/app/building-your-application/caching

## Open questions
- Confirm the exact fetch opt-in option in the current caching docs before publishing, and date the piece.
