# TrajMem-OT

Gate-0 implementation of return-driven video trajectory-memory editing. The core keeps policy parameters, current observation, instruction, simulator state, and trajectory noise fixed; only history memory may change.

Implemented now:

- return-tilted empirical trajectory distribution;
- log-domain Sinkhorn OT and barycentric trajectory directions;
- matrix-free JVP/VJP normal operator with conjugate gradient;
- low-rank, temporal-sparse, trust-region memory update;
- paired `M`, `M+`, `M-`, norm-matched-random causal controls;
- two-GPU seed-parallel launcher.
- exact RoboMME branching through deterministic episode reconstruction;
- research-only MME-VLA controls for fixed flow noise and history-only edits;
- a real frozen-checkpoint low-rank memory-gradient integration probe.

Run the mathematical/unit smoke tests:

```bash
PYTHONPATH=src pytest -q
```

Run the paired video-memory Gate-0 proxy on both GPUs:

```bash
bash scripts/run_gate0_2gpu.sh
```

Official upstream sources are pinned under `third_party/`. Official RoboMME sample data and the released best perceptual-memory checkpoint are downloaded into `data/` and `checkpoints/` respectively.

Run the official checkpoint smoke test (two terminals):

```bash
cd third_party/robomme_policy_learning
CUDA_VISIBLE_DEVICES=0 XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 uv run scripts/serve_policy.py \
  --seed=7 --port=8010 policy:checkpoint \
  --policy.dir=/root/trajmem-ot/checkpoints/perceptual-framesamp-modul/79999 \
  --policy.config=mme_vla_suite

cd third_party/robomme_policy_learning
uv run /root/trajmem-ot/scripts/smoke_robomme_client.py \
  --data=/root/trajmem-ot/data/robomme_preprocessed_data_sample --port=8010
```

The upstream data unzip helper currently flattens the directory tree. Preserve
the required dataloader layout with:

```bash
cd data/robomme_preprocessed_data_sample
python3 -m zipfile -e data.zip .
python3 -m zipfile -e features.zip .
```
