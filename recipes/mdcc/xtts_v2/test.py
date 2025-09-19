import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.tts.layers.xtts.tokenizer import Tokenizer
from TTS.tts.utils.text.tokenizer import TTSTokenizer

print("Loading model...")
config = XttsConfig()
config.load_json("config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="./")
#model.cuda()

#text = "我挥一挥衣袖，不带走一片云彩。"
#text = "我挥一挥衣袖不带走一23456789"
#text = "不带走一片云彩"
text = "天文台于下午三点挂起八号风球，所有渡轮停止运营。"

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["speaker.wav"])
#gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["andy.wav"])

print("Inference...")
out = model.inference(
    text,
    "yue",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.7, # Add custom parameters here
    #repetition_penalty=1.0,  # 降低重复惩罚（默认通常是1.1或更高）
    #return_dict_in_generate=True,
    #output_scores=True,
)
torchaudio.save("demo.wav", torch.tensor(out["wav"]).unsqueeze(0), 22050)
tokens = model.tokenizer.encode(text, 'yue')
print(f"原始文本: {text}")
print(f"Tokens: {tokens}")
print('decode:', model.tokenizer.decode(tokens))
