# AVHBench-Align-FT

This directory contains the training code for the feature alignment and LoRA fine-tuning stages used in AVHBench.

This code implements the alignment and fine-tuning stages described in the AVHBench paper.

## Training

### Stage 2: Feature Alignment

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --nproc_per_node=4 train.py \
  --cfg-path train_configs/multimodal_llama_stage2_pretrain_audiodata.yaml
```

### Stage 3: LoRA Fine-tuning

```bash
torchrun --nproc_per_node=4 train.py \
  --cfg-path train_configs/multimodal_llama_stage3_finetune_audiodata_lora.yaml
```