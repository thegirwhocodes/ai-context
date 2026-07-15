---
name: ""
metadata: 
  node_type: memory
  originSessionId: 3656ec2d-babd-4f3e-9b97-a7cb9f9d17be
---

When Naomi says "go through everything and make sure it works," she means **experience the flow the way a user would** — click through it, read each message in its real rendered position, look for UX inconsistencies — NOT just confirm the build is green and the right strings exist.

**Why:** On the sign-in cleanup (session 3656ec2d) I shipped an error message that said "Reset your password **below**" when the reset link was actually **above** it. Build passed, curl found the string, API returned 200 — so my checks were all green, but the copy was visibly wrong to a real user. Naomi caught it in 5 seconds; I should have. Curl + build-green verifies it *compiles and renders*, not that it *reads right or makes sense in context*.

**How to apply:** For any UI change, actually drive it (Browser pane / claude-in-chrome on the live/public site) — trigger the states (errors, empty fields, success), screenshot them, and READ the rendered result in position relative to the other elements. Hunt for copy that points the wrong way, controls that don't line up with their labels, dead ends. If the preview is walled ([[reference_vercel_preview_auth_wall]]) and the Browser pane is flaky, push through on production rather than falling back to curl-only. Don't call something verified until I've seen it behave.
