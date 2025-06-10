import os

# Trainer: Where the ✨️ happens.
# TrainingArgs: Defines the set of arguments of the Trainer.
from trainer import Trainer, TrainerArgs

# GlowTTSConfig: all model related values for training, validating and testing.
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.tts.configs.shared_configs import CharactersConfig
# BaseDatasetConfig: defines name, formatter and path of the dataset.
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.glow_tts import GlowTTS
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

# we use the same path as this script as our training folder.
output_path = os.path.dirname(os.path.abspath(__file__))

# DEFINE DATASET CONFIG
# You can also use a simple Dict to define the dataset and pass it to your custom formatter.
dataset_config = BaseDatasetConfig(
    formatter="mdcc",
    dataset_name="mdcc",
    path="mdcc-dataset/",
    meta_file_train="cnt_asr_train_metadata.csv",
    meta_file_val="cnt_asr_valid_metadata.csv",
    language="yue-cn",
)

# INITIALIZE THE TRAINING CONFIGURATION
# Configure the model. Every config class inherits the BaseTTSConfig.
config = GlowTTSConfig(
    batch_size=32,
    eval_batch_size=16,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="yue-cn",
    characters=CharactersConfig(
        pad="_",
        eos="~",
        bos="^",
        characters="abcdefghijklmnopqrstuvwxyz123456",
        punctuations="!'(),-.:;? ！？｡。，、；：「」『』（）〔〕【】—…–～《》〈〉",
        phonemes="abcdefghijklmnopqrstuvwxyz123456"
    ),
    #use_eos_bos=True,
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    print_step=25,
    print_eval=True,
    mixed_precision=True,
    output_path=output_path,
    datasets=[dataset_config],
    test_sentences=field(
        default_factory=lambda: [
            "我挥一挥衣袖，不带走一片云彩。",
            "我不知道这些测试句子有什么用。",
        ]
    )
)

# INITIALIZE THE AUDIO PROCESSOR
# Audio processor is used for feature extraction and audio I/O.
# It mainly serves to the dataloader and the training loggers.
ap = AudioProcessor.init_from_config(config)

# INITIALIZE THE TOKENIZER
# Tokenizer is used to convert text to sequences of token IDs.
# If characters are not defined in the config, default characters are passed to the config
tokenizer, config = TTSTokenizer.init_from_config(config)

# LOAD DATA SAMPLES
# Each sample is a list of ```[text, audio_file_path, speaker_name]```
# You can define your custom sample loader returning the list of samples.
# Or define your custom formatter and pass it to the `load_tts_samples`.
# Check `TTS.tts.datasets.load_tts_samples` for more details.
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)
print(f"训练样本数: {len(train_samples)}")
print(f"验证样本数: {len(eval_samples)}")
print(f"示例: {train_samples[0]}")

# INITIALIZE THE MODEL
# Models take a config object and a speaker manager as input
# Config defines the details of the model like the number of layers, the size of the embedding, etc.
# Speaker manager is used by multi-speaker models.
model = GlowTTS(config, ap, tokenizer, speaker_manager=None)

# INITIALIZE THE TRAINER
# Trainer provides a generic API to train all the 🐸TTS models with all its perks like mixed-precision training,
# distributed training, etc.
trainer = Trainer(
    TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples
)

# AND... 3,2,1... 🚀
trainer.fit()
