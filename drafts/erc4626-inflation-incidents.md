---
title: Vault Share-Price Incidents, 2023 To 2026: How Each One Was Pulled Off
slug: erc4626-inflation-incidents
companion_to: drafts/erc4626-inflation-attack-defences.md
domain: Web3
last_verified: 9 November 2026
status: draft
---

# Vault Share-Price Incidents, 2023 To 2026: How Each One Was Pulled Off

Companion case file to "ERC-4626 Inflation Attack: 3 Defences That Hold, 1 That Fails". The article explains the mechanism and the defences. This file goes incident by incident: what the attacker did, in order, with the amounts the post-mortems report; which term of the share formula moved; and which of the three defences would have stopped it.

Every entry describes the vulnerability class and the fix. None of it is a runnable exploit, and none of these contracts should be interacted with. Amounts are as reported by the sources linked under each entry; where sources disagree, both figures are given.

The formula under all six:

```text
shares = assets × totalSupply / totalAssets
```

| Incident | Date | Loss | Term moved | How | Defence that stops it |
|---|---|---|---|---|---|
| Belong Staking.sol | October 2025 | none, audit finding | totalAssets, by donation | Classic 1 wei + donation on an empty vault | Any of the three |
| Thetanuts new vault | 20 April 2026 | ~$50,000 | totalAssets, by donation | Classic first depositor attack | Any of the three |
| Yearn yUSDT | 13 April 2023 | ~$11.6M | totalAssets, by configuration | Misconfigured lender address, rebalance() wipes accounted value | Internal accounting with a minimum pool check; a seed |
| Yearn yTUSD | 16 December 2025 | ~$293,000 | totalAssets, by configuration | Same bug, different vault | Same |
| Thetanuts legacy index | 15 June 2026 | ~$105,500 net, ~$2.1M headline | totalSupply, driven to near zero | claim() empties the basket, mint() rounds requirements to 0 | Dead shares / minimum supply |
| Summer.fi Lazy Summer | 6 July 2026 | ~$6.04M | totalAssets, by donation to a sub-strategy | Stale strategy adapter still in the NAV sum | Internal accounting at the adapter level; full offboarding |

---

## 1. Belong Staking.sol, October 2025

**Status:** found in an Immunefi audit competition before launch. No funds lost.

**What the contract was.** `contracts/v2/periphery/Staking.sol`, an ERC-4626 vault for the LONG token with a minimum stake period. The deployment script minted nothing before the first user.

**How the vector was implemented, per the proof of concept in report #57401.**
1. The vault is deployed. The attacker deposits 1 wei of LONG and receives 1 sLONG share.
2. A legitimate user prepares a deposit of 10 LONG, which is 10e18 wei.
3. The attacker front-runs it by transferring 10e18 LONG straight to the vault. Supply is still 1 share; `totalAssets()` is now 10e18 + 1.
4. The user's deposit mints 10e18 × 1 / (10e18 + 1), which rounds to 0 shares.
5. After the minimum stake period, the attacker redeems the single share for 20e18 + 1 LONG.

**Which term moved.** `totalAssets()`, by donation, on a vault with supply 1.

**Why the defences would have worked.** Any of the three. A seed deposit with burned shares, a non-zero `_decimalsOffset()`, or a tracked `totalAssets()` each break step 4. The report notes the attack needs no other staker to act between steps 1 and 5, which is why it is a front-running attack in practice.

**Notes for the article.** The report header says Critical and the body says Medium; the competition logged several near-duplicate reports (#57716, #57924, #56896). The library the vault inherited from is not named in the report. The claim in some write-ups that it was Solady's ERC-4626 with a +1 virtual offset is unverified; check the audit-comp repository before repeating it.

**Sources.** [Immunefi report #57401](https://reports.immunefi.com/belong/57401-sc-critical-erc4626-inflation-attack-vulnerability), [#57716](https://reports.immunefi.com/belong/57716-sc-critical-erc4626-inflation-bug-in-staking-contract).

---

## 2. Thetanuts Finance New Vault, 20 April 2026

**Status:** exploited. About $50,000 lost.

**What the contract was.** A newly deployed Thetanuts vault on Ethereum. Thetanuts is an on-chain options protocol; the vault was a new deployment, not the deprecated index token hit two months later.

**How the vector was implemented.** SlowMist's incident entry and DefiLlama's hacks list classify it as a first depositor attack on a vault that started with zero assets and zero shares. Public detail stops there: no post-mortem from the team, no reconstructed trace. The vector is the one in entry 1, with real funds on the other side.

**Which term moved.** `totalAssets()`, by donation, on an empty vault.

**Why the defences would have worked.** Any of the three, for the same reason as Belong.

**Notes for the article.** This is the one live ERC-4626 inflation attack of 2026 that matches the textbook. Keep it to a sentence or two in the article until a technical write-up appears. If you quote the "1000 ETH donation" figure that appears in one aggregator, mark it unverified; it does not appear in SlowMist's or DefiLlama's entries.

**Sources.** [SlowMist hacked archive](https://hacked.slowmist.io/), [DefiLlama Thetanuts hacks](https://defillama.com/protocol/thetanuts-finance).

---

## 3. Yearn yUSDT, 13 April 2023

**Status:** exploited. About $11.6 million (PeckShield); CertiK and Halborn round to $10 million.

**What the contract was.** The legacy iearn yUSDT contract, which predates Yearn's v1 and v2 vaults. It held USDT across several lenders (Aave, Compound, dYdX, Fulcrum) and priced its shares from the sum of those positions. The Fulcrum slot was hardcoded to bZx iUSDC, a USDC lending token, instead of iUSDT. The error had been live since deployment, about three years.

**How the vector was implemented.**
1. The attacker took flash loans and arranged positions so that the yUSDT contract's balances at Aave, Compound and dYdX could be unwound. SlowMist's analysis describes repaying others' debt on Aave to push the rate down and force the vault's strategy to move.
2. They minted iUSDC and transferred it directly to yUSDT, raising the reserve the misconfigured Fulcrum slot reports.
3. With the other reserves emptied, only the iUSDC position remained. They called `rebalance()`, which runs `_withdrawAll()` and redeems the Fulcrum position. Because the slot pointed at iUSDC, the redemption returned USDC, which yUSDT does not count. The accounted pool value dropped to near zero while the yUSDT supply stayed large.
4. They deposited 10,000 USDT and minted 1,252,660,242,212,927 yUSDT, the share formula dividing by an almost-empty pool.
5. They swapped the inflated yUSDT through Curve's yPool and other venues into stablecoins and repaid the flash loans.

**Which term moved.** `totalAssets()`, by configuration. A plain donation is not required when the contract itself can be made to throw its own assets out of the accounting.

**Why the defences would or would not have worked.** Virtual shares would have slowed the final mint but the contract predates them. Dead shares would not have mattered; supply was large throughout. The fix is accounting: a `totalAssets()` that cannot fall to dust while supply is large, a minimum pool-value check on deposit, and a deployment check that every lender address holds the vault's own asset.

**Notes for the article.** The number people remember is "1.2 quadrillion yUSDT from $10,000". The lesson that matters is that the attack path ran through a config value, not a code bug, and the immutable contract could not be patched once researchers noticed.

**Sources.** [CertiK analysis](https://www.certik.com/resources/blog/earnings-misconfigured-yearn-finance-exploit-explained), [SlowMist analysis](https://slowmist.medium.com/an-analysis-of-the-attack-on-yearn-finance-bd17f55460ea), [Halborn explainer](https://halborn.com/blog/post/explained-the-yearn-finance-hack-april-2023), [The Block on yUSDT](https://www.theblock.co/post/226134).

---

## 4. Yearn yTUSD, 16 December 2025

**Status:** exploited. About $293,000 profit to the attacker (rekt.news); PeckShield rounds to $300,000. Swapped to 103 ETH.

**What the contract was.** The legacy iearn TUSD vault at `0x73a052500105205d34daf004eab301916da8190f` (verify on a block explorer before publishing). Underlying asset TUSD. Its Fulcrum slot was hardcoded to bZx iSUSD, whose underlying is sUSD, and its Compound slot to cUSDC rather than cTUSD. Deployed over 2,100 days before the incident.

**How the vector was implemented (banteg's trace).**
1. Flash loan of 30,000,000 USDC from Morpho.
2. Built collateral: added 9,619,877.89 yDAI and 7,763,100.31 yUSDC to Curve's yPool for 631,198,494.03 yCRV, deposited that into the Yearn yCRV vault, and used the shares as collateral to mint 3,900,000 STABLEx.
3. Deposited 1,169,030.28 TUSD into yTUSD for 732,294.52 yTUSD.
4. Minted 213,848.03 iSUSD and transferred it straight to the yTUSD contract. The misconfigured Fulcrum slot counted it, inflating the pool value.
5. Burned 769,318.06 yTUSD and received 1,414,919.51 TUSD against the inflated value.
6. Called `rebalance()`. `_withdrawAll()` redeemed the donated iSUSD into 215,192.93 sUSD, which yTUSD does not price. The accounted pool collapsed.
7. Sent 0.000000001 TUSD to the contract, leaving a dust pool against a large supply.
8. Deposited 1,000 TUSD and minted about 1.17 × 10^35 yTUSD. Price per share fell from about 1.596 × 10^18 to 8,546 wei.
9. Swapped 9,000,000 yTUSD for 7,812,398.14 yUSDC and about 1.17 × 10^35 yTUSD for 9,623,355.34 yDAI through the yPool.
10. Unwound and repaid the flash loan. The EOA kept about 245,643.07 TUSD and 6,845.15 USDC.

**Which term moved.** `totalAssets()`, twice: up by donation (step 4) and down by configuration (step 6). The final mint is the inflation step.

**Collateral damage.** About 3.9 million STABLEx left undercollateralised. Curve yPool's virtual price fell about 480×, from 1.262 × 10^16 to 2.629 × 10^13. 215,192.93 sUSD remains inside yTUSD with no code path to withdraw it.

**Why the defences would or would not have worked.** Same as yUSDT. Internal accounting that only counts the vault's own asset and its correctly configured lenders breaks steps 4 and 6. A minimum pool-value check breaks step 8. The deployment-time check that every lender's underlying equals the vault's asset would have caught both Yearn bugs before they went live.

**Notes for the article.** This is the strongest evidence for "audit the config as hard as the code": the same class of error, in a sibling contract, 32 months after the first one made headlines.

**Sources.** [banteg's technical write-up](https://github.com/banteg/iearn-2025-12-investigation/blob/master/technical-writeup.md), [rekt.news](https://rekt.news/yearn-rekt4), [William Li's thread](https://x.com/hklst4r/status/2001072409684685003), [OpenZeppelin's 2025 rewind](https://www.openzeppelin.com/news/web3-security-auditors-2025-rewind).

---

## 5. Thetanuts Legacy Index Token, 15 June 2026

**Status:** exploited. Headline $2.1 million; about $105,471 USDC realised plus three residual option-vault tokens after whitehats recovered roughly $2 million in option tokens.

**What the contract was.** A deprecated index token, TN-IDX-USDC-PUT at `0xC2C3AE0a7b405058558C9b4a63b373486CB86Ac7` (verify before publishing), redeemable for a basket of five Thetanuts option-vault tokens (BTC, ETH, AVAX, BNB and MATIC puts against USDC). Not ERC-4626, but the same proportional share maths.

**How the vector was implemented (DarkNavy's reconstruction, medium confidence on the exact Solidity).**
1. The attacker deployed a runner contract and flash-loaned 153,054.60 TN-IDX-USDC-PUT from a lending pool.
2. Called `claim(153,054.600569)` once. `claim` pays each basket component pro rata (`basketBalance[i] × amount / supplyBefore`), so the index token paid out all five positions: 49,716.43 BTC-put tokens, 23,955.28 ETH-put, 6,378.69 AVAX-put, 17,186.38 BNB-put and 10,028.70 MATIC-put. The basket was empty and supply was near zero.
3. Called `mint(uint256)` 37 times, doubling from 0.000002 up to 68,719.48, then a final 15,753.40. `mint` computes `required[i] = basketBalance[i] × amount / supply`; with the basket empty every `required[i]` rounded to zero, so every `transferFrom` pulled nothing and the shares were minted anyway. Total: 153,192.35 unbacked index tokens.
4. Repaid the flash loan plus a 137.75 token premium with the freshly minted tokens.
5. Redeemed the BTC and ETH option tokens for 70,315.56 and 35,155.94 USDC. Swept the AVAX, BNB and MATIC tokens to the same wallet.

**Which term moved.** `totalSupply`, driven to near zero by `claim`, so that the inverse of the share formula rounded to nothing.

**Why the defences would or would not have worked.** This is the rounding half of the ERC-4626 story without the donation half. Dead shares or a minimum-supply floor make step 2 impossible to complete, because supply cannot reach the range where `required[i]` rounds to zero. Virtual shares in the mint path would have had the same effect. Internal accounting alone would not have helped; the backing really was gone. Rejecting any mint where a non-zero share amount requires zero backing is the one-line fix.

**Notes for the article.** Useful as the counterexample that shows the weapon is rounding, not donation. Also the second deprecated-contract loss in this list.

**Sources.** [DarkNavy analysis](https://www.darknavy.org/web3/exploits/thetanuts-legacy-index-vault-zero-cost-remint/), [BeInCrypto report](https://beincrypto.com/thetanuts-deprecated-vault-exploit-defi/), [Softstack June recap](https://softstack.io/blog/june-2026-protocol-engineering-recap).

---

## 6. Summer.fi Lazy Summer Protocol, 6 July 2026

**Status:** exploited. About $6.04 million across two USDC vaults: roughly $5.64 million from LazyVault_LowerRisk_USDC and $0.40 million from the Higher Risk vault. Summer.fi Labs announced its wind-down on 15 July 2026; the protocol passed to the Lazy Summer DAO.

**What the contract was.** Lazy Summer vaults are ERC-4626 `FleetCommander` contracts that allocate deposits across strategy adapters called Arks. `totalAssets()` is the sum of every active Ark's reported value. One Ark held Silo "Varlamore USDC Growth" tokens that had been impaired since the Stream Finance collapse in November 2025. It had been capped (`depositCap` set to zero) but not removed from the active set, so its stale valuation still fed the share price.

**How the vector was implemented (Verichains and the Summer.fi post-mortem).**
1. Flash loans of 65,419,171.88 USDC and 1,000,000 USDT from Morpho Blue, repaid in the same transaction.
2. Pre-staged the Higher Risk vault by depositing about 398,172 USDC and withdrawing almost all of it, which left the deposit in the buffer and raised the vault's immediately available liquidity from about 1,000 to about 399,172 USDC.
3. Deposited about 490,637 USDC into a Term "Summer USDC" Yearn v3 strategy for about 439,778 Term shares, to be used as the donation in step 5.
4. Lower Risk vault: deposited 64.83 million USDC at about 1.0665 per share for 60.79 million shares. Donated the impaired Silo Varlamore tokens, accumulated over the previous three months, directly to the capped Silo Ark. The Ark's reported value rose, `totalAssets()` rose with it, and the share price moved about 9.5% to 1.1677. Redeemed 60.77 million shares for 70.96 million USDC, paid out of the buffer and the liquid Arks.
5. Higher Risk vault: deposited about 29.52 million USDC at about 1.0583 per share. Donated the 439,778 Term shares to the Term Ark, which credited them at about 490,637 USDC and moved the price to 1.0756. Redeemed about 27.81 million shares for 29.92 million USDC.
6. Repaid the flash loans and sent about 6.017 million DAI plus leftover shares to the beneficiary address.

**Which term moved.** `totalAssets()`, by donation, one level down: the donation went to a sub-strategy whose balance the vault sums, not to the vault itself. The impaired tokens were valued above what they could be sold for, so the vault paid real USDC for stale value.

**Why the defences would or would not have worked.** This is the case the article's third defence is for, applied at the adapter level: an Ark's contribution to `totalAssets()` should be what the vault put there plus recognised yield, not whatever is sitting at its address. Dead shares and a decimals offset would not have mattered; supply was in the tens of millions. Fully removing an offboarded Ark from `getActiveArks()`, rather than capping it, closes the path that was actually used.

**Notes for the article.** Summer.fi's post-mortem is explicit that the contracts behaved as written and the failure was operational: capping a strategy is not removing it. The attacker funded wallets from early April 2026 and built the stale-token position over about three months.

**Sources.** [Verichains analysis](https://blog.verichains.io/p/lazy-summer-hack-analysis-stale-asset), [Summer.fi post-mortem via AMBCrypto](https://ambcrypto.com/summer-fi-reveals-months-long-preparation-behind-6m-defi-exploit/), [CoinDesk](https://www.coindesk.com/web3/2026/07/06/defi-protocol-summer-fi-halts-lazy-summer-vaults-after-usd6-million-exploit), [The Block on Summer.fi](https://www.theblock.co/post/407198/summer-finance-exploited). The primary post-mortem lives on blog.summer.fi (8 July 2026); link it directly once the URL is confirmed.

---

## What the Six Have in Common

- Five of six moved `totalAssets()`: two by plain donation (Belong, Thetanuts April), one by donation to a sub-strategy (Summer.fi), two by configuration that let the contract throw its own assets out of the accounting (both Yearn cases). One moved `totalSupply` (Thetanuts June).
- Flash loans appeared in four of six, always as the amplifier, never as the vulnerability.
- Three of six were deprecated or legacy contracts that still held value (yUSDT, yTUSD, Thetanuts June). Two were brand new (Belong, Thetanuts April).
- The two most expensive incidents (yUSDT, Summer.fi) were configuration and operations failures in contracts that behaved exactly as written.

## Verify Before Publishing

- Contract addresses for yTUSD and the Thetanuts index token on a block explorer.
- The Summer.fi primary post-mortem URL on blog.summer.fi.
- Whether a technical write-up of the Thetanuts April 2026 vault has appeared.
- Which library Belong's Staking.sol inherited (audit-comp repo).
