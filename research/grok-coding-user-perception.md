# Grok for coding: current user perception and routing implications

**Updated 2026-08-18.** This report separates model versions and distinguishes first-party capability claims from direct, mostly anecdotal user reports. The original broad scan ran through 2026-03-13; the update below covers Grok 4.6, which materially changes the routing recommendation.

## Current recommendation: Grok 4.6

Use **Grok 4.6** as the high-volume implementation route when the plan, boundaries, and acceptance checks are explicit. Keep **Claude Opus 5** for architecture, ambiguous debugging, difficult review, and work where taste or failure cost dominates token cost. For work that is both difficult and code-heavy, use **Claude plan → Grok implementation → Claude review**.

This is a routing prior, not a claim that Grok and Claude are interchangeable:

- xAI prices Grok 4.6 at **$2/M input and $6/M output** below 200k prompt tokens, versus Anthropic's **$2/$10** for Sonnet 5 and **$5/$25** for Opus 5. Grok's output is therefore 40% cheaper than Sonnet and 76% cheaper than Opus at base API rates. Grok doubles all token rates once a prompt reaches 200k, so repository size can narrow the advantage. [xAI model page](https://docs.x.ai/developers/models/grok-4.6), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- xAI reports Grok 4.6 at **69.9% CursorBench 3.2**, **65.9% DeepSWE 1.1**, and **61.3% FrontierCode 1.1 Extended**. Those first-party results put it near frontier models but show benchmark-dependent gaps; they are useful priors, not neutral head-to-head proof. [xAI launch and evals, 2026-08-12](https://x.ai/news/grok-4-6)
- Direct user reports are positive on price/performance but mixed on parity. One daily user says it is good but still below Opus 5 and Sol 5.6 ([HN, 2026-08-18](https://news.ycombinator.com/item?id=49341812)); another switched from Opus 4.8 because Grok was “good enough” and much cheaper ([HN, 2026-08-14](https://news.ycombinator.com/item?id=49302267)); another calls it a price/output-quality game changer ([HN, 2026-08-14](https://news.ycombinator.com/item?id=49305307)).
- Taste remains the clearest reason to retain Claude. One user describes Grok as “messy” but says it finishes and now verifies visually more often ([HN, 2026-08-13](https://news.ycombinator.com/item?id=49280473)); another rates Grok's design output poorly ([HN, 2026-08-14](https://news.ycombinator.com/item?id=49295424)); a separate visual comparison says Grok has caught up substantially but Opus remains best ([HN, 2026-08-13](https://news.ycombinator.com/item?id=49289786)).

**Community-shaped routing estimate:** Grok 4.6 belongs just below Opus/Sol on judgment, with lower taste but strong completion behavior. The evidence supports routing bulk code generation to it; it does not support replacing Claude for plans, reviews, or subjective product decisions. These reports are early, anecdotal, and affected by launch promotions and harness differences.

## Earlier routing snapshot (through 2026-03-13)

- **Do not create a generic “Grok” route.** At minimum, distinguish **Grok Code Fast 1**, **Grok 4.1 Fast**, and the very new **Grok 4.20 beta/checkpoint**. Reports about one do not transfer safely to another.
- **Grok Code Fast 1:** route bounded, well-specified implementation, repetitive edits, compilation/test-fix loops, and other latency-sensitive work here when cost matters. Give it an explicit plan and objective checks. Do **not** make it the sole planner/reviewer for large cross-cutting work or an unattended long run.
- **Grok 4.1 Fast:** consider for cheap long-context repository exploration, search/research, tool-heavy triage, and plan drafts. Coding reports are mixed and generally place it below Claude on difficult implementation; require harness-specific tool tests and downstream verification.
- **Grok 4.20 (`0309`, beta):** evaluation-only for coding routing. It is current and inexpensive relative to Claude, but there is too little version-specific coding sentiment to infer reliability from older Grok models.
- **Claude Opus 4.6:** prefer for architecture, ambiguous/high-risk debugging, major refactors, difficult review, long autonomous work, and work where one-shot quality or taste matters more than token price.
- **Claude Sonnet 4.6:** prefer as the lower-cost production default for substantial implementation, frontend/UI, and agentic coding when Opus is unnecessary. Use Grok Code Fast 1 beneath it only when the task is narrow enough that retries and review will not erase the price advantage.

**Practical pattern:** Claude Opus/Sonnet plans or reviews; Grok Code Fast 1 executes small verified slices. Grok 4.1 Fast can cheaply gather context or propose alternatives, but should not silently replace Claude for complex coding.

## Model identity, official limits, and API cost

Prices are USD per million tokens and exclude tool charges. Subscription products and third-party harness multipliers differ.

| Model at cutoff | Status / intended role | Context | Input / output | Important official claim |
|---|---|---:|---:|---|
| **Grok Code Fast 1** (`grok-code-fast-1`) | Coding-specific model launched **2025-08-28** | 256k | **$0.20 / $1.50**; cached input $0.02 | xAI reported 70.8% SWE-bench Verified on its **own internal harness**, plus optimization for grep, terminal, and file editing. [xAI launch](https://x.ai/news/grok-code-fast-1), [model card](https://data.x.ai/2025-08-26-grok-code-fast-1-model-card.pdf). It remained active in Copilot Free auto-selection on **2026-03-04**. [GitHub](https://github.blog/changelog/2026-03-04-grok-code-fast-1-is-now-available-in-copilot-free-auto-model-selection/)
| **Grok 4.1 Fast** (`grok-4-1-fast-reasoning` / `-non-reasoning`) | General agent/tool model launched **2025-11-19** | 2M | **$0.20 / $0.50**; cached input $0.05; hosted tools from $5/1k successful calls | xAI calls it its best tool-calling model and reports long-horizon RL, parallel tools, search, code execution, and strong function-calling results. These are vendor claims, not coding-user consensus. [xAI](https://x.ai/news/grok-4-1-fast)
| **Grok 4.20 `0309` reasoning** | Current beta checkpoint; too new for stable sentiment | 1M | Below 200k: **$1.25 / $2.50**, cached $0.20; at/above 200k: $2.50 / $5.00, cached $0.40 | xAI documents function calling, structured output, and reasoning. [xAI model page](https://docs.x.ai/developers/models/grok-4.20-0309-reasoning) (checkpoint dated **2026-03-09**, accessed 2026-03-13)
| **Claude Opus 4.6** | Anthropic flagship launched **2026-02-05** | 1M beta | Standard: **$5 / $25**; over 200k: $10 / $37.50 | Anthropic claims improved planning, long-running agents, large-codebase work, debugging, and review, and a leading Terminal-Bench 2.0 result. [Anthropic](https://www.anthropic.com/news/claude-opus-4-6)
| **Claude Sonnet 4.6** | Lower-cost Claude default launched **2026-02-17** | 1M beta | Starts at **$3 / $15** | Anthropic reports improvements in coding, long sessions, instruction-following, agent planning, and design; its own Claude Code test preferred it to Sonnet 4.5 about 70% of the time. [Anthropic](https://www.anthropic.com/news/claude-sonnet-4-6)

Official benchmarks are useful priors, not apples-to-apples routing evidence: vendors use different harnesses, prompts, tool budgets, and sampling. In particular, xAI explicitly labels the Code Fast SWE-bench harness internal.

## What users repeatedly report

### Grok Code Fast 1: strong consensus on speed and price; disputed quality ceiling

**Recurring positive pattern.** Users repeatedly call it very fast, cheap, and useful for everyday or focused edits. Examples include “very fast and very cheap, but only moderately intelligent” (**2025-09-29**, [HN](https://news.ycombinator.com/item?id=45417253)); a Cursor user reserving Sonnet for more complex requests while using Code Fast for simple-to-semi-complex refactors (**2025-09-09**, [Reddit](https://www.reddit.com/r/cursor/comments/1nc9lre/grokcodefast1_appreciation_post/)); and a coding-agent author praising its function calling and instruction-following (**2025-10-13**, [HN](https://news.ycombinator.com/item?id=45566083)). A stronger positive outlier reports a complicated refactor, exhaustive CLI tests, and Kubernetes monorepo work being “a breeze” (**2025-11-09**, [HN](https://news.ycombinator.com/item?id=45864720)).

**Recurring negative pattern.** Other users report that quality drops as complexity rises: precise edits work, but large concurrent programs get it stuck (**2026-02-17**, [HN](https://news.ycombinator.com/item?id=47046139)); it is “amazing for quick edits” while full Grok is closer to Claude on complex issues (**2026-01-11**, [HN](https://news.ycombinator.com/item?id=46581528)); and Claude is “far better” after letting Code Fast churn on a solution (**2026-02-26**, [HN](https://news.ycombinator.com/item?id=47168277)). In one OpenRouter community thread, users variously reported rapid struggle, syntax/compile errors, loops and false completion, while others called it a strong app builder (**2025-09-07–25**, [thread and direct comments](https://www.reddit.com/r/openrouter/comments/1nb0u80/grok_code_fast_1_came_out_of_nowhere_and/)).

**Instruction and tool reliability are harness-sensitive.** One user asked it to read OpenTUI documentation and received a plan for a different Rust TUI library (**2025-11-06**, [HN](https://news.ycombinator.com/item?id=45835945)). A Cline issue reports destructive editing of a long source file, while the same reporter says the model worked nearly flawlessly in Kilo Code (**2025-10-11**, [GitHub](https://github.com/cline/cline/issues/6769)). That is evidence against treating model and harness quality as separable constants.

**Routing inference:** the defensible consensus is “fast, economical, often good enough,” not “Claude-equivalent.” Positive large-project reports exist, but disagreement is substantial. Keep tasks small, retain checkpoints, and require compile/test/lint or a stronger reviewer.

### General Grok models: useful second opinion and cheap tools, but not one coding profile

Reports about **Grok 4 / 4.1 / 4.1 Fast** are meaningfully different from Code Fast:

- Several users use regular Grok as an **architecture or review consultant**, while Claude remains the implementation workhorse: Grok 4 for architecture consulting and Claude Code for features (**2025-07-18**, [HN](https://news.ycombinator.com/item?id=44607502)); Grok 4 as a “Stack Overflow”/diff-review second opinion while Sonnet runs coding sprints for hours (**2025-08-06**, [HN](https://news.ycombinator.com/item?id=44809787)); and Grok 4 finding a subtle bug, though Claude/Gemini CLI remained the recommended starting environment (**2025-07-10**, [HN](https://news.ycombinator.com/item?id=44526991)).
- **Grok 4.1 Fast** has a credible cost/context/tool-use proposition, but coding sentiment remains mixed. One user says it “choke[s] less” than Sonnet while also declining to trust any model with non-standard architecture (**2026-02-10**, [HN](https://news.ycombinator.com/item?id=46968135)). Another says it is not as good as Claude for coding but “incredible” for research (**2026-03-06**, [HN](https://news.ycombinator.com/item?id=47270998)).
- General Grok quality has sharp disagreement: one user found Grok 4 Expert repeatedly introduced new coding errors and hallucinated while following instructions (**2025-12-22**, [HN](https://news.ycombinator.com/item?id=46360009)); another rated Grok 4 Heavy above Claude 4.5 but conceded Claude had better tooling and UX (**2025-12-22**, [HN](https://news.ycombinator.com/item?id=46359591)).
- **Grok 4.20 beta:** one early user says it has not been a top coding model and Claude remains ahead (**2026-03-10**, [HN](https://news.ycombinator.com/item?id=47323497)); another beta participant says the multi-agent build often beat Claude and GPT on coding/STEM tasks (**2026-03-13**, [HN](https://news.ycombinator.com/item?id=47369320)). Two conflicting anecdotes are not enough to set a production route.

**Routing inference:** use Grok 4.1 Fast for its documented economics, context, and tool/search specialization—not because Code Fast users liked a different model. Treat Grok 4.20 as a candidate requiring local evals.

## Task-by-task comparison

| Task | User-reported Grok picture | Routing implication versus Opus/Sonnet |
|---|---|---|
| **Large code-writing / refactors** | Code Fast has real success stories, but the more recurrent boundary is small-to-medium, explicit work; failures rise with complexity. | Sonnet default; Opus for cross-cutting/high-risk work. Use Code Fast only in tested slices.
| **Long autonomous runs** | Speed enables many actions, but looping, false completion, context drift, and harness failures appear in direct reports. Grok 4.1 Fast is officially trained for long horizons, but coding-user validation is thin. | Prefer Opus; Sonnet is the economical alternative. If using Grok, checkpoint frequently and cap retries/tool calls.
| **Architecture / planning** | Regular Grok 4 is sometimes valued as a consultant. Code Fast is weaker when asked to absorb unfamiliar docs or plan broadly. | Opus first; Sonnet for routine planning. Grok 4.1 Fast can generate a cheap second plan, not own the final decision.
| **Debugging** | Regular Grok 4 has positive subtle-bug and second-opinion anecdotes. Code Fast is useful in quick test-fix loops, but retries can erase its speed advantage. | Opus for ambiguous/root-cause debugging; Sonnet for normal bugs; Grok as a parallel hypothesis generator or bounded fixer.
| **Code review** | Best direct evidence is for regular Grok 4/Fast as a second pair of eyes, not Code Fast as final reviewer. | Opus for high-stakes review; Sonnet for scaled routine review. Grok may add an inexpensive independent pass.
| **UI / visual taste** | Version-specific evidence is sparse for Code Fast. A Grok 4 frontend report found it underwhelming and behind Claude Opus/Sonnet in a crowdsourced UI leaderboard (**2025-07-11**, [Reddit](https://www.reddit.com/r/ChatGPTCoding/comments/1lww9hw/grok_4_still_doesnt_come_close_to_claude_4_on/)). | Do not assign Grok a high-taste route from current anecdotes. Prefer Opus/Sonnet, especially Sonnet 4.6 given Anthropic’s design-focused release evidence.
| **Instruction-following** | Contradictory: agent authors praise Code Fast, while others report wrong-framework plans, shortcuts, loops, and claims of completion without changes. | Restrict Code Fast to explicit acceptance checks. Sonnet/Opus remain safer defaults for nuanced constraints.
| **Tool use** | Code Fast and 4.1 Fast were explicitly trained for tools; users confirm speed and function calling, but failures vary substantially by Cline/Kilo/Cursor/OpenCode integration. | Evaluate **model × harness**, not model alone. Claude Code’s mature harness is part of Claude’s practical advantage.
| **Cost** | Grok’s token prices and latency are the clearest advantages. Users repeatedly cite them as the reason for daily-driver use. | Route high-volume bounded work to Grok. Measure total cost including retries, review, and failed edits; use Claude when failure cost dominates token cost.

## Evidence quality and bias

- These are **anecdotes**, not controlled head-to-head experiments. They reveal recurring workflow fit and failure modes, not a numerical intelligence ranking.
- Launch-period Code Fast usage and praise are selection-biased by free placement in Cursor, Copilot, Cline, Roo Code, Kilo Code, OpenCode, and Windsurf. Reddit and HN users explicitly disputed whether OpenRouter popularity reflected quality or promotion ([Reddit, 2025-09-07](https://www.reddit.com/r/openrouter/comments/1nb0u80/grok_code_fast_1_came_out_of_nowhere_and/); [HN, 2025-09-25](https://news.ycombinator.com/item?id=45376924)). Usage share is not a quality vote.
- Communities are self-selecting: cost-sensitive hobbyists, AI-heavy developers, and users motivated by unusually good or bad runs post disproportionately.
- Model output depends heavily on repository, language, prompt, reasoning mode, provider checkpoint, and agent harness. Some “model” complaints are clearly integration incidents.
- Current-model evidence is asymmetric: Code Fast has months of reports, while Grok 4.20 had only a short beta history by the cutoff; Opus/Sonnet 4.6 were also recent. First-party release evaluations are informative but promotional.
- Therefore, update routing from repeatable local task evals and observed retry/review cost. Treat numerical routing scores as provisional shorthand, not measured community consensus.
