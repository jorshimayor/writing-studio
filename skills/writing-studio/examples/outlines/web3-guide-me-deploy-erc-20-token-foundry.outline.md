---
topic: Deploying an ERC-20 token to a testnet with Foundry and OpenZeppelin
user_need: Guide Me
domain: Web3
channel: blog
profile: jorshimayor
reader: developers who know some Solidity and want a clean, safe first deployment
level: beginner
primary_keyword: deploy erc-20 token
secondary_keywords: [Foundry, OpenZeppelin, testnet]
title: How To Deploy An ERC-20 Token With Foundry
seo_title: How to Deploy an ERC-20 Token With Foundry, Step by Step
meta_description: Deploy an ERC-20 token to a testnet with Foundry and OpenZeppelin. Set up the project, write and test the contract, deploy safely, and verify it works.
slug: deploy-erc-20-token-foundry
cta: Watch the video version of this deployment
target_length: 1,800 to 2,500 words
keyword_source: autocomplete + SERP
status: example
---

# How To Deploy An ERC-20 Token With Foundry

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | How To Deploy An ERC-20 Token With Foundry | 42 | How-to | Exact query |
| 2 | Deploy An ERC-20 Token In 15 Minutes With Foundry | 49 | Timeframe | Clear promise |
| 3 | Your First ERC-20 Token: Foundry Step-By-Step Guide | 51 | Audience | Beginner-friendly |
| 4 | ERC-20 Token Deployment With Foundry And OpenZeppelin | 53 | Keyword: tools | Tool searches |
| 5 | How To Deploy An ERC-20 Token Safely On A Testnet | 49 | Safety | Differentiates on safety |
| 6 | Foundry Tutorial: Write, Test And Deploy An ERC-20 | 50 | Process | Covers the whole loop |
| 7 | Deploy An ERC-20 Token Without Leaking Your Private Key | 55 | Mistake | Strong safety hook |
| 8 | From forge init To Deployed Token: An ERC-20 Guide | 49 | Specific | Dev-native language |

## Reader desires
- I want clear steps I can follow.
- I want answers to follow-up questions before I've asked them.
- I want to know it actually worked.

## Search intent
- Format that ranks: step-by-step tutorials with commands.
- Questions to answer: how to deploy erc20 with foundry, forge create vs forge script, how to verify a contract, how to keep keys safe.
- Gap: many tutorials paste private keys into commands. This one uses environment variables and a burner wallet.

## Intro plan
- Setup: deploying a token is the "hello world" of Web3, and it's easy to do unsafely.
- Why it matters now: Foundry has become a standard toolkit, and testnet-first habits prevent costly mistakes.
- Implied roadmap: prerequisites, project setup, contract, tests, deployment, verification.
- Transition: first, what you need installed.

## Outline
### H2: Prerequisites for Deploying an ERC-20 Token
- Purpose: everything needed before step 1.
- Key points: Foundry installed, a burner wallet with testnet ETH, an RPC URL, basic Solidity. Warn: never use a wallet holding real funds.
- Keywords: deploy erc-20 token; testnet
- Links: [the Foundry book](https://book.getfoundry.sh/)

### H2: Step 1: Set Up a Foundry Project for Your ERC-20 Token
- Purpose: project setup.
- Key points: numbered steps: forge init, install OpenZeppelin, configure remappings. Screenshot of the folder tree.
- Keywords: Foundry
- Visual: screenshot of the project structure, alt "Foundry project structure for an ERC-20 token".

### H2: Step 2: Write the Token Contract With OpenZeppelin
- Purpose: the contract.
- Key points: extend the audited ERC20 contract, set name, symbol and initial supply. Note that example code is unaudited for production use.
- Keywords: OpenZeppelin
- Links: [OpenZeppelin ERC-20 docs](https://docs.openzeppelin.com/contracts/5.x/erc20), [the ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20)

### H2: Step 3: Test the Token Locally
- Purpose: tests before deployment.
- Key points: numbered steps: write forge tests for supply and transfers, run forge test, read the output.
- Visual: screenshot of passing tests.

### H2: Step 4: Deploy the ERC-20 Token to a Testnet
- Purpose: deployment.
- Key points: load the key from an environment variable, run a forge script with broadcast, save the address. Expected output shown.
- Keywords: deploy erc-20 token; testnet
- Visual: screenshot of the deployment output.

### H2: How To Verify Your ERC-20 Token Deployment
- Purpose: confirm it worked, then next steps.
- Key points: check the contract on a block explorer, add the token to a wallet, troubleshoot common errors (insufficient funds, wrong chain ID).
- Links: [the video version](https://www.youtube.com/@jorshimayor), [my fractional NFT project](https://github.com/jorshimayor/fractionalize-nft), [more Web3 guides](https://jorshimayor.is-a.dev/work)

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| the video version | https://www.youtube.com/@jorshimayor | How To Verify |
| my fractional NFT project | https://github.com/jorshimayor/fractionalize-nft | How To Verify |
| more Web3 guides | https://jorshimayor.is-a.dev/work | How To Verify |

## Sources
- https://book.getfoundry.sh/
- https://docs.openzeppelin.com/contracts/5.x/erc20
- https://eips.ethereum.org/EIPS/eip-20

## Open questions
- Pin Foundry and OpenZeppelin versions on the day of writing, and test every command.
