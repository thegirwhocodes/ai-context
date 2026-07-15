# Sabi Multilingual Audio Plan

- Multilingual audio should be built as a separate Sabi Language Lab lane, not a production prompt flip: separate Asterisk context, proposed AudioSocket `9030`, offline replay, adult native-speaker canary, then child canary only after eval gates. - 019f3565-3bd6-7d60-a103-cb8aa02c6da6 / 019f3520-7af6-7101-b1ff-2499b2f10931
- Production remains Nigerian-English first and mother-tongue aware; Yoruba/Igbo/Hausa responses require language ID, STT, canonical English translation, original+translated safety checks, deterministic grading, and native-language TTS evals. - 019f3565-3bd6-7d60-a103-cb8aa02c6da6 / 019f3520-7af6-7101-b1ff-2499b2f10931
- Canonical product spelling is `Igbo`; accept `Ibo` only as an alias. - 019f3565-3bd6-7d60-a103-cb8aa02c6da6 / 019f3520-7af6-7101-b1ff-2499b2f10931
- First provider bake-off: Intron, Soniox, and Google STT V2 for STT; Google/Azure/OpenAI/open models for translation; YarnGPT/ElevenLabs/Azure `en-NG`/OpenAI/local for TTS, with native-speaker eval required before child-facing use. - 019f3565-3bd6-7d60-a103-cb8aa02c6da6 / 019f3520-7af6-7101-b1ff-2499b2f10931
- Do not store child raw audio by default; any child language eval/training corpus must use the existing separate guardian training consent path. - 019f3565-3bd6-7d60-a103-cb8aa02c6da6 / 019f3520-7af6-7101-b1ff-2499b2f10931
