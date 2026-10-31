# Robot camera

A robot camera is an ISP camera plus three extra requirements:

1. **Geometry.** Intrinsics and distortion so pixels become rays.
2. **Time.** Frame age must be known. A pretty late frame is a bad observation.
3. **Motion.** Long exposure kills blur-sensitive tasks. AE and denoise fight each other.

That is why `calib`, `undistort`, `motion_ae`, and `latency` sit next to 3A instead of inside it.

## Expand later

- [ ] Extrinsics (camera to base / gripper)
- [ ] Rolling shutter
- [ ] Multi-camera sync
