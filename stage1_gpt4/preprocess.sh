#!/bin/bash

set -e
trap exit INT


####### generate the visaul tags (ram++)
for VIDPATH in ../data/AVHBench_v0/video/*.mp4
do
    VIDNAMEMP4=$(basename "$VIDPATH")
    VIDNAME="${VIDNAMEMP4%.*}"
    echo "$VIDNAME"

    if [ -e ../data/AVHBench_v0/frame/"$VIDNAME" ]; then
        echo "$VIDNAME Already processed."
        continue
    fi

    if [[ "$VIDNAME" == *swap* ]]; then
        echo "no gpt4 for swapped video"
        continue
    
    else
        mkdir -p "../data/AVHBench_v0/frame/$VIDNAME" 
        ffmpeg -i "$VIDPATH" -vf fps=0.8 "../data/AVHBench_v0/frame/$VIDNAME/%03d.png"
    fi

    cnt=$(( ${cnt}+1 ))
    if [ $cnt -ge 10 ]; then
        echo "ending loop at cnt 10."
        break
    fi
done

source ~/anaconda3/etc/profile.d/conda.sh
cd recognize-anything

conda activate recognize_anything
python inference_tag2text_halluci.py  --image ../../data/AVHBench_v0/frame --pretrained YOUR_RAM_CHECKPOINT_PATH/tag2text_swin_14m.pth  --output ../../stage1_gpt4/visual_tagging/tags.json
conda deactivate

########### generate the stage1 annotation
cd ../
conda activate avhbench
python3 disentangle_gpt4.py
conda deactivate