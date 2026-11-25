"""ERC-4626 inflation attack figures, v2 (illustrated). Every number comes from the Foundry
suite in Web3-Hack-Analysis chains/evm/erc4626-inflation-attack (Foundry 1.9.0, solc 0.8.25,
OpenZeppelin Contracts 5.4.0) and design/examples/erc4626_model.py.

    python3 design/figures/erc4626_v2.py drafts/images/png [figure ...]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figures.kit import E, figure, render, vault, coins, ticket, avatar, arrow, mini_vault  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ONLY = set(sys.argv[2:])
KICK = "ERC-4626 inflation attack"
RUN = ("Attack: 1 wei deposit, 10,000 token donation, 9,000 token victim deposit. "
       "Foundry 1.9.0, solc 0.8.25, OpenZeppelin Contracts 5.4.0, Web3-Hack-Analysis test suite.")

STORY_CSS = """
.trace{position:relative;height:30px;margin:0 0 6px}
.trace::before{content:"";position:absolute;left:131px;right:131px;top:14px;height:2px;background:#c3c2b7}
.trace span{position:absolute;top:4px;width:22px;height:22px;border-radius:50%;background:var(--paper);border:3px solid var(--blue)}
.trace span.brk{background:var(--ink);border-color:var(--ink);box-shadow:inset 0 0 0 5px var(--paper)}
.story{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.step{padding:18px 18px 16px;display:flex;flex-direction:column;gap:12px;}
.step.bad{border:2px solid var(--ink)}
.top{display:flex;justify-content:space-between;align-items:center}
.n{font:700 13px var(--mono);letter-spacing:.1em;color:var(--ink3)}
.step h3{font:700 19px/1.2 var(--head);letter-spacing:-.01em;min-height:46px}
.scene{position:relative;height:230px;display:flex;align-items:flex-end;justify-content:center}
.ledger{margin-top:auto;border-top:1px dashed #d6d5cf;padding-top:10px;display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font:500 14px var(--mono)}
.ledger dt{color:var(--ink3)} .ledger dd{text-align:right;font-weight:700}
.eq{font:600 14px var(--mono);color:var(--ink);background:#f6f5f1;border-radius:10px;padding:8px 10px;text-align:center}
"""


def attack_flow():
    sliver = coins(0, "att", w=40, step=10)
    att10 = coins(10, "att", w=40, step=10)
    vic9 = coins(9, "vic", w=40, step=10)

    def step(n, actor, title, scene, ledger, extra="", bad=False):
        rows = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in ledger)
        return (f'<div class="card step{" bad" if bad else ""}"><div class="top"><span class="n">STEP {n}</span>{actor}</div>'
                f'<h3>{title}</h3><div class="scene">{scene}</div>{extra}<dl class="ledger">{rows}</dl></div>')

    s1 = step(1, avatar("att", "Attacker"), "Deposits 1 wei into the empty vault",
              f'<div style="display:flex;align-items:flex-end;gap:10px">{vault([sliver], w=140, h=210)}'
              f'<div style="margin-bottom:60px">{ticket("1 SHARE", "att", w=100)}</div></div>',
              [("shares", "1"), ("assets", "1 wei")],
              '<div class="eq">1 wei buys the only share</div>')
    s2 = step(2, avatar("att", "Attacker"), "Sends 10,000 tokens straight to the vault",
              f'<div style="display:flex;align-items:flex-end;gap:8px"><div style="margin-bottom:70px">{arrow(46, 22, label="transfer")}</div>{vault([att10], w=140, h=210)}</div>',
              [("shares", "1"), ("assets", "10,000")],
              '<div class="eq">no deposit(), so no new shares</div>')
    s3 = step(3, avatar("vic", "Victim"), "Deposits 9,000 tokens",
              f'<div style="display:flex;align-items:flex-end;gap:10px">{vault([att10, vic9], w=140, h=210)}'
              f'<div style="margin-bottom:66px;position:relative"><span class="circ">{ticket("0 SHARES", "ghost", w=104, empty=True)}</span></div></div>'
              f'<div class="note" style="position:absolute;right:-6px;top:-6px;transform:rotate(-3deg)">rounds down to 0</div>',
              [("shares", "1"), ("assets", "19,000")],
              '<div class="eq">9,000 × 1 / 10,000 = <span class="hl">0.8999</span> → 0</div>', bad=True)
    s4 = step(4, avatar("att", "Attacker"), "Redeems the 1 share and walks out with everything",
              f'<div style="display:flex;align-items:flex-end;gap:10px">{vault([], w=120, h=210, label="EMPTY")}'
              f'<div style="display:flex;align-items:flex-end;gap:1px;margin-bottom:6px">{att10}{vic9}</div></div>',
              [("shares", "0"), ("assets", "0")],
              '<div class="eq" style="background:#fdeee8;color:#a8401a">19,000 out · profit 9,000</div>')
    trace = '<div class="trace">' + "".join(
        f'<span class="{"brk" if i == 2 else ""}" style="left:calc({i} * (100% - 54px) / 4 + {i * 18}px + (100% - 54px) / 8 - 11px)"></span>'
        for i in range(4)) + "</div>"
    body = trace + f'<div class="story">{s1}{s2}{s3}{s4}</div>'
    legend = (f'<div style="display:flex;gap:22px;margin-top:18px;font:500 16px var(--ui);color:var(--ink2)">'
              f'<span style="display:flex;align-items:center;gap:8px">{coins(1, "att", w=22, step=5)}attacker\'s tokens</span>'
              f'<span style="display:flex;align-items:center;gap:8px">{coins(1, "vic", w=22, step=5)}victim\'s tokens</span>'
              f'<span style="display:flex;align-items:center;gap:8px">one coin ≈ 1,000 tokens</span></div>')
    page = figure(KICK, "The inflation attack in four steps",
                  "The donation in step 2 mints no shares, so the attacker's single share owns the whole vault. "
                  "<strong>The victim's 9,000 tokens round down to 0 shares.</strong>",
                  body + legend, RUN, STORY_CSS)
    render(page, f"{OUT}/attack-flow.png")


DEF_CSS = """
.defs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.def{padding:20px;display:flex;flex-direction:column;gap:14px}
.def .hd{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.def .lab{font:700 12px var(--mono);letter-spacing:.1em;color:var(--ink3)}
.def h3{font:800 25px/1.05 var(--display);letter-spacing:-.03em;margin-top:6px}
.def .scene{height:250px;display:flex;align-items:flex-end;justify-content:center;gap:12px;position:relative}
.formula{font:600 14.5px/1.6 var(--mono);background:#f6f5f1;border-radius:12px;padding:10px 12px}
.out{display:grid;grid-template-columns:auto 1fr;gap:8px 10px;align-items:center;font:500 16px var(--ui);border-top:1px dashed #d6d5cf;padding-top:12px}
.out b{font:700 14px var(--mono);text-align:right}
.ok{color:#0f7a54}
.pile{position:relative;width:118px;height:110px}
.pile > div{position:absolute}
.cap{font:600 12.5px var(--mono);color:var(--ink2);text-align:center;margin-top:6px}
.book{width:84px;height:104px;border:3px solid var(--ink);border-radius:6px 10px 10px 6px;background:#fff;box-shadow:inset 10px 0 0 #e9e8e3;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;font:700 13px var(--mono)}
.bounce{display:flex;flex-direction:column;align-items:center;gap:6px;position:relative}
.x{font:800 13px var(--display);letter-spacing:.06em;color:var(--red);border:2.5px solid var(--red);border-radius:6px;padding:4px 7px;transform:rotate(-8deg);background:#fff}
"""


def defences():
    small = lambda k: coins(10, "att", w=34, step=8)
    holds = '<span class="stamp ok">holds</span>'
    c1 = (f'<div class="card def"><div class="hd"><div><div class="lab">DEFENCE 1</div><h3>Dead shares</h3></div>{holds}</div>'
          f'<div class="scene">{vault([small(0)], w=130, h=200)}'
          f'<div><div class="pile">' + "".join(
              f'<div style="left:{i * 6}px;top:{i * 14}px;transform:rotate({-6 + i * 4}deg)">{ticket("SHARE", "ghost", w=100)}</div>' for i in range(3)) +
          f'</div><div class="cap">1,000 shares<br>sent to 0xdead</div></div></div>'
          f'<div class="formula">assets × (supply <span class="hl">+ 1,000 burned</span>)<br>/ totalAssets</div>'
          f'<div class="out"><span>Victim gets</span><b>900 shares</b><span>Victim loses</span><b>4.73 tokens</b>'
          f'<span>Attacker</span><b class="ok">−9,990</b></div></div>')
    c2 = (f'<div class="card def"><div class="hd"><div><div class="lab">DEFENCE 2</div><h3>Virtual shares, offset 6</h3></div>{holds}</div>'
          f'<div class="scene">{vault([small(0), coins(1, "vic", w=34, step=8, ghost=True)], w=130, h=200)}'
          f'<div><div class="pile">' + "".join(
              f'<div style="left:{i * 6}px;top:{i * 14}px">{ticket("10^6", "ghost", w=100, empty=True)}</div>' for i in range(3)) +
          f'</div><div class="cap">10^6 virtual shares<br>+1 virtual asset</div></div></div>'
          f'<div class="formula">assets × (supply <span class="hl">+ 10^offset</span>)<br>/ (totalAssets <span class="hl">+ 1</span>)</div>'
          f'<div class="out"><span>Victim gets</span><b>1,799,999 shares</b><span>Victim loses</span><b>0.003 tokens</b>'
          f'<span>Attacker</span><b class="ok">−5,000</b></div></div>')
    c3 = (f'<div class="card def"><div class="hd"><div><div class="lab">DEFENCE 3</div><h3>Internal accounting</h3></div>{holds}</div>'
          f'<div class="scene"><div class="book"><span style="color:var(--ink3);font-size:11px">LEDGER</span>assets<br>1 wei</div>'
          f'<div class="bounce">{coins(10, "att", w=40, step=8)}<span class="x">not counted</span><span class="cap">10,000 donated<br>by transfer()</span></div></div>'
          f'<div class="formula">assets × supply<br>/ <span class="hl">accountedAssets</span></div>'
          f'<div class="out"><span>Victim gets</span><b>9,000 × 10^18 shares</b><span>Victim loses</span><b>0</b>'
          f'<span>Attacker</span><b class="ok">−10,000</b></div></div>')
    page = figure(KICK, "Three defences that hold",
                  "Each one changes a single term in <span class=\"mono\">shares = assets × supply / totalAssets</span>. "
                  "<strong>Against the same attack, every one of them makes the attacker lose money.</strong>",
                  f'<div class="defs">{c1}{c2}{c3}</div>', RUN + " Coins: one per 1,000 tokens.", DEF_CSS)
    render(page, f"{OUT}/defences-formula.png")


SCORE_CSS = """
.board{padding:10px 26px}
.row{display:grid;grid-template-columns:250px 1fr 120px 150px 110px;align-items:center;gap:18px;padding:16px 0;border-bottom:1px solid var(--line)}
.row:last-child{border-bottom:0}
.row.head{font:600 12px var(--mono);letter-spacing:.1em;color:var(--ink3);padding:10px 0}
.name{display:flex;align-items:center;gap:12px;font:600 18px var(--ui)}
.name svg{flex:none}
.track{height:18px;border-radius:9px;background:#efeee9;overflow:hidden}
.track i{display:block;height:100%;border-radius:9px}
.pct{font:800 24px var(--display);letter-spacing:-.02em;text-align:right}
.pnl{text-align:right}
.v{text-align:center}
.v .stamp{font-size:13px;padding:6px 9px}
"""


def test_results():
    rows = [("Naive vault", 100, "100 %", "+9,000", "broken", "att"),
            ("OpenZeppelin, offset 0", 29.63, "29.63 %", "−3,667", "leaks", "att"),
            ("Dead shares (1,000)", 0.0526, "0.0526 %", "−9,990", "holds", "ok"),
            ("OpenZeppelin, offset 6", 0, "0 %", "−5,000", "holds", "ok"),
            ("Internal accounting", 0, "0 %", "−10,000", "holds", "ok")]
    out = ['<div class="row head"><span>VAULT</span><span>VICTIM\'S LOSS ON A 9,000 DEPOSIT</span><span style="text-align:right">LOSS</span>'
           '<span style="text-align:right">ATTACKER P&amp;L</span><span style="text-align:center">VERDICT</span></div>']
    for name, v, lab, pnl, verdict, kind in rows:
        col = "var(--orange)" if kind == "att" else "var(--blue)"
        stamp_col = "#a8401a" if kind == "att" else "#0f7a54"
        pct = f'<span class="circ">{lab}</span>' if name.endswith("offset 0") else lab
        icon = mini_vault()
        out.append(f'<div class="row"><span class="name">{icon}{E(name)}</span>'
                   f'<div class="track"><i style="width:{max(v, 0.6)}%;background:{col}"></i></div>'
                   f'<span class="pct">{pct}</span><span class="pnl"><span class="pill {"att" if pnl.startswith("+") else "ok"}">{pnl}</span></span>'
                   f'<span class="v"><span class="stamp" style="color:{stamp_col}">{verdict}</span></span></div>')
    note = ('<div class="note" style="position:absolute;left:452px;top:126px;transform:rotate(-2deg)">'
            'still leaks →</div>')
    body = f'<div class="card board" style="position:relative">{"".join(out)}{note}</div>'
    page = figure(KICK, "Five vaults, one attack: who loses?",
                  "Only the naive vault pays the attacker. <strong>OpenZeppelin's default offset of 0 still costs the victim 29.6%</strong>; "
                  "dead shares, offset 6 and internal accounting all leave the attacker worse off.",
                  body, RUN + " Attacker P&amp;L is profit in tokens.", SCORE_CSS)
    render(page, f"{OUT}/test-results.png")


CARD_CSS = """
.duo{display:grid;grid-template-columns:330px minmax(0,1fr);gap:20px}
.pane{padding:22px;display:flex;flex-direction:column;gap:14px}
.lab{font:700 12px var(--mono);letter-spacing:.1em;color:var(--ink3);text-transform:uppercase}
.pane h3{font:700 20px/1.2 var(--head)}
.state{display:flex;flex-wrap:wrap;gap:8px}
.calc{font:600 17px/1.5 var(--mono);background:#f6f5f1;border-radius:12px;padding:12px 14px}
.calc small{display:block;font:500 13px var(--mono);color:var(--ink3);margin-bottom:4px}
.res{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.who{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.who > div{border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:12px;border:1.5px solid var(--line);background:#fff}
.who b{display:block;font:800 26px var(--display);letter-spacing:-.02em}
.who span{font:400 16px var(--ui);color:var(--ink2)}
.ok{color:#0f7a54} .bad{color:#a8401a}
.lane{display:grid;grid-template-columns:200px minmax(0,1fr) 290px;align-items:center;gap:20px;padding:20px 22px}
.lane + .lane{margin-top:14px}
.dec{display:grid;grid-template-columns:minmax(0,1fr) 70px minmax(0,1fr);align-items:center;gap:0;row-gap:0}
.q{padding:16px 18px;font:600 18px/1.3 var(--head);display:flex;align-items:center;gap:14px}
.q .qn{flex:none;width:34px;height:34px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font:800 15px var(--display)}
.yes{display:flex;flex-direction:column;align-items:center;font:700 12px var(--mono);color:var(--blue)}
.act{padding:14px 16px;display:flex;align-items:center;gap:12px;font:400 17px/1.35 var(--ui);border:2px solid var(--blue);background:var(--btint)}
.act b{font-family:var(--head);font-weight:700}
.down{grid-column:1;display:flex;align-items:center;gap:10px;padding:6px 0 6px 30px;font:700 12px var(--mono);color:var(--ink3)}
.down i{display:block;width:2px;height:30px;background:#c3c2b7}
"""


def _vault_state(att=10, vic=0, dead=False, ghost=False, label="VAULT"):
    stacks = [coins(att, "att", w=38, step=8)]
    if vic:
        stacks.append(coins(vic, "vic", w=38, step=8))
    if ghost:
        stacks.append(coins(1, "vic", w=38, step=8, ghost=True))
    return vault(stacks, w=150, h=210, label=label)


def _defence_card(fname, kicker, title, dek, state_pills, scene, calc_lines, result_html, redeem, victim, attacker, verdict):
    stamp_col = "#0f7a54" if verdict == "holds" else "#a8401a"
    left = (f'<div class="card pane"><span class="lab">Vault after 1 wei + 10,000 donation</span>'
            f'<div style="display:flex;justify-content:center">{scene}</div>'
            f'<div class="state">{"".join(f"<span class=pill>{E(x)}</span>" for x in state_pills)}</div></div>')
    right = (f'<div class="card pane" style="position:relative"><div style="display:flex;justify-content:space-between;align-items:center">'
             f'<span class="lab">Victim deposits 9,000</span><span class="stamp" style="color:{stamp_col}">{verdict}</span></div>'
             f'<div class="calc">{calc_lines}</div><div class="res">{result_html}</div>'
             f'<div class="calc"><small>attacker redeems</small>{redeem}</div>'
             f'<div class="who"><div>{avatar("vic")}<div><span>victim loses</span><b class="{"ok" if victim[1] else "bad"}">{victim[0]}</b></div></div>'
             f'<div>{avatar("att")}<div><span>attacker</span><b class="{"ok" if attacker[1] else "bad"}">{attacker[0]}</b></div></div></div></div>')
    page = figure(KICK + " · " + kicker, title, dek, f'<div class="duo">{left}{right}</div>', RUN, CARD_CSS)
    render(page, f"{OUT}/{fname}.png")


def defence_dead():
    burned = "".join(f'<div style="position:absolute;left:{i * 5}px;top:{i * 12}px;transform:rotate({-5 + i * 4}deg)">{ticket("DEAD", "ghost", w=84)}</div>' for i in range(3))
    scene = (f'<div style="display:flex;align-items:flex-end;gap:10px">{_vault_state()}<div><div style="position:relative;width:100px;height:96px">{burned}</div>'
             f'<div style="font:600 12px var(--mono);color:var(--ink2);text-align:center">1,000 → 0xdead</div></div></div>')
    _defence_card("defence-dead-shares", "Defence 1", "Dead shares: 1,000 burned at deployment",
                  "A seed deposit mints 1,000 shares to a dead address, so supply never drops to 1. "
                  "<strong>The donation now mostly belongs to shares nobody can redeem.</strong>",
                  ["totalSupply = 1,001", "totalAssets = 10,000"], scene,
                  "9,000 × <span class=\"hl\">1,001</span> / 10,000 = 900.9",
                  f'{ticket("900 SHARES", "vic", w=150)}<span style="font:400 17px var(--ui);color:var(--ink2)">victim owns 900 of 1,901</span>',
                  "1 share × 19,000 / 1,901 = 9.99 tokens",
                  ("4.73 tokens", True), ("−9,990", True), "holds")


def defence_virtual():
    ghosts = "".join(f'<div style="position:absolute;left:{i * 5}px;top:{i * 12}px">{ticket("10^6", "ghost", w=84, empty=True)}</div>' for i in range(3))
    scene = (f'<div style="display:flex;align-items:flex-end;gap:10px">{_vault_state(ghost=True)}<div><div style="position:relative;width:100px;height:96px">{ghosts}</div>'
             f'<div style="font:600 12px var(--mono);color:var(--ink2);text-align:center">virtual shares</div></div></div>')
    _defence_card("defence-virtual-shares", "Defence 2", "Virtual shares, offset 6",
                  "OpenZeppelin adds 10^offset virtual shares and 1 virtual asset to the maths. "
                  "<strong>With offset 6 the attacker's 1 wei buys 1,000,000 shares, and the donation is shared out.</strong>",
                  ["totalSupply = 1,000,000", "totalAssets = 10,000", "+10^6 virtual, +1 wei"], scene,
                  "9,000 × (1,000,000 <span class=\"hl\">+ 1,000,000</span>)<br>/ (10,000 <span class=\"hl\">+ 1 wei</span>) ≈ 1,800,000",
                  f'{ticket("1,799,999", "vic", w=150)}<span style="font:400 17px var(--ui);color:var(--ink2)">of about 2.8M real shares</span>',
                  "1,000,000 × 19,000 / (2,800,000 + 1,000,000) ≈ 5,000",
                  ("0.003 tokens", True), ("−5,000", True), "holds")


def defence_internal():
    scene = (f'<div style="display:flex;align-items:flex-end;gap:14px"><div style="width:96px;height:120px;border:3px solid var(--ink);border-radius:6px 10px 10px 6px;'
             f'background:#fff;box-shadow:inset 10px 0 0 #e9e8e3;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;font:700 14px var(--mono)">'
             f'<span style="font-size:11px;color:var(--ink3)">LEDGER</span>assets<br>1 wei</div>'
             f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px">{coins(10, "att", w=40, step=8)}'
             f'<span class="stamp" style="color:var(--red);font-size:12px;background:#fff">not counted</span></div></div>')
    _defence_card("defence-internal-accounting", "Defence 3", "Internal accounting",
                  "The vault tracks deposits in its own variable instead of reading its token balance. "
                  "<strong>The donation never enters the formula.</strong>",
                  ["totalSupply = 1", "accountedAssets = 1 wei", "balanceOf = 10,000 (ignored)"], scene,
                  "9,000 × (1 + 1) / (<span class=\"hl\">1 wei</span> + 1)<br>= 9,000 × 10^18",
                  f'{ticket("9,000×10^18", "vic", w=170)}<span style="font:400 17px var(--ui);color:var(--ink2)">everything the victim paid for</span>',
                  "1 share × 9,000 / (9,000 × 10^18) = 1 wei",
                  ("0", True), ("−10,000", True), "holds")


def non_defence():
    lane = lambda tag, dep, calc, outcome, ok_html: (
        f'<div class="card lane"><div style="display:flex;align-items:center;gap:12px">{avatar("vic")}<div><div class="lab">{tag}</div>'
        f'<div style="font:800 30px var(--display)">{dep}</div></div></div><div class="calc" style="text-align:center">{calc}</div>'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px">{outcome}{ok_html}</div></div>')
    a = lane("deposit", "9,000", "9,000 × 1 / 10,000 = 0.8999 → 0<br><span class=\"hl\">require(shares != 0)</span> fails",
             '<span class="stamp" style="color:var(--red)">reverts</span>',
             '<span style="font:400 16px var(--ui);color:var(--ink2);text-align:center">blocked: the vault is unusable<br>for small deposits</span>')
    b = lane("deposit", "15,000", "15,000 × 1 / 10,000 = 1.4999 → 1<br>check passes",
             f'<span class="circ">{ticket("1 SHARE", "vic", w=120)}</span>',
             '<span style="font:800 24px var(--display);color:#a8401a">worth 12,500: −2,500</span>')
    body = (f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px"><span class="pill">totalSupply = 1</span>'
            f'<span class="pill">totalAssets = 10,000</span><span class="pill att">require(shares != 0)</span></div>{a}{b}'
            f'<div class="note" style="margin:10px 0 0 760px;transform:rotate(-2deg)">still loses 2,500</div>')
    page = figure(KICK + " · the non-defence", "Reverting on zero shares doesn't fix it",
                  "Below the inflated share price every deposit reverts, so theft becomes denial of service. "
                  "<strong>Above it the check passes and the partial loss goes through.</strong>",
                  body, RUN, CARD_CSS)
    render(page, f"{OUT}/non-defence-revert-on-zero.png")


def share_rounding():
    css = CARD_CSS + """
.three{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px}
.three .pane{align-items:center;text-align:center}
.mini{font:400 17px/1.4 var(--ui);color:var(--ink2)}
"""
    p1 = (f'<div class="card pane"><span class="lab">after steps 1 and 2</span>{_vault_state(10)}'
          f'{ticket("1 SHARE", "att", w=120)}<p class="mini">attacker holds the only share;<br>vault holds 10,000</p></div>')
    p2 = (f'<div class="card pane" style="position:relative"><span class="lab">step 3: victim deposits 15,000</span>'
          f'<div style="display:flex;align-items:flex-end;gap:6px">{avatar("vic")}{coins(15, "vic", w=40, step=8)}</div>'
          f'<div class="calc">15,000 × 1 / 10,000 = <span class="hl">1.4999</span></div>'
          f'<div style="display:flex;gap:10px;align-items:center"><span class="circ">{ticket("1 SHARE", "vic", w=110)}</span>'
          f'{ticket("0.4999", "ghost", w=96, empty=True)}</div>'
          f'<div class="note" style="transform:rotate(-2deg)">0.4999 never minted</div></div>')
    p3 = (f'<div class="card pane"><span class="lab">after step 3</span>{_vault_state(10, 15)}'
          f'<p class="mini">2 shares, 25,000 tokens,<br>so <b style="color:var(--ink)">1 share = 12,500</b></p>'
          f'<div class="who" style="width:100%"><div style="flex-direction:column;gap:4px">{avatar("vic")}<span>paid 15,000</span><b class="bad">−2,500</b></div>'
          f'<div style="flex-direction:column;gap:4px">{avatar("att")}<span>paid 10,000</span><b class="bad">+2,500</b></div></div></div>')
    page = figure(KICK, "The 15,000 token deposit: where the 2,500 goes",
                  "A deposit bigger than the donation still gets a share, but rounding throws away the fraction. "
                  "<strong>Both shares end up worth 12,500, so 2,500 moves from victim to attacker.</strong>",
                  f'<div class="three">{p1}{p2}{p3}</div>', RUN + " Coins: one per 1,000 tokens.", css)
    render(page, f"{OUT}/share-rounding.png")


def defence_decision():
    qs = [("Does totalAssets() read a live token balance?", "No", "<b>Internal accounting already.</b> Add a seed or offset."),
          ("Are you on OpenZeppelin's ERC4626?", "Yes", "<b>Override _decimalsOffset()</b> to 6 or more."),
          ("Do you control deployment?", "Yes", "<b>Seed deposit</b>, shares burned to 0xdead."),
          ("Does an oracle read your share price?", "Yes", "<b>Internal accounting</b>, plus a seed or offset.")]
    rows = []
    for i, (q, ans, act) in enumerate(qs):
        rows.append(f'<div class="card q"><span class="qn">{i + 1}</span>{E(q)}</div>'
                    f'<div class="yes">{E(ans.upper())}{arrow(60, 22, color="#2a78d6")}</div>'
                    f'<div class="card act">{mini_vault(30, "#1d5fae")}<span>{act}</span></div>')
        if i < len(qs) - 1:
            other = "YES" if ans == "No" else "NO"
            rows.append(f'<div class="down"><i></i>{other}</div><div></div><div></div>')
    page = figure(KICK, "Which defence fits your vault?",
                  "Answer from the top and stop at the first match. "
                  "<strong>Combinations are cheap: an offset plus a seed deposit covers rounding and donations together.</strong>",
                  f'<div class="dec">{"".join(rows)}</div>',
                  "Pick one as the defence and keep a minimum-shares-out check in the front end as the user's second layer.", CARD_CSS)
    render(page, f"{OUT}/defence-decision.png")


def incidents_timeline():
    css = """
.tl{position:relative;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;padding-top:6px}
.tl::before{content:"";position:absolute;left:0;right:0;top:263px;height:3px;background:#c3c2b7}
.ev{display:flex;flex-direction:column;align-items:center;gap:10px}
.ev .c{width:100%;padding:14px;display:flex;flex-direction:column;gap:6px;height:236px}
.ev .d{font:700 12px var(--mono);letter-spacing:.08em;color:var(--ink3)}
.ev .n{font:700 17px/1.2 var(--head)}
.ev .a{font:800 30px/1 var(--display);letter-spacing:-.02em}
.ev .v{font:400 15px/1.3 var(--ui);color:var(--ink2);margin-top:auto}
.dot{width:22px;height:22px;border-radius:50%;border:4px solid;background:var(--paper);z-index:1}
.legend{display:flex;gap:24px;margin-top:22px;font:400 17px var(--ui);color:var(--ink2)}
.legend span{display:flex;align-items:center;gap:8px}
.legend i{width:14px;height:14px;border-radius:50%;border:3px solid}
"""
    events = [("Apr 2023", "Yearn yUSDT", "$11.6M", "misconfiguration", "o"),
              ("Oct 2025", "Belong Staking", "caught in audit", "classic attack", "b"),
              ("Dec 2025", "Yearn yTUSD", "$293K", "misconfiguration", "o"),
              ("Apr 2026", "Thetanuts new vault", "$50K", "classic attack", "b"),
              ("Jun 2026", "Thetanuts legacy", "$105K net", "rounding at ~0 supply", "o"),
              ("Jul 2026", "Summer.fi", "$6.04M", "stale strategy", "o")]
    cards = []
    for d, n, a, v, k in events:
        col = "var(--orange)" if k == "o" else "var(--blue)"
        big = a.startswith("$1") or a.startswith("$6")
        amt = f'<span class="circ">{E(a)}</span>' if a == "$11.6M" else E(a)
        cards.append(f'<div class="ev"><div class="card c" style="border-top:5px solid {col}">{mini_vault(30)}<span class="d">{E(d)}</span>'
                     f'<span class="n">{E(n)}</span><span class="a" style="color:{"#a8401a" if k == "o" else "#1d5fae"};font-size:{30 if big or a.startswith("$") else 20}px">{amt}</span>'
                     f'<span class="v">{E(v)}</span></div><span class="dot" style="border-color:{col}"></span></div>')
    legend = ('<div class="legend"><span><i style="border-color:var(--blue)"></i>first depositor attack on an empty vault</span>'
              '<span><i style="border-color:var(--orange)"></i>the same ratio moved another way</span></div>')
    page = figure(KICK, "Share-price incidents, 2023 to 2026",
                  "Two textbook cases in three years. <strong>The expensive ones moved the same ratio from the configuration side.</strong>",
                  f'<div class="tl">{"".join(cards)}</div>{legend}',
                  "Amounts as reported by PeckShield, SlowMist, DarkNavy, banteg and the Summer.fi post-mortem.", css)
    render(page, f"{OUT}/incidents-timeline.png")


FIGS = {"attack-flow": attack_flow, "defences-formula": defences, "test-results": test_results,
        "share-rounding": share_rounding, "defence-dead-shares": defence_dead, "defence-virtual-shares": defence_virtual,
        "defence-internal-accounting": defence_internal, "non-defence-revert-on-zero": non_defence,
        "defence-decision": defence_decision, "incidents-timeline": incidents_timeline}

if __name__ == "__main__":
    for name, fn in FIGS.items():
        if not ONLY or name in ONLY:
            fn()
            print("wrote", f"{OUT}/{name}.png")
