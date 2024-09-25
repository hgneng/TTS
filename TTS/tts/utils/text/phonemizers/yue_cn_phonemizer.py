from typing import Dict
import sys
#sys.path.append('/home/hgneng/code/hgneng/TTS')
from TTS.tts.utils.text.cantonese.phonemizer import cantonese_text_to_phonemes
from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_ZH_PUNCS = "、.,[]()?!〽~『』「」【】"


class YUE_CN_Phonemizer(BasePhonemizer):
    """🐸TTS Yue-Cn phonemizer using functions in `TTS.tts.utils.text.cantonese.phonemizer`

    Args:
        punctuations (str):
            Set of characters to be treated as punctuation. Defaults to `_DEF_ZH_PUNCS`.

        keep_puncs (bool):
            If True, keep the punctuations after phonemization. Defaults to False.

    Example ::

        "这是，样本中文。" -> `d|ʒ|ø|4| |ʂ|ʏ|4| |，| |i|ɑ|ŋ|4|b|œ|n|3| |d|ʒ|o|ŋ|1|w|œ|n|2| |。`
    """

    language = "yue-cn" # what about yue-hk?

    def __init__(self, punctuations=_DEF_ZH_PUNCS, keep_puncs=False, **kwargs):  # pylint: disable=unused-argument
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)

    @staticmethod
    def name():
        return "yue_cn_phonemizer"

    @staticmethod
    def phonemize_yue_cn(text: str, separator: str = "|") -> str:
        ph = cantonese_text_to_phonemes(text, separator)
        return ph

    def _phonemize(self, text, separator):
        return self.phonemize_yue_cn(text, separator)

    @staticmethod
    def supported_languages() -> Dict:
        return {"yue-cn": "Cantonese"}

    def version(self) -> str:
        return "0.0.1"

    def is_available(self) -> bool:
        return True

# import opencc
# if __name__ == "__main__":
#     text = "English Text"
#     #text = "这是，样本中文。"
#     converter = opencc.OpenCC('s2t')
#     text = converter.convert(text)
#     print(text)
#     #text = "這是，樣本中文。"
#     e = YUE_CN_Phonemizer()
#     print(e.supported_languages())
#     print(e.version())
#     print(e.language)
#     print(e.name())
#     print(e.is_available())
#     print("`" + e.phonemize(text) + "`")
