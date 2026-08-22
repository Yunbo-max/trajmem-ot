# Gate-0 status

## E7 — real-memory local geometry (running, 2026-08-22)

- Backbone: frozen pi0.5 / MME-VLA `perceptual-framesamp-modul`, rank 16.
- Protocol: 64 real demonstration states (16 per selected RoboMME task), fixed current observation, instruction, robot state, and flow noise.
- Sweep: relative memory radii 0, 0.003125%, 0.00625%, 0.0125%, 0.025%, 0.05%, 0.1%, both signs, plus 64 norm-matched random controls per nonzero radius.
- Hardware: two RTX 3090 GPUs, two deterministic policy servers, sharded 32 states each.
- Scope: these are official preprocessed training-demonstration states because the quick dataset supplies action targets but not val demonstrations. E8 will use simulator branches and environment outcomes; train geometry is not reported as val performance.
- Pilot found numerical instability for states whose demonstration action MSE is already near zero. The full analysis will report aggregate paired probabilities and strata by baseline MSE.

- Hardware: 2x RTX 3090 24GB.
- Core unit tests: 4 passed.
- Synthetic paired video-memory test (8 seeds, 8 particles):
  - original return: -0.553794
  - positive memory edit: -0.551756
  - negative direction: -0.555864
  - norm-matched random: -0.553955
  - per-particle improvement rate: 96.875%
  - mean critical-event rank: 3 (not yet strong enough for an attribution claim)
- Official RoboMME sample dataloader: passed, 27,452 samples.
- Released perceptual-framesamp-modul checkpoint: restored on one RTX 3090.
- Official checkpoint inference: passed, finite action chunk with shape [20, 8].
- First-call compile timings: memory buffer 11.76s; policy inference 40.07s.
- RoboMME simulator: installed and verified on Mesa llvmpipe; one official
  PickXtimes test episode completed and video was written.
- Deterministic branch restore: exact replay produced bit-identical RGB, joint
  state and reward after a shared five-action prefix.
- Real MME-VLA edit interface: fixed flow-noise repeats and delta clearing are
  bit-exact; a history-only edit changes the action chunk.
- Real frozen-model rank-16 oracle probe at 0.025% trust radius:
  - Q(original): -0.006280535
  - Q(positive): -0.006268218
  - Q(negative): -0.006273085
  - positive beat 8/8 norm-matched random controls.
- End-to-end memory -> action -> simulator branching: passed. All four branches
  had the same start fingerprint and distinct final fingerprints.
- Important limitation: RoboMME short-horizon dense rewards are zero; the
  20-step real branches remained ongoing. Environment-return improvement is
  therefore not established yet.

These results validate plumbing, the local causal optimizer, exact simulator
branching, and frozen-checkpoint memory steering. They are not RoboMME task
success-rate results; terminal rollouts or an action-sensitive learned critic
remain necessary for return-conditioned optimization.
