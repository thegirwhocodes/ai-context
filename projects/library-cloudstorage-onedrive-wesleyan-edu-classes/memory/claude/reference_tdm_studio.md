---
name: TDM Studio access
description: ProQuest TDM Studio Workbench is where Naomi runs WSJ text-mining notebooks for QAC 386. Browser-specific quirks and the working setup.
type: reference
originSessionId: ed1f260a-8aa3-446e-b16b-bc77f605156a
---
# TDM Studio (ProQuest Workbench)

- **URL**: tdmstudio.proquest.com
- **What it is**: Cloud Jupyter VM with licensed WSJ/NYT corpora. Data cannot leave the VM (15 MB/week export cap, no full text export, no API).
- **Naomi's project**: QAC 386 final — WSJ Nigeria risk analysis (`nigeria_risk_analysis_WSJ.ipynb`, `package_nigeria_outputs.ipynb`).

## Working browser
- **Use Atlas (OpenAI browser)** for TDM Studio. Chrome blocks clipboard paste into the Jupyter cells; Atlas works out of the box. Confirmed by Naomi 2026-04-30.
- Chrome fix (if ever needed): `chrome://settings/content/clipboard` → Add `https://tdmstudio.proquest.com` to Allowed.

## Workflow
- Edit `.ipynb` files locally in VS Code (faster than browser Jupyter), upload via TDM's My Files → Upload.
- Pull results out via the `package_nigeria_outputs.ipynb` zip-bundler, staying under 15 MB/week.
- No SSH, no remote kernel, no API — uploads/downloads through the browser are the only channel.
