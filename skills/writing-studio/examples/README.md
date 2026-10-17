# Examples

Eight complete outlines, one per reader need, two per domain. Each one passes `scripts/outline_check.py` with no warnings, so they double as test fixtures when the checker changes.

| Domain | Reader need | Outline | Title |
|---|---|---|---|
| ZK | Educate Me | [zk-educate-me-what-is-a-zero-knowledge-proof](outlines/zk-educate-me-what-is-a-zero-knowledge-proof.outline.md) | What Is A Zero-Knowledge Proof? A Developer's Guide |
| AI | Explain It | [ai-explain-it-how-does-a-context-window-work](outlines/ai-explain-it-how-does-a-context-window-work.outline.md) | How Does A Context Window Work In LLMs? |
| Web3 | Compare For Me | [web3-compare-for-me-optimistic-vs-zk-rollups](outlines/web3-compare-for-me-optimistic-vs-zk-rollups.outline.md) | Optimistic Vs ZK Rollups: Which Should You Build On? |
| Web3 | Guide Me | [web3-guide-me-deploy-erc-20-token-foundry](outlines/web3-guide-me-deploy-erc-20-token-foundry.outline.md) | How To Deploy An ERC-20 Token With Foundry |
| Web2 | Fix It | [web2-fix-it-postgresql-too-many-connections](outlines/web2-fix-it-postgresql-too-many-connections.outline.md) | PostgreSQL Too Many Connections? 5 Fixes That Work |
| AI | Give Me Perspective | [ai-give-me-perspective-140-few-shot-experiments](outlines/ai-give-me-perspective-140-few-shot-experiments.outline.md) | I Ran 140 Few-Shot Experiments: Here's What Actually Matters |
| Web2 | Update Me | [web2-update-me-nextjs-15-caching-changes](outlines/web2-update-me-nextjs-15-caching-changes.outline.md) | Next.js 15 Caching Changes: What Breaks And How To Fix It |
| ZK | Inspire Me | [zk-inspire-me-learning-zero-knowledge-proofs](outlines/zk-inspire-me-learning-zero-knowledge-proofs.outline.md) | Learning Zero-Knowledge Proofs: From Solidity To A ZK App |

Notes:
- The Inspire Me outline is a **template**: replace every `<placeholder>` with real details. Never invent a story.
- Facts in the outlines were checked against their linked sources in October 2026. Re-verify versions, dates and limits before publishing, as each outline's "Open questions" asks.

Run them all:

```bash
python3 scripts/outline_check.py examples/outlines/*.outline.md \
  --site "jorshimayor.is-a.dev, jorshimayor.hashnode.dev, jorshimayor.substack.com, youtube.com/@jorshimayor, github.com/jorshimayor" --strict
```

Fill-in templates for each channel live in [`../templates/`](../templates/): `article.md`, `substack-post.md`, `newsletter-issue.md` and `youtube-package.md`.
