import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.tts.layers.xtts.tokenizer import Tokenizer

print("Loading model...")
config = XttsConfig()
config.load_json("config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="./")
#model.cuda()

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["female.wav"])

print("Inference...")
out = model.inference(
    "我挥一挥衣袖，不带走一片云彩。", #ngo5 wui2 syut3 jyut6 jyu5", #
    "yue",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.7, # Add custom parameters here
)
torchaudio.save("demo.wav", torch.tensor(out["wav"]).unsqueeze(0), 22050)