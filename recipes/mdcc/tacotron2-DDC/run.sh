#!/bin/bash
# take the scripts's parent's directory to prefix all the output paths.
RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CORPUS=mdcc-dataset
echo $RUN_DIR
if [ \! -d $RUN_DIR/$CORPUS ] ; then
    echo "$RUN_DIR/$CORPUS doesn't exist."
    echo "Follow the instruction of https://github.com/HLTCHKUST/cantonese-asr to make the corpus."
    exit 1
fi

# create train-val splits
#shuf $RUN_DIR/$CORPUS/metadata.csv > $RUN_DIR/$CORPUS/metadata_shuf.csv
#head -n 8000 $RUN_DIR/$CORPUS/metadata_shuf.csv > $RUN_DIR/$CORPUS/metadata_train.csv
#tail -n 812 $RUN_DIR/$CORPUS/metadata_shuf.csv > $RUN_DIR/$CORPUS/metadata_val.csv

# compute dataset mean and variance for normalization
#python TTS/bin/compute_statistics.py $RUN_DIR/tacotron2-DDC.json $RUN_DIR/scale_stats.npy --data_path $RUN_DIR/$CORPUS/audio/

# training ....
# change the GPU id if needed
CUDA_VISIBLE_DEVICES="0" python TTS/bin/train_tts.py \
    --config_path $RUN_DIR/tacotron2-DDC.json \
    --restore_path $RUN_DIR/best_model.pth \
    --coqpit.output_path $RUN_DIR \
    --coqpit.datasets.0.path $RUN_DIR/$CORPUS \
    --coqpit.audio.stats_path $RUN_DIR/scale_stats.npy \
    --coqpit.phoneme_cache_path /tmp/phoneme_cache \