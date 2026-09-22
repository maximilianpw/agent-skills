# GPT-6 Astra and Sol: routing research

**Updated 2026-09-22.** First-party names and prices are from OpenAI docs. Community notes are labeled as direct user reports, not benchmark facts. GPT-6 Sol and Luna launched the same day as this note, so Sol-specific user consensus is hours old.

These are not private aliases. OpenAI’s public catalog is **GPT-6 Astra**, **GPT-6 Sol**, and **GPT-6 Luna**. There is **no GPT-6 Terra**.

## Names and variants

| Public name | API / Codex ID | Role | First-party status |
|---|---|---|---|
| **GPT-6 Astra** | `gpt-6-astra` | Flagship. “Most capable model, built for the hardest end-to-end work.” | Generally available from **2026-09-03**. [Models index](https://developers.openai.com/api/docs/models), [Codex models](https://learn.chatgpt.com/codex/models), [HN launch](https://news.ycombinator.com/item?id=49554643) |
| **GPT-6 Sol** | `gpt-6-sol` | Mid-tier. “Built to power complex coding and agentic workflows.” | Launched **2026-09-22** in API, ChatGPT Work, and Codex. Not in Chat. [Sol/Luna launch](https://openai.com/index/introducing-gpt-6-sol-and-luna/) |
| **GPT-6 Luna** | `gpt-6-luna` | Cheap. “Most efficient model for focused, high-volume tasks.” | Same launch as Sol. Free/Go: desktop only. [Codex what’s new](https://learn.chatgpt.com/codex/whats-new#choose-gpt-6-sol-and-luna) |
| **GPT-5.6 Sol / Terra / Luna** | `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` | Previous generation. Terra has no GPT-6 successor. | Still listed and priced. [Pricing](https://developers.openai.com/api/docs/pricing), [Terra model page](https://developers.openai.com/api/docs/models/gpt-5.6-terra) |

OpenAI’s current default recommendation is Astra for complex reasoning and coding, Sol to balance intelligence and cost, Luna for high-volume work. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)

Codex Power presets, when rolled out: Luna High, Sol Light (starting preset), Sol Medium, Astra Light, Astra Medium, Astra Extra High. Codex says start **Medium for Sol, High for Luna, Light (`low`) for Astra**. [Codex models](https://learn.chatgpt.com/codex/models)

Amp is a third-party harness, not an OpenAI product. With a linked ChatGPT subscription, Amp’s current Dial puts **GPT-6 Astra** on `high` (main agent, medium effort) and as Oracle in several modes; `ultra` stays Claude Fable 5.1. [Amp Dial](https://ampcode.com/docs/the-dial), [Amp Modes & Models](https://ampcode.com/models)

## Official capabilities

All three GPT-6 models: text+image in, text out; 1.05M context; 922k max input; 128k max output; Responses and Chat Completions; tools include functions, web search, file search, computer use, code interpreter, apply_patch, skills, MCP, tool_search. [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)

Reasoning effort:

- Astra: `low`, `medium`, `high`, `xhigh`, `max`. **No `none`.**
- Sol and Luna: `none`, `low`, `medium` (default), `high`, `xhigh`, `max`.
- Astra tool calling needs the Responses API. Sol/Luna function-calling on Chat Completions only with `reasoning_effort: "none"`.
- EU data residency is Standard processing only. Fast mode is 2x rates; Astra Fast has no latency SLA. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)

OpenAI’s Astra behavior notes, which matter for routing:

- Stronger long-task coherence than GPT-5.6 Sol, and **more likely to ask** when an answer could change the outcome. That can stall work users expected to continue.
- More sensitive to `AGENTS.md` and skills; audit those files.
- Tends toward lists, tables, Markdown, and recurring phrases.
- May under-delegate to subagents unless prompted.
- Coding: thorough testing; can over-test small changes.
- New platform features: async tool calling, mid-turn steering, mid-conversation reasoning changes that preserve cache, misalignment monitoring. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)

Safety, not a coding score: OpenAI designated Astra **Critical** for cybersecurity under its Preparedness Framework and added production misalignment monitoring that can pause ChatGPT/Codex work or stop API tasks. CoT monitorability is lower than previous models. [Path to Astra](https://openai.com/index/path-to-astra/), [system card excerpt](https://deploymentsafety.openai.com/gpt-6-astra)

Vendor evals, not independent proof:

- OpenAI: Astra is SOTA on computer use, browsing, SWE, science, and professional work, with **fewer output tokens** so estimated cost per task can beat older models despite higher per-token prices. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)
- Sol launch: GPT-6 Sol (xhigh) 33.2% AutomationBench at $0.27/task vs Opus 5 max 26.9% at 11.1× Sol cost; DeepSWE v1.1 Sol max **68.8%** vs Fable 5 xhigh 69.9% at ~80% lower cost; Luna max 66.6%. FrontierCode: Sol improved over 5.6 Sol and matched Fable 5.1 xhigh at lower cost. [Sol/Luna launch](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
- Independent (Artificial Analysis, 2026-09-09): Astra **ties Fable 5.1** on Intelligence Index (53) and Coding Agent Index (62). Coding Agent cost ~40% below Fable and ~30% below Opus 5 at similar/higher score. Token use at max ~1/3 of Fable. Hallucination rate 92% → 51% on AA-Omniscience. Presentation Quality Elo still led by GPT-5.6 Sol. DeepSWE 68% vs 5.6 Sol 72%. GDPval-AA dropped, with fewer turns (24 vs 45 for 5.6 Sol). [AA article](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
- CodeRabbit (vendor eval, not a public leaderboard): Astra caught ~4% more labeled bugs than 5.6 Sol and ~22% more than Opus 5; cross-file subset +20% / +33%. They treat this as directional. [CodeRabbit](https://www.coderabbit.ai/blog/gpt-6-astra-code-review-evaluation)

## Pricing and limits

USD per 1M tokens, Standard, short context (<272k). Long context is 2× input/cache and 1.5× output for the full request. Cached input is 10% of input; cache writes 1.25× input. Batch/Flex 50%; Fast 2×. [Pricing](https://developers.openai.com/api/docs/pricing)

| Model | Input | Cached in | Cache write | Output |
|---|---:|---:|---:|---:|
| GPT-6 Astra | $10 | $1 | $12.50 | $50 |
| GPT-6 Sol | $2 | $0.20 | $2.50 | $10 |
| GPT-6 Luna | $0.10 | $0.01 | $0.125 | $0.50 |
| GPT-5.6 Sol | $4 | $0.40 | $5 | $20 |
| GPT-5.6 Terra | $2 | $0.20 | $2.50 | $12 |
| GPT-5.6 Luna | $0.20 | $0.02 | $0.25 | $1.20 |
| Grok 4.6 (<200k) | $2 | $0.50 | — | $6 |
| Claude Opus 5 | $5 | $0.50 | $6.25 | $25 |
| Claude Fable 5.1 | $10 | $0.25 | $12.50 | $50 |

Grok: [xAI grok-4.6](https://docs.x.ai/developers/models/grok-4.6). Claude: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing). OpenAI says GPT-6 Sol/Luna are **50% cheaper than GPT-5.6 promotional prices**. 5.6 Sol promo pricing lasts at least through **2026-11-21**.

Codex/ChatGPT Work share usage. Plus local-message estimates per 5 hours: Astra **5–45**, GPT-6 Sol **15–150**, GPT-6 Luna **350–3,000**, 5.6 Sol **10–100**, Terra **25–200**. Credits per 1M tokens (Standard): Astra 250/25/1,250; GPT-6 Sol 50/5/250; GPT-6 Luna 2.5/0.25/12.5. Fast is 2.5× those credit rates. Plus includes Sol and Luna; Astra is on the usage table for Plus but burns the allowance fastest. [Codex pricing](https://learn.chatgpt.com/codex/pricing)

API rate limits for Astra/Sol (Standard): Tier 1 500 RPM / 500k TPM, up to Tier 5 15k RPM / 40M TPM. Luna TPM is higher (Tier 5 180M). [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)

## Local catalog (non-secret)

Pi’s `openai-codex` catalog still lists `gpt-5.6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-6-astra` (272k context estimate, Astra $10/$50). It does **not** yet list `gpt-6-sol` or `gpt-6-luna`. Bedrock/OpenCode/Radius already advertise `gpt-6-astra`.

Local Pi settings already enable `cliproxyapi/gpt-6-astra`, `cliproxyapi/gpt-6-sol`, and `cliproxyapi/gpt-6-luna` alongside the 5.6 Sol/Luna IDs. Treat `gpt-6-sol` as the intended Sol ID once the proxy/catalog catch up; do not assume `gpt-5.6-sol` was silently renamed.

Quota mapping implication for the routing skill: the `codex` family now includes Astra, which is several times more expensive per message than Sol. A quota check that only asks “is Codex available?” will overstate how much Astra work the remaining allowance can support.

## Community / user reports about Astra

These are anecdotes. They are not evals. They disagree.

**Taste / communication.** Recurring positive: Astra is less “Claudeish” and more direct. One Pi user called Astra’s terse factual style “a breath of fresh air” versus Claude ([HN](https://news.ycombinator.com/item?id=49796064)). Another switched from Claude to Astra because they wanted a professional coding voice ([HN](https://news.ycombinator.com/item?id=49792117)). Recurring negative: AA’s Presentation Quality Elo still favors 5.6 Sol; one OpenAI user called Astra “horrible” on a design-doc project (duplicated lines, unsolicited edits, poor prose) and went back to 5.6 Sol ([HN](https://news.ycombinator.com/item?id=49791214)). OpenAI itself warns about lists, stock phrases, and over-formatting.

**Efficiency, cost, speed.** Per-token Astra is 2.5× 5.6 Sol and matches Fable 5.1. AA says Astra is token-efficient enough that **cost per task** can undercut Fable. Subscription users still report Astra as slow and quota-heavy: “usable for coding but slow and very expensive”; copy-editing burned 70% of a Pro allowance ([HN](https://news.ycombinator.com/item?id=49802834)). Another: 5.6 Sol xhigh was the workhorse until rate limits started hitting Astra/Sol/Luna before weekly caps ([HN](https://news.ycombinator.com/item?id=49799215)). Simon Willison’s max pelican SVG: 4m02s, $0.63 ([HN](https://news.ycombinator.com/item?id=49570643)). Codex Plus estimates put Astra at roughly 1/3 the message budget of GPT-6 Sol.

**Task completion / reliability.** Official docs already say Astra asks more and may stop. Direct reports match that, plus some failure modes shared with 5.6 Sol: out of scope, premature stop, odd/dangerous workarounds ([HN](https://news.ycombinator.com/item?id=49790550)). Same-day Sol-launch comments: 5.6 Sol still preferred for ~9/10 daily tasks; Astra better for ambitious features; Astra felt like a **downgrade** when extra intelligence was not needed ([HN Sol/Luna thread](https://news.ycombinator.com/item?id=49805509)). One user found Astra “horrible at making orchestration decisions” and uses Fable until the limit, then Astra ([same thread](https://news.ycombinator.com/item?id=49805767)). OpenAI alignment evals claim fewer misleading coding claims than 5.6 Sol; that is a vendor claim, not user consensus.

**Coding.** Split, not a landslide. Positive: “first one that feels as good as Fable,” and less annoying in replies, but no cheaper OpenAI drop-in like Opus ([HN](https://news.ycombinator.com/item?id=49798106)). AA ties Fable on the Coding Agent Index; CodeRabbit’s cross-file review gain is the strongest independent-ish coding signal. Negative: “No, Astra isn’t better for coding. I’ve switched back to Sol” ([HN](https://news.ycombinator.com/item?id=49791503)); “Fable seems better for hardcore coding,” Astra for creative work ([HN](https://news.ycombinator.com/item?id=49805437)); DeepSWE slightly below 5.6 Sol in AA. Computer use / 3D is a commonly cited Astra strength even among people who stopped using it for coding ([HN](https://news.ycombinator.com/item?id=49790550)).

**Judgment / best use.** Users and OpenAI agree on *when* Astra is worth it: long, multi-step, cross-file, computer-use, research, ambitious features. They do not agree it should be the daily coding model. Proposed “Astra orchestrates, Sol implements” pattern appeared immediately on the Sol launch thread and was contradicted in the next comment. Amp already encodes a similar split: Astra on `high` / Oracle, Fable on `ultra`, Sol on `medium`.

**GPT-6 Sol (same-day only).** HN reaction is mostly price: Sol $2/$10 is 50% below 5.6 Sol and far below Opus 5 / Fable. Several people who liked 5.6 Sol’s “feel” worry the successor will be technically better but worse to work with. One commenter already plans to use Sol 6 as a high-volume weekly model because Astra was too expensive and 5.6 Luna too weak ([HN](https://news.ycombinator.com/item?id=49805619)). There is not yet a coding-quality consensus for GPT-6 Sol.

## Routing recommendations

Personal-cost scale in the skill is 1 cheap → 10 expensive. Scores below are routing priors, not AA/OpenAI numbers.

### Suggested grading row

Current skill already lists GPT-6 Sol at cost 7, which matched **GPT-5.6 Sol** API/subscription cost, not GPT-6 Sol’s $2/$10.

| model | personal cost | judgment | code | taste | note |
|---|---:|---:|---:|---:|---|
| Luna | 1 | 5 | 6 | 4 | Prefer **GPT-6 Luna** when the catalog has it; 5.6 Luna remains the fallback ID |
| Grok 4.6 | 2 | 8 | 9 | 7 | Still the cheapest strong coding loop ($2/$6). Keep as high-volume implementer |
| GPT-6 Sol | **4** | 9 | 9 | **7** | Cost should drop from 7. Taste up one vs 5.6 Sol because OpenAI shipped Astra’s communication style to Sol; unverified in use |
| **GPT-6 Astra** | **9** | **9** | **9** | **7** | New row. Cost near Opus/Fable per token; often cheaper per hard task than Fable if token-efficient. Not a taste winner vs Opus |
| Opus 5 | 10 | 8 | 7 | 9 | Keep for product/UI/copy. Fable 5.1 is the closer Astra peer on price/capability, but the skill’s Claude route is still Opus |

### Suggested routes

Keep Grok on the complete code loop. Do not promote Astra to daily implementation.

| responsibility | primary | fallback |
|---|---|---|
| trivial mechanical edit with an obvious check | Luna (GPT-6 Luna if available) | Grok 4.6 |
| bounded analysis or routine edit with explicit scope and checks | **GPT-6 Luna** | Grok 4.6 |
| repository exploration, code planning, implementation, refactoring, migrations, tests, reproducible debugging, performance | Grok 4.6 | **GPT-6 Sol** |
| routine code review and verification | Grok 4.6 | **GPT-6 Sol** |
| cross-cutting high-risk implementation or non-reproducible technical debugging | **GPT-6 Sol** | Grok 4.6; **escalate to Astra** only after Sol/Grok stall or the work is long-horizon / computer-use |
| technical architecture | **GPT-6 Sol** | **GPT-6 Astra** (Opus 5 remains fine if the question is product-shaped) |
| product architecture, UI, copy, and subjective API design | Opus 5 | GPT-6 Sol. **Do not make Astra primary** — presentation/taste reports are mixed and AA still prefers 5.6 Sol on presentation |
| independent code or security review | **GPT-6 Astra** for Grok or Sol work; Grok 4.6 for Astra, Luna, or Opus work | the other of Grok 4.6 or GPT-6 Sol |
| independent architecture or design review | Opus 5 for Sol/Astra work; **GPT-6 Astra** for Opus work | the other of Opus 5 or GPT-6 Sol |

Amp-specific: if the thread is already on Astra, use Amp’s built-in **`high`** rather than inventing a custom Astra pin. That matches both Amp’s current Dial and the global agent policy.

Quota: map the routed `codex` models to Astra, Sol, and Luna, but treat Astra as a scarce Codex resource. If Codex quota is tight, keep Grok on implementation and reserve remaining Codex for Sol or a single Astra review, not an Astra coding loop.

Prompting if Astra is used: bias it to act, finish authorized work before asking, and cap extra tests. OpenAI’s own initiative/follow-through prompts exist because the default is to pause. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)

## Evidence quality

- Names, prices, limits, and intended roles: high confidence (OpenAI API, Codex, pricing pages, 2026-09-22 Sol/Luna post).
- Astra capability vs Fable: medium. AA is independent but harness-specific; OpenAI evals are vendor; CodeRabbit is a vendor with a product to sell.
- Astra as daily coder: user reports after ~3 weeks are mixed and often negative on cost/quota, not on peak intelligence. Do not route bulk coding to it from anecdotes or from SOTA claims.
- GPT-6 Sol quality: **too new to grade from users.** The cost cut and “Sol remains the coding/agent default” are first-party. Coding/taste scores above assume continuity with 5.6 Sol plus Astra’s writing-style transfer. Revisit after a week of direct use.
- Local IDs: Pi Codex catalog still 5.6 Sol/Luna/Terra + Astra; cliproxyapi already enables GPT-6 Sol/Luna. Confirm the live ID before editing the skill’s quota text.
