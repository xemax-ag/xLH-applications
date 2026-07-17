# xLH Gantry — CODESYS Example Application

Example motion-control application for the **xLH gantry**: a 3-axis portal robot (X/Y/Z)
with an electromagnet gripper, a conveyor axis (C), a marble feeder and a marble run.
The application runs on **CODESYS Control for Raspberry Pi 64 SL** and uses CODESYS
SoftMotion (single-axis, axis-group/robotics and CNC interpolation).

Further information: <https://xlh.xemax.ch/applications/motion-control>

## Repository layout

| Path | Description |
|---|---|
| `codesys/xlh_gantry_example_1_00_91.project` | Complete example application (described in this README) |
| `codesys/xlh_gantry_start_00_91.project` | Reduced starting point for your own experiments |
| `codesys/_old/` | Archive of previous project versions |

## Hardware

- **Controller:** Raspberry Pi with CODESYS Control for Raspberry Pi 64 SL; 7 LEDs / 8 switches on the Pi GPIOs (`GPIOs_A_B` device).
- **Fieldbus:** CANopen at 1 Mbit/s with two custom nodes:
  - **`xlh_motion` (node 1)** — motion board: 4 stepper axes (encoder position feedback in; per-axis control byte and step frequency out), digital inputs (limit switches, inductive sensors), electromagnet PWM output, 8 RC-servo channels.
  - **`xlh_terminal` (node 2)** — operator terminal: 24 keys with RGB backlight, 3 rotary encoders (C / XY / Z), master velocity potentiometer, brightness control.

### Axes

All four axes are `SM_Drive_PosControl` drives in the SoftMotion General Axis Pool.
X, Y and Z form the SoftMotion **AxisGroup** (gantry kinematics, linear interpolated
moves); C (conveyor) is driven as a single axis.

| Axis | Drive ID | Scaling | Homing |
|---|---|---|---|
| `x_axis` | 0 | ≈ 814.77 pulses/mm (25600 pulses/rev, drive Ø ≈ 10.0 mm) | Limit switch (fast/slow seek), offset −5.0 mm |
| `y_axis` | 1 | ≈ 814.77 pulses/mm, direction inverted | Limit switch, offset −5.0 mm |
| `z_axis` | 2 | ≈ 814.77 pulses/mm, direction inverted | Limit switch, offset −5.0 mm |
| `c_axis` | 3 | 530 pulses/unit (gear 3:1), direction inverted | Without limit switch (setpoint reset to 0) |

Default motion profile (set in `MC`): velocity 30, acceleration/deceleration 20, jerk 100;
homing velocity 2.0 (fast seek = 3×).

### Signal list (xLH motion board)

| Connector | Function |
|---|---|
| J3 / J4 / J7 | Stepper axis X / Y / Z |
| J11 / J12 / J13 | Limit switch axis X / Y / Z |
| J14 | Inductive sensor sphere |
| J19 / J20 | Inductive sensor marble run start / end |
| J27 | Electromagnet (PWM) |
| J21+J25 / J22+J26 | RC servo 1 / 2 |
| J28+J32 | RC servo 3 → marble run |
| J29+J33 | RC servo 4 → marble feeder |
| J30+J34 / J31+J35 | RC servo 5 / 6 |
| — | Axis C, limit switch C, conveyor sensors (reserved) |

## Software structure

### Tasks

| Task | Content |
|---|---|
| `MAIN_TASK` | `io` (I/O image) and `MAIN_CALLER` (application entry point) |
| `CANOPEN_TASK` | CANopen stack |
| `VISU_TASK` | Web visualization (`VisuElems.Visu_Prg`) |
| `SoftMotion_PlanningTask` | Path planning for the axis group |

### Program flow

1. **`MAIN_CALLER`** waits (250 ms debounce) until both CANopen nodes report
   `OPERATIONAL`, then calls the main state machine `MC` cyclically.
2. **`MC`** (main state machine):
   - **Startup/Homing:** power up all four axes, disable the axis group, home Z and C
     first, then X and Y (see the `homing` action), re-enable the axis group.
   - **Wait for command:** dispatches to one of the operating modes below; the *Home*
     key restarts homing at any time.
   - The actions of `MC` bundle recurring work: `axInitPointers` (wire FBs and axis
     references at startup), `axCmdReset`, `axSmExecuteToFalse` / `axGexecuteToFalse`
     (clear PLCopen execute flags), `read_io` / `write_io` (I/O image and RGB key
     feedback).

### Operating modes

| Mode (program) | Trigger | Description |
|---|---|---|
| `MANUAL_MODE` | *Manual* key | Jog mode: axis keys move the XYZ group relatively; C and Y can be jogged as single axes (F2/F3 for Y). Step sizes are adjusted with the three terminal encoders. Keys 1/2 run a manual pick-and-place between marble feeder and marble run; keys 5/6 toggle the feeder/run servos; the *Magnet* key toggles the electromagnet. |
| `APP_SQUARE_MODE` | *F1* key | Automatic pick-and-place demo: 5 square steps (`PNP_STEPS`) executed at each grid offset (`PNP_GRID`) around a reference position, driven by `FB_AXG_PICK_AND_PLACE`. |
| `CNC_MODE` | *F2* key | CNC demo: moves XYZ to a reference point, then runs the G-code from `GCODE/DEMO_GCODE` through the SoftMotion chain `SMC_CheckVelocities` → `SMC_Interpolator` → `SMC_ControlAxisByPos` (interpolation cycle 4000 µs). The path is offset so it starts at the current actual position; the master velocity potentiometer acts as feed override. |

### POU reference

**`MOTION_BASE`** — motion abstraction layer:

| POU | Purpose |
|---|---|
| `FB_PLC_OPEN_AXIS` | Bundles the PLCopen blocks (MC_Power, MC_Stop, MC_MoveAbsolute/Relative/Velocity, MC_Reset, status/error blocks) for one axis with shared velocity/acceleration/jerk defaults. |
| `FB_XLH_MOTION_AXIS_BASE` | Hardware interface between a stepper axis and SoftMotion: feeds the encoder position into `AXIS_REF_POSCONTROL` (`mRead`), derives direction/enable/in-motion and pulse frequency from the setpoint velocity (`mWrite`). |
| `FB_XLH_MOTION_AXIS_SIMPLE` | Homing without a limit switch (used for the C axis): move the setpoint to 0 without emitting pulses. |
| `FB_XLH_MOTION_AXIS_SIMPLE_ES` | Homing with a limit switch (X/Y/Z): fast seek → retreat → slow seek → offset move → zero the setpoint. |
| `FB_AXG_MOVE_ABSOLUTE` / `FB_AXG_MOVE_RELATIVE` | Wrappers around `MC_MoveLinearAbsolute`/`MC_MoveLinearRelative` with fixed blending defaults (BlendingHigh, corner distance 50, MCS). |
| `FB_AXG_PICK_AND_PLACE` | Pick-and-place sequencer (hover → down → magnet on → lift → move → down → magnet off → lift). |
| `FB_AXG_PICK_AND_PLACE_MANUAL` | Variant with decomposed XY/Z/Y/X moves to avoid obstacles between feeder and marble run. |
| `FB_KALMAN_FILTER` | One-dimensional Kalman filter; smooths the step-frequency output per axis. |
| `ST_PnpStep` | Pick/place coordinate pair for the square demo. |

**`IO`** — hardware image:

| POU | Purpose |
|---|---|
| `io` (PRG) | I/O image and wiring: instantiates `gpio`, `terminal` and `motion`, links the four axis FBs to the PLCopen wrappers and the SoftMotion axes, drives magnet and marble feeder/run servos. Contains the signal list of the board. |
| `FB_XLH_MOTION` | PDO image of the motion board: packs the per-axis control byte (enable, direction, reset, inverted, in-motion, move-without-pulse), converts the SoftMotion step period into a frequency in Hz and smooths it with a Kalman filter. |
| `FB_XLH_TERMINAL` | Terminal interface: unpacks key bytes into BOOLs with rising-edge flags, scales the velocity potentiometer to 0..1, packs the RGB LED states. |
| `FB_XLH_GPIO` | Data container for the Pi GPIO LEDs/switches. |
| `RGB`, `MOTION_CONTROL_BYTE`, `UNION_BYTE_INT` | Helper types (RGB enum, control-byte layout, byte/int union). |

**Other objects:** `GCODE/DEMO_GCODE` (CNC G-code object for the demo path),
`CNC settings`, `MISC/TRACE` (traces for axis X/Z), `Visualization` + `WebVisu`,
`AxisGroup` (XYZ gantry kinematics).

### Key libraries

SM3_Basic, SM3_CNC, SM3_Robotics (+ Transformation/Visu), SM3_Drive_PosControl,
SM3_CamBuilder, 3S CANopenStack, CAA CiA 405, IoDrvGPIO and the CODESYS
visualization libraries.

## Terminal quick reference

| Control | Function |
|---|---|
| **Home** | Start/repeat homing (RGB red while not homed) |
| **Manual** | Enter jog mode (green = waiting, blue = moving) |
| **X± / Y± / Z± / C±** | Jog keys (manual mode) |
| **Encoders C / XY / Z** | Jog step size |
| **F1** | Start square pick-and-place demo (blue while running) |
| **F2** | Start CNC demo; in manual mode: jog Y+ (F3: Y−) |
| **Velocity potentiometer** | Override 0..1 (red ≤ 0.1, green, blue > 0.9) |
| **Magnet** | Toggle electromagnet |
| **Keys 1 / 2** | Manual pick-and-place: feeder → marble run / marble run → feeder |
| **Keys 5 / 6** | Toggle marble feeder / marble run servo |
| **Reset** | Leave manual mode |
