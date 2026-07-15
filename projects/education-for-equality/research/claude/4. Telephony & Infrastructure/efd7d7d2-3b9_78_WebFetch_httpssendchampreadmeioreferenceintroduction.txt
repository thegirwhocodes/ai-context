========================================================================
WEBFETCH RESEARCH: WebFetch: https://sendchamp.readme.io/reference/introduction
Session: efd7d7d2-3b94-4e82-bb2d-7a045a3e9736
Time: 2026-03-11 06:30:12 UTC
========================================================================

URL: https://sendchamp.readme.io/reference/introduction
Extraction prompt: What APIs does Sendchamp offer? List all endpoints, especially voice-related ones. Does it support: IVR, custom audio playback, recording, webhooks, programmable voice calls, inbound calls, outbound calls? What is the full API capability?

----------------------------------------

# Sendchamp API Capabilities

## Core Messaging APIs Offered

Sendchamp provides RESTful APIs for multiple communication channels:

- **SMS** - Send and receive text messages
- **Email** - Send email messages
- **Voice** - Text-to-speech and audio playback
- **WhatsApp** - Template messages and two-way messaging
- **Facebook Messenger, Twitter, Instagram** - Additional channels mentioned

## Voice API Endpoints

The platform supports these voice-related capabilities:

**Outbound Voice:**
- Text-to-Speech: Convert text messages to voice calls
- Audio playback: Send pre-recorded audio files to recipients
- Message repetition control

**Inbound/Call Management:**
- Create voice calls
- List voice calls
- Retrieve single call details
- Receive/handle incoming calls

**Voice Delivery:**
- Voice delivery reports and status tracking

## Advanced Voice Features (XML/IVR)

Sendchamp supports programmable voice through XML verbs:

- `<Say>` - Text-to-speech output
- `<Play>` - Audio file playback
- `<Dial>` - Route calls to numbers
- `<Record>` - Capture caller audio
- `<Gather>` - Collect DTMF input from callers
- `<Pause>`, `<Redirect>`, `<Enqueue>` - Call flow control
- `<Reject>` - Decline calls

**Child Actions:**
- `<Number>`, `<Queue>`, `<SIP>` for advanced routing

## Additional Features

- **OTP/Verification** - Send and confirm one-time passwords across channels
- **Webhooks** - Event notifications supported
- **Number Insight API** - Phone number validation and insights
- **Wallet/Reports** - Balance checks and delivery reporting

========================================================================
END OF WEBFETCH RESEARCH
========================================================================