from typing import List

import re
import pycantonese

from .jyutpingToPhonemes import JYUTPING_DICT

# @deprecated: no reference
def _cantonese_character_to_jyutping(text: str) -> List[str]:
    jyutpings = pycantonese.characters_to_jyutping(text)
    ret = []
    for word in jyutpings:
        jyutpingWord = word[1]
        ret.extend(re.findall(r'[a-zA-Z]+[0-9]+', jyutpingWord))

    return ret

# @deprecated: no reference
def _cantonese_jyutping_to_phoneme(pinyin: str) -> str:
    segment = pinyin[:-1]
    tone = pinyin[-1]
    phoneme = JYUTPING_DICT.get(segment, [""])[0]
    return phoneme + tone

def cantonese_text_to_phonemes(text: str, seperator: str = "|") -> str:
    jyutpings = pycantonese.characters_to_jyutping(text)
    tokens = []
    for word in jyutpings:
        jyutpingWord = word[1]
        if jyutpingWord == None:
            tokens.append('')
        else:
            tokens.extend(re.findall(r'[a-zA-Z]+[0-9]+', jyutpingWord))

        tokens.append('')

    return seperator.join(tokens)
