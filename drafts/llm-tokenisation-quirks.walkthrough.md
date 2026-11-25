# Test Everything In The Tokenisation Article Yourself

A step-by-step companion to "Why One Trailing Space Breaks Your Prompt: LLM Tokenisation Explained". Each step gives you the code, the output you should see, the chart to make from it, and the paper that explains why. Run it top to bottom in about 15 minutes on a laptop CPU. No GPU, no API key.

## 0. Set Up

Pin the versions the article used, so your numbers match.

```bash
mkdir tokenisation-probes && cd tokenisation-probes
uv init --python 3.11
uv add "torch==2.2.2" "transformers==4.49.0" "numpy<2" "matplotlib>=3.8" "tiktoken==0.8.0"
uv run python -c "import transformers, torch; print(transformers.__version__, torch.__version__)"
```

Expected: `4.49.0 2.2.2`.

Every snippet below assumes this header has run once:

```python
import math, torch
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
print(model.config.vocab_size, model.config.n_embd)   # 50257 768
```

The first run downloads about 550 MB of GPT-2 weights.

## 1. See The Splits (Quirks 1 To 5)

What you're testing: the model receives integer IDs, and the split points follow frequency in web text, not word boundaries.

```python
def show(text, ids=False):
    toks = tok.encode(text)
    pieces = [repr(tok.decode([t])) + (f":{t}" if ids else "") for t in toks]
    print(f"{text!r:28} {len(toks):>2} tok | " + " ".join(pieces))

for t in ["hello", " hello", "Hello", "HELLO", " HELLO",
          "2026", "1234567", "3.14159",
          "    return x", "        return x",
          "tokenization", "ChatGPT", "🙂", "👨‍👩‍👧", "你好"]:
    show(t)
```

What to look for:
- `hello` and ` hello` are both one token, with different IDs. Rerun with `ids=True` to see them.
- `HELLO` is three tokens, ` HELLO` is two. Same word, different split, because the leading space changes which merges apply.
- `2026` is `20` `26`. `1234567` is `123` `45` `67`. Nothing lines up with place value.
- The eight-space indent is eight tokens, so `        return x` is nine.
- 🙂 is two tokens that each decode to �. 你好 is four. The family emoji is ten.

Round-trip check, which proves byte-level BPE never loses information even when individual tokens are garbage:

```python
weird = ["  leading", "trailing  ", "\t\n\r", "🙂🙃🙂", "混合 mixed текст", "<|endoftext|>"]
print(all(tok.decode(tok.encode(s), clean_up_tokenization_spaces=False) == s for s in weird))  # True
```

Chart: a token-split card is clearer as a table than a plot, so skip the chart here. If you want one, plot `len(tok.encode(" " * n))` for n from 1 to 40 against n. Where the line bends is where GPT-2 has a merge for a run of spaces.

Paper: Sennrich, Haddow, and Birch, "Neural Machine Translation of Rare Words with Subword Units" (2016), https://arxiv.org/abs/1508.07909. Read section 3.2 for the merge algorithm; it's half a page. Then the GPT-2 report, Radford et al. (2019), section 2.2, for why they went to bytes: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf.

## 2. The Trailing Space (Quirk 1, The Proof)

What you're testing: a trailing space is its own token, so the model must predict a word with no leading space, which it rarely saw.

```python
@torch.no_grad()
def next_probs(prompt):
    ids = tok(prompt, return_tensors="pt").input_ids
    return torch.softmax(model(ids).logits[0, -1], dim=-1)

def entropy_bits(p):
    return -(p * torch.log2(p.clamp_min(1e-12))).sum().item()

def report(prompt, answer):
    p = next_probs(prompt)
    a = tok.encode(answer)[0]
    rank = int((p > p[a]).sum()) + 1
    print(f"{prompt!r:30} P({answer!r})={p[a]:.2%}  rank {rank:>4}  H={entropy_bits(p):.2f} bits")
    print("   tokens:", [tok.decode([t]) for t in tok.encode(prompt)])

report("The capital of France is", " Paris")
report("The capital of France is ", "Paris")
```

Expected:

```text
'The capital of France is'     P(' Paris')=3.22%  rank    5  H=8.65 bits
   tokens: ['The', ' capital', ' of', ' France', ' is']
'The capital of France is '    P('Paris')=0.00%  rank 1472  H=2.55 bits
   tokens: ['The', ' capital', ' of', ' France', ' is', ' ']
```

The second token list ends with `' '`. That lone space token is the whole story.

Chart: two panels, top six tokens each, same x axis.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 3), sharex=True)
for ax, prompt in zip(axes, ["The capital of France is", "The capital of France is "]):
    p = next_probs(prompt); v, i = p.topk(6)
    ax.barh([repr(tok.decode([ix])) for ix in i][::-1], (v * 100)[::-1], color="#2a78d6")
    ax.set_title(repr(prompt), fontsize=10); ax.set_xlabel("probability (%)")
plt.tight_layout(); plt.savefig("next-token-after-space.png", dpi=150)
```

What to look for: the right panel is dominated by `'\xa0'` (a non-breaking space) and `'ét'`. Lower entropy on the right means the model is more confident, and confidently wrong.

Extra probes worth one minute each:

```python
report("the capital of france is", " Paris")        # lowercase prompt still finds Paris
report("THE CAPITAL OF FRANCE IS", " PARIS")        # all caps: rank drops to the hundreds
report("Q: What is the capital of France?\nA:", " Paris")
```

Paper: none needed. This is the mechanism from step 1 showing up in the output distribution. If you want the background on reading next-token distributions as the model's whole interface, Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020), https://arxiv.org/abs/1904.09751, is the standard reference on what those distributions look like.

## 3. The Token Tax (Quirk 6)

What you're testing: the same sentence costs a different number of tokens per language, because the merges were learned mostly from English.

```python
same_sentence = {
    "English": "The weather is beautiful today and I want to go for a walk in the park.",
    "French":  "Il fait très beau aujourd'hui et je veux aller me promener dans le parc.",
    "German":  "Das Wetter ist heute wunderschön und ich möchte im Park spazieren gehen.",
    "Russian": "Сегодня прекрасная погода, и я хочу погулять в парке.",
    "Chinese": "今天天气很好，我想去公园散步。",
    "Arabic":  "الطقس جميل اليوم وأريد أن أذهب للتنزه في الحديقة.",
    "Hindi":   "आज मौसम बहुत सुंदर है और मैं पार्क में टहलने जाना चाहता हूँ।",
}
base = len(tok.encode(same_sentence["English"]))
counts = {}
print(f"{'lang':8} {'chars':>5} {'bytes':>5} {'tokens':>6} {'vs EN':>6}")
for lang, s in same_sentence.items():
    n = len(tok.encode(s)); counts[lang] = n
    print(f"{lang:8} {len(s):5} {len(s.encode()):5} {n:6} {n/base:5.1f}x")
```

Expected: English 17, French 30, German 28, Russian 57, Chinese 28, Arabic 50, Hindi 91. Hindi is 5.4× English.

Chart:

```python
order = sorted(counts, key=counts.get)
plt.figure(figsize=(7, 3))
plt.barh(order, [counts[l] for l in order], color="#2a78d6")
plt.xlabel("GPT-2 tokens for the same sentence"); plt.tight_layout(); plt.savefig("token-tax.png", dpi=150)
```

What to look for: compare the `bytes` column to `tokens`. Hindi is 156 bytes and 91 tokens, so GPT-2 manages fewer than two bytes per token on Devanagari. English gets about four characters per token.

Stretch (the table still marked "to run" in the article):

```python
import tiktoken
encs = {n: tiktoken.get_encoding(n) for n in ["gpt2", "cl100k_base", "o200k_base"]}
print(f"{'lang':8}" + "".join(f"{n:>14}" for n in encs))
for lang, s in same_sentence.items():
    print(f"{lang:8}" + "".join(f"{len(e.encode(s)):>14}" for e in encs.values()))
```

Divide each column by its English row to get the multipliers, then paste them into the article's table. The first `tiktoken` call downloads each vocabulary file, so you need network access.

Paper: Petrov, La Malfa, Torr, and Bibi, "Language Model Tokenizers Introduce Unfairness Between Languages" (2023), https://arxiv.org/abs/2305.15425. Figure 1 is the same experiment across 17 tokenisers and many more languages. Read section 4 for the cost, latency, and context-length consequences.

## 4. Special Tokens And Glitch Tokens (Quirk 7)

What you're testing: typed text can become a control token, and some tokens exist in the vocabulary without the model having learned them.

```python
show("Hello<|endoftext|>world", ids=True)
print("eos id:", tok.eos_token_id)
for g in [" SolidGoldMagikarp", " TheNitromeFan", " davidjl", " RandomRedditorWithNo"]:
    show(g, ids=True)
```

Expected: `<|endoftext|>` becomes ID 50256, the real end-of-text token, and each glitch string is a single token.

To see the glitch behaviour rather than just the split, ask the model to repeat one:

```python
@torch.no_grad()
def complete(prompt, n=8):
    ids = tok(prompt, return_tensors="pt").input_ids
    out = model.generate(ids, max_new_tokens=n, do_sample=False, pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids.shape[1]:])

print(complete('Please repeat the word " SolidGoldMagikarp" back to me:'))
print(complete('Please repeat the word " banana" back to me:'))
```

What to look for: GPT-2 small is weak at instruction following either way, so compare the two outputs rather than judging one alone. The glitch token tends to produce something unrelated to its spelling.

Papers: Rumbelow and Watkins, "SolidGoldMagikarp (plus, prompt generation)" (2023), https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation, for the discovery and the Reddit-username explanation. Then Land and Bartolo, "Fishing for Magikarp: Automatically Detecting Under-trained Tokens in Large Language Models" (2024), https://arxiv.org/abs/2405.05417, for detection methods that work across model families, which is the direct follow-up to what step 5 tests.

## 5. The Failed Hypothesis: Centroid Distance

What you're testing: whether under-trained tokens sit close to the mean embedding. On GPT-J they do. On GPT-2 the famous ones don't.

```python
W = model.transformer.wte.weight.detach()            # (50257, 768)
dist = (W - W.mean(0)).norm(dim=1)
rank = dist.argsort()
pos = torch.empty_like(rank); pos[rank] = torch.arange(len(rank))

print("closest to centroid:", [tok.decode([i]) for i in rank[:15]])
for g in [" SolidGoldMagikarp", " TheNitromeFan", " davidjl", " RandomRedditorWithNo", " the", " Paris", " dog"]:
    i = tok.encode(g)[0]
    print(f"{g!r:24} dist={dist[i]:.2f}  percentile {100*pos[i]/len(W):5.1f}%")
```

Expected percentiles: SolidGoldMagikarp 28.6, TheNitromeFan 41.7, davidjl 49.9, RandomRedditorWithNo 12.5, the 25.2, Paris 16.7, dog 12.0. The closest-to-centroid list starts with ` externalToEVA`, control bytes, and `quickShip`.

Chart: a histogram of all 50,257 distances with the glitch tokens marked.

```python
plt.figure(figsize=(8, 3))
plt.hist(dist.numpy(), bins=120, color="#c3c2b7")
for g, c in [(" SolidGoldMagikarp", "#eb6834"), (" the", "#2a78d6"), (" dog", "#2a78d6")]:
    d = dist[tok.encode(g)[0]].item()
    plt.axvline(d, color=c); plt.text(d, plt.ylim()[1] * 0.9, g.strip(), rotation=90, color=c, fontsize=8, ha="right")
plt.xlabel("distance from embedding centroid"); plt.ylabel("tokens"); plt.tight_layout(); plt.savefig("centroid-distance.png", dpi=150)
```

What to look for: the glitch token lands inside the main bulk of the histogram, right next to ordinary words. The far left tail is where the control bytes live. That picture is the "what I got wrong" section in one image.

Paper: the Land and Bartolo paper above. It covers why embedding-distance alone is an incomplete detector and the indicators they use instead, and it discusses the GPT-J result the hypothesis came from.

## 6. Embeddings And Neighbours

What you're testing: token IDs become 768-dimensional vectors, and similar tokens end up nearby, including surface variants the model had to reconcile.

```python
Wn = W / W.norm(dim=1, keepdim=True)
def neighbours(word, k=8):
    ids = tok.encode(word); assert len(ids) == 1, f"{word!r} is {len(ids)} tokens"
    top = (Wn @ Wn[ids[0]]).topk(k + 1).indices[1:]
    print(f"{word!r:12} -> " + ", ".join(repr(tok.decode([i])) for i in top))

for w in [" king", " Paris", "Paris", " 7", " running", " happy"]:
    neighbours(w)
```

Expected: ` king` → ` kings`, ` King`, ` queen`, `King`, ` prince`, ` monarch`. ` Paris` → `Paris` first. ` 7` → ` 6`, ` 8`, ` 5`.

Chart: a 2D projection of a dozen tokens with PCA. Keep it to case and spacing variants so the point is visible.

```python
words = [" king", " King", "King", " queen", " Paris", "Paris", " London", "London", " 7", "7", " 6", " 8"]
X = torch.stack([W[tok.encode(w)[0]] for w in words])
X = X - X.mean(0)
U, S, V = torch.pca_lowrank(X, q=2)
Z = (X @ V[:, :2]).numpy()
plt.figure(figsize=(6, 5))
plt.scatter(Z[:, 0], Z[:, 1], color="#2a78d6")
for (x, y), w in zip(Z, words):
    plt.annotate(repr(w), (x, y), fontsize=9, xytext=(4, 4), textcoords="offset points")
plt.title("12 GPT-2 token embeddings, PCA to 2D"); plt.tight_layout(); plt.savefig("embedding-pca.png", dpi=150)
```

What to look for: ` Paris` and `Paris` sit close but not on top of each other. Same for the digits. The model closed most of the gap tokenisation opened, but not all of it.

Paper: Vaswani et al., "Attention Is All You Need" (2017), https://arxiv.org/abs/1706.03762. Section 3.4 (embeddings and softmax) and 5.1 (the 37,000-token BPE vocabulary) are the two paragraphs that connect to this article. Section 3.5 (positional encoding) sets up the bonus probe below. For word embeddings generally, Mikolov et al., "Efficient Estimation of Word Representations in Vector Space" (2013), https://arxiv.org/abs/1301.3781, is where king and queen come from.

## 7. Bonus: Positional Embeddings (Sets Up Article 3)

Vaswani et al. used fixed sine and cosine position encodings. GPT-2 learns its position vectors instead. Check whether it rediscovered the same shape.

```python
P = model.transformer.wpe.weight.detach()            # (1024, 768)
Pn = P / P.norm(dim=1, keepdim=True)
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].imshow((Pn[:256] @ Pn[:256].T).numpy(), cmap="viridis"); ax[0].set_title("cosine similarity, positions 0 to 255")
for d in range(4):
    ax[1].plot(P[:256, d].numpy(), label=f"dim {d}")
ax[1].legend(); ax[1].set_title("four position-embedding dimensions")
plt.tight_layout(); plt.savefig("positional-embeddings.png", dpi=150)
```

What to look for: a bright diagonal band in the left panel (nearby positions are similar) and smooth waves on the right. Compare with Figure 1 and section 3.5 of the paper.

## Self-Check: Answer Closed-Book, Then Verify

1. Why can't a byte-level BPE tokeniser produce an unknown token? (Step 1, the round-trip check.)
2. Why is ` Paris` one token, yet a prompt ending in a space breaks the prediction? (Step 2, the token list.)
3. What gets merged in English that doesn't get merged in Hindi? (Step 3, bytes versus tokens.)
4. Why does one emoji token decode to � while the full sequence decodes correctly? (Step 1.)
5. Give one example of how digit splitting can hurt arithmetic. (Step 1: `1234567` as `123` `45` `67`. Then try `report("17 + 25 =", " 42")` and see what GPT-2 prefers.)
6. How does the gap between tokeniser training data and model training data create glitch tokens? (Steps 4 and 5.)

## Files You'll Have At The End

| File | Used in the article as |
|---|---|
| `next-token-after-space.png` | Trailing-space proof chart |
| `token-tax.png` | Token tax chart |
| `centroid-distance.png` | Optional figure for "What I Got Wrong" |
| `embedding-pca.png` | Optional figure for "Where Do Tokens Become Meaning?" |
| `positional-embeddings.png` | Article 3 |

Everything here is also in the original notebook, `submissions/week1/week1_transformer_probing.ipynb`, in the same order.
