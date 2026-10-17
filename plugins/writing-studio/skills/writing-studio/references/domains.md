# Domain Guide: Web3, AI, ZK and Web2

How to research, word and fact-check pieces in the four domains this skill is tuned for. Read the section for your topic's domain in Step 2 (research) and Step 5 (draft). Many pieces sit across two domains (for example zkML, onchain AI agents, or a Web2 backend for a dApp). Apply both sections.

## Contents

- [Quick map](#quick-map)
- [Web3](#web3)
- [AI](#ai)
- [Zero knowledge (ZK)](#zero-knowledge-zk)
- [Web2](#web2)
- [Cross-domain topics](#cross-domain-topics)

## Quick map

| | Web3 | AI | ZK | Web2 |
|---|---|---|---|---|
| Typical reader | Solidity or Rust devs, node operators, curious Web2 devs | Developers moving into AI engineering | Web3 devs and cryptography-curious engineers | Full-stack and backend developers |
| Common reader needs | Guide Me, Compare For Me, Fix It, Update Me | Explain It, Give Me Perspective, Guide Me | Educate Me, Explain It, Compare For Me | Fix It, Guide Me, Update Me |
| Primary sources | EIPs, client and protocol docs, audited contract libraries | Papers (arXiv), model and API docs, eval results you ran | Papers, proving system and DSL docs, audits | Official docs, RFCs, release notes, MDN |
| Fastest-moving facts | Upgrade names and dates, gas costs, L2 stats | Model names, context sizes, prices, benchmarks | Prover performance, tooling versions | Framework defaults between major versions |
| Biggest risk | Security mistakes and financial-advice tone | Overclaiming capability, stale model facts | Wrong security assumptions | Version-specific advice without a version |

---

## Web3

**Readers** range from Web2 developers writing their first smart contract to validator operators. State the chain, network (mainnet or testnet) and tooling versions in every technical piece.

**Primary sources to cite**
- Ethereum Improvement Proposals: [eips.ethereum.org](https://eips.ethereum.org/) (e.g. [EIP-20](https://eips.ethereum.org/EIPS/eip-20) for tokens, [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844) for blob-carrying transactions, [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) for account abstraction).
- [ethereum.org developer docs](https://ethereum.org/en/developers/docs/), including [optimistic rollups](https://ethereum.org/en/developers/docs/scaling/optimistic-rollups/) and [ZK rollups](https://ethereum.org/en/developers/docs/scaling/zk-rollups/).
- Tooling docs: [Foundry](https://book.getfoundry.sh/), [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/5.x/erc20), [Solana docs](https://solana.com/docs).
- L2 data and risk: [L2BEAT](https://l2beat.com/).
- Security: [Consensys smart contract best practices](https://consensys.github.io/smart-contract-best-practices/), [SWC registry](https://swcregistry.io/), published audit reports.

**Where readers ask questions** (for keyword and heading ideas): [Ethereum Stack Exchange](https://ethereum.stackexchange.com/), [ethresear.ch](https://ethresear.ch/), [Ethereum Magicians](https://ethereum-magicians.org/), [r/ethdev](https://www.reddit.com/r/ethdev/), project Discords and GitHub issues.

**Terminology conventions** (pick one form and keep it; the checker flags mixed forms):
- "Web3" (capital W), "smart contract" (lowercase), "Ethereum", "Solana", "Layer 2 (L2)", "rollup".
- "onchain" / "offchain" or "on-chain" / "off-chain": choose one per piece.
- Standards as written by their authors: ERC-20, ERC-721, EIP-4844, ERC-4337.
- "dApp", "DeFi", "NFT" expanded on first use: "non-fungible token (NFT)".
- Gas and fees: write units ("gwei"), and give gas figures with the date and network.

**Accuracy and safety rules**
- **No financial advice.** Never tell readers to buy, sell or hold tokens, and never predict prices. Explain mechanisms instead.
- **Security first in code.** Example contracts use audited libraries (e.g. OpenZeppelin), get deployed to a testnet first, and carry a short note that example code is unaudited and not for production funds.
- **Never paste private keys or seed phrases** in examples, even fake-looking ones. Use environment variables and a burner wallet.
- **Date anything that changes:** upgrade names, gas costs, TVL, validator requirements. Link the live source (e.g. L2BEAT) rather than freezing numbers that go stale.
- Hacks and exploits: describe the vulnerability class and the fix, and link the post-mortem. Don't publish a step-by-step reproduction against live contracts.

**Example topics by need**

| Need | Example |
|---|---|
| Educate Me | What Is Account Abstraction (ERC-4337)? |
| Explain It | How Do Blobs (EIP-4844) Lower Rollup Fees? |
| Compare For Me | Optimistic Rollups Vs ZK Rollups: Which Should You Build On? |
| Guide Me | How To Deploy An ERC-20 Token With Foundry |
| Fix It | Transaction Stuck Pending? 5 Fixes For Ethereum Nonce Errors |
| Give Me Perspective | What I Learned Running A Solana Validator For 30 Days |
| Update Me | What The Latest Ethereum Upgrade Changes For Smart Contract Developers |
| Inspire Me | How A Reentrancy Bug Taught Me To Write Safer Solidity |

---

## AI

**Readers** are mostly developers with programming experience but little ML background. Explain model concepts in terms of what the developer controls: prompts, context, tools, parameters and evals.

**Primary sources to cite**
- Papers on [arXiv](https://arxiv.org/) (e.g. [Attention Is All You Need](https://arxiv.org/abs/1706.03762), [Lost in the Middle](https://arxiv.org/abs/2307.03172), [Rethinking the Role of Demonstrations](https://arxiv.org/abs/2202.12837)).
- Model and API documentation from the provider (e.g. [Anthropic context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows), [Hugging Face docs](https://huggingface.co/docs)), and the [Model Context Protocol](https://modelcontextprotocol.io/) spec for tool integrations.
- **Your own experiments**: notebooks, eval results and code. These are the strongest evidence and the hardest to copy.

**Where readers ask questions:** [Hugging Face forums](https://discuss.huggingface.co/), [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/), [Hacker News](https://news.ycombinator.com/), GitHub issues of popular frameworks, and YouTube comments on tutorials.

**Terminology conventions**
- "large language model (LLM)", "retrieval-augmented generation (RAG)", "Model Context Protocol (MCP)" expanded on first use.
- "fine-tuning" (hyphenated), "in-context learning", "chain-of-thought", "context window", "token".
- Model names exactly as the provider writes them, with the version.
- Parameter counts as "0.5B", "7B". Context lengths in tokens ("8,192 tokens").

**Accuracy rules**
- **Date and version every model fact.** Context sizes, prices, rankings and benchmark scores change monthly. Write "as of <month year>" and link the source.
- **Report your setup** for any result: model, size, hardware, prompt format, dataset and sample size. Say when a result is from a small model and may not generalise.
- **No capability hype.** Avoid "understands", "thinks" or "knows" as literal claims. Describe behaviour you measured.
- Separate what you measured from what you believe (Give Me Perspective).
- Code examples pin library versions and never hard-code API keys.

**Example topics by need**

| Need | Example |
|---|---|
| Educate Me | What Is Retrieval-Augmented Generation (RAG)? |
| Explain It | How Does A Context Window Work In LLMs? |
| Compare For Me | Fine-Tuning Vs RAG: Which Should You Use For Your App? |
| Guide Me | How To Build A ReAct Agent In 100 Lines Of Python |
| Fix It | LLM Ignoring Your Instructions? 6 Prompt Fixes That Work |
| Give Me Perspective | I Ran 140 Few-Shot Experiments: Here's What Actually Matters |
| Update Me | What The Model Context Protocol Means For Agent Builders |
| Inspire Me | From Solidity To AI Engineering: My First Three Weeks |

---

## Zero knowledge (ZK)

**Readers** are usually Web3 developers or engineers curious about cryptography. Most know what a hash is and few know elliptic curves. Build intuition first, then the mechanism, then the code.

**Primary sources to cite**
- [ethereum.org on zero-knowledge proofs](https://ethereum.org/en/zero-knowledge-proofs/) for accessible background.
- Proving system papers (Groth16, PLONK, STARK) and the [ZKProof community standards](https://zkproof.org/).
- Tooling docs: [Circom](https://docs.circom.io/), [Noir](https://noir-lang.org/docs), zkVMs such as [RISC Zero](https://github.com/risc0/risc0) and [SP1](https://github.com/succinctlabs/sp1), and ZK rollup docs ([Starknet](https://docs.starknet.io/), [ZKsync](https://docs.zksync.io/)).
- Audit reports for any circuit or library you recommend.

**Where readers ask questions:** [zkresear.ch](https://zkresear.ch/), [ethresear.ch](https://ethresear.ch/), project Discords and Telegram groups, GitHub issues of Circom, Noir and zkVM repos.

**Terminology conventions**
- "zero-knowledge proof (ZKP)" on first use, then "ZK proof" or "ZKP" consistently.
- "zk-SNARK", "zk-STARK" (lowercase zk, hyphenated, as most of the literature writes them).
- "prover", "verifier", "witness", "circuit", "constraint", "trusted setup", "proving key", "verification key".
- "zkVM", "zkEVM", "ZK rollup": keep one capitalization scheme per piece.

**Accuracy rules**
- **State the security assumptions** of each proof system (for example, whether it needs a trusted setup and what it's secure against). These are the details readers most often get wrong.
- **Proof sizes and proving times** depend on the circuit and hardware. Give the setup and date, and link the benchmark. Don't quote a single "speed" for a proof system.
- Circuit code: warn that under-constrained circuits are a common critical bug class, and that example circuits are unaudited.
- Explain with a concrete analogy first, then correct the analogy's limits. Never leave the reader with an analogy that implies a wrong security property.

**Example topics by need**

| Need | Example |
|---|---|
| Educate Me | What Is A Zero-Knowledge Proof? A Developer's Guide |
| Explain It | How Does A zk-SNARK Prove Something Without Revealing It? |
| Compare For Me | zk-SNARK Vs zk-STARK: Trade-Offs For Developers |
| Guide Me | How To Write Your First Noir Circuit |
| Fix It | Circom Constraint Errors Explained: 5 Common Causes And Fixes |
| Give Me Perspective | I Benchmarked 3 zkVMs On The Same Program: The Results |
| Update Me | What The New zkVM Releases Mean For Rollup Builders |
| Inspire Me | How I Went From Zero Cryptography To Shipping A ZK App |

---

## Web2

**Readers** are full-stack and backend developers. They want the fix or the pattern quickly, with the version it applies to.

**Primary sources to cite**
- Official docs and release notes (e.g. [PostgreSQL docs](https://www.postgresql.org/docs/current/runtime-config-connection.html), [Next.js 15 release notes](https://nextjs.org/blog/next-15), [Next.js caching docs](https://nextjs.org/docs/app/building-your-application/caching), [PgBouncer](https://www.pgbouncer.org/)).
- Standards: [MDN](https://developer.mozilla.org/) for the web platform, [RFCs](https://www.rfc-editor.org/) for protocols.
- Performance and security references: [Core Web Vitals](https://web.dev/articles/vitals), [OWASP Top 10](https://owasp.org/www-project-top-ten/).

**Where readers ask questions:** [Stack Overflow](https://stackoverflow.com/), GitHub issues and discussions, [Hacker News](https://news.ycombinator.com/), framework Discords and subreddits.

**Terminology conventions**
- Product and project names exactly as styled: PostgreSQL, Next.js, Node.js, GitHub, Kubernetes.
- "API", "REST", "GraphQL", "CDN", "ORM" expanded on first use where the audience includes beginners.
- Versions in full: "Next.js 15", "PostgreSQL 17", "Node.js 22".

**Accuracy rules**
- **Every fix names the version** it applies to, and notes when defaults changed between versions.
- Commands are copy-paste safe: no destructive commands without a warning and a backup step.
- Security advice follows current OWASP guidance. Never suggest disabling a security control as a "fix" without explaining the risk.
- Benchmarks state hardware, data size and configuration.

**Example topics by need**

| Need | Example |
|---|---|
| Educate Me | What Is Connection Pooling? |
| Explain It | How Does Next.js Caching Actually Work? |
| Compare For Me | REST Vs GraphQL: Which Fits Your API? |
| Guide Me | How To Add Rate Limiting To A Node.js API |
| Fix It | PostgreSQL "Too Many Connections"? 5 Fixes That Work |
| Give Me Perspective | I Moved A Side Project From Serverless To A VPS: The Numbers |
| Update Me | Next.js 15 Caching Changes: What Breaks And How To Fix It |
| Inspire Me | How A Weekend Script Became My Most-Used Tool |

---

## Cross-domain topics

Pieces that bridge domains often find gaps that single-domain writers miss. Name both audiences in the intro and explain each side's terms for the other.

| Bridge | Example | Watch for |
|---|---|---|
| AI + Web3 | Building An AI Agent That Reads Onchain Data | Agents must never hold keys with real funds. Simulate transactions before sending |
| AI + ZK | What Is zkML? Proving A Model Ran Without Revealing It | State what is proven (inference, not training) and the current performance limits |
| ZK + Web3 | How ZK Rollups Use Validity Proofs To Scale Ethereum | Separate the rollup's proof system from its data availability |
| Web2 + Web3 | Adding Wallet Login To A Next.js App | Session handling and signature replay protection |
| Web2 + AI | Caching LLM Responses In A Web App | Privacy of cached prompts, invalidation when the model or prompt changes |
