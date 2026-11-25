"""jorshimayor's figure kit: the Writing Studio figure kit loaded with this profile's brand.

The kit itself lives in the skill (plugins/writing-studio/skills/writing-studio/scripts/figure_kit.py)
and the brand in profiles/jorshimayor.brand.json, so there is one copy of each.
"""
import os
import sys

_SKILL = os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "writing-studio", "skills", "writing-studio")
sys.path.insert(0, os.path.join(_SKILL, "scripts"))
import figure_kit as _kit  # noqa: E402

_kit.use_brand(os.path.join(_SKILL, "profiles", "jorshimayor.brand.json"))
from figure_kit import *  # noqa: E402,F401,F403
from figure_kit import E, CSS, FONTS, WIDTH, ATT, VIC, GHOST, shoot  # noqa: E402,F401
