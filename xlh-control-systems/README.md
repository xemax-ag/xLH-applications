# xLH Control Systems Library

`codesys/xlh_control_systems_00_10.library` is a CODESYS library (v0.10) of control-engineering basic elements written in Structured Text.

## Purpose

The library replicates the system behavior of the basic blocks used in the simulation software [WinFACT BORIS](https://www.kahlert.com/winfact-uebersicht/). This guarantees identical behavior in simulation and in the technological implementation on the PLC: a control loop designed and tuned in BORIS can be transferred 1:1 to the CODESYS application.

The underlying control-engineering theory (accompanying WinFACT BORIS) is covered in the book *"Crashkurs Regelungstechnik"* (Crash Course in Control Engineering), ISBN 978-3-8007-5837-1.

## Core concept: global cycle time

All dynamic function blocks are discretized with the explicit Euler method using a single global cycle time:

```
CS_COMMOM.fdt   // cycle time [s] of the calling task, default 0.004
```

Before using any dynamic block, set `CS_COMMOM.fdt` to the cycle time of the task in which the blocks are called. (The name `COMMOM` instead of `COMMON` is kept intentionally for backward compatibility.)

## Function blocks

### Dynamic elements (transfer functions)

| Block | Behavior |
|---|---|
| `P` | Proportional element, `G(s) = K` |
| `I` | Integrator, `G(s) = 1/(Ti*s)`; holds its output if `fTi <= 0` |
| `PT1` | First-order lag (low-pass), `G(s) = K/(1 + T*s)` |
| `PT2` | Second-order lag parameterized with two time constants `T1`, `T2` |
| `PT2s` | Second-order lag parameterized with damping and natural frequency (oscillatory for zeta < 1) |
| `PTt` | Dead-time element, `G(s) = K*e^(-Tt*s)`, shift register with up to 5000 samples |
| `DT1` | Derivative element with first-order lag (real differentiator), `G(s) = Tv*s/(1 + Tvz*s)` |
| `Controller` | Universal controller (P, I, PI, PDT1, PIDT1) with anti-windup and feed-forward input; type selected via `eControllerType`; anti-windup behavior matches WinFACT BORIS |

### Static / nonlinear elements

| Block | Behavior |
|---|---|
| `Limitation` | Output limiter (saturation) to `[fYmin, fYmax]` with limit-active flags |
| `Deadband` | Dead-zone element; output is 0 while the input magnitude is below the threshold |
| `CharacteristicCurve` | Piecewise linear lookup table with linear interpolation, optional inverse curve (mirror at X=Y) |

### Signal sources and test tools

| Block | Behavior |
|---|---|
| `SignalGenerator` | Test signal generator: off, constant, square, triangle, sine or ramp (`eSignalShape`), with optional added noise |
| `SignalNoise` | Pseudo-random noise generator (repeating sequence of 10000 pre-generated values, scalable amplitude) |
| `Logger_` | Data logger for step responses: up to 10 signals, 1000 samples each, with time axis and configurable downsampling |

### TOOLBOX

| Block | Behavior |
|---|---|
| `KalmanFilter` | Scalar (1-D) Kalman filter for smoothing noisy measurements, tuned via process/measurement noise covariances `fQ`/`fR` |
| `LrealToInt`, `LrealToUInt` | Rounding conversion helpers |

## Visualization

Most function blocks carry the `FBVisuCreator` attribute; the `CS_VISU_*` visualization objects (faceplates) are generated from them with the FBVisuCreator tool. Helper visualizations and text lists (`VISU_HELPER_Combobox_*`, `TextListForCombobox_*`) provide combo boxes for the `eSignalShape` and `eControllerType` enumerations.

## Naming conventions

All POU documentation is written in English. Some identifiers keep their original German or historically misspelled names on purpose (e.g. `CS_COMMOM`, `bAktiviert`, `bSpiegelungXgY`) — they must not be renamed, to preserve API and visualization compatibility with existing applications.
