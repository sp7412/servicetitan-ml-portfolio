# ServiceTitan: Transformer & ViT Use Cases

## Confirmed Production Transformer Use

### NLP / Speech (Shipped)

**Second Chance Leads**
- Pipeline: ASR → transcript → missed booking classification
- ASR: almost certainly Whisper or Azure Cognitive Services Speech (transformer encoder-decoder)
- Classification: likely fine-tuned DistilBERT or similar on top of transcript

**Field Pro / Siro Integration**
- AI-powered pre-job briefs, guided troubleshooting, sales coaching
- Conversation scoring and coaching extraction = transformer-based speech + NLP pipeline
- Siro's core product is a fine-tuned speech + NLP transformer stack

**Contact Center Pro / Voice Agents**
- Real-time ASR + NLU for booking, routing, intent classification
- Full transformer stack end-to-end

**Atlas (Pantheon 2025)**
- GPT-4 via Azure OpenAI — transformer is the product
- Tool-calling agent for dispatch, reports, campaigns

**AP Automation (Jan 2025)**
- Automated invoice processing
- Architecture: LayoutLM / Donut — transformers that jointly attend over text and 2D layout/position

### Vision (Confirmed Production)

**Equipment Nameplate OCR — Field Mobile App (Pantheon 2025)**
- Tech points phone at HVAC unit → app extracts model number, serial, manufacture date
- Likely architecture: TrOCR (Microsoft transformer OCR) or Donut (image → structured JSON, no OCR preprocessing step)

---

## High-Confidence ViT Use Cases (Well-Motivated, Not Explicitly Confirmed)

### 1. Equipment Condition Assessment from Job Photos
- Techs photograph equipment on every job; ST has millions of images with matched service outcomes
- Problem: `image → {good, marginal, replace_soon}` → feeds upsell recommendation engine
- ViT preferred over ResNet: handles cluttered real-job-site backgrounds better
- Training signal: subsequent service history (replaced in <6mo = end-of-life label)

### 2. Rooftop / Aerial Imagery Analysis (Roofing Vertical)
- ST is aggressively expanding into roofing (Pantheon 2024 called out as "full-court press")
- Use cases: roof area measurement, hail/wind damage detection, material type classification
- Competitors EagleView and GAF QuickMeasure (GAF partnered with ST) already do this
- Architecture: ViT + segmentation head (SegFormer) for semantic segmentation of aerial imagery

### 3. Invoice / Document OCR at Scale (AP Automation)
- Supplier invoices, POs, receipts — often scanned PDFs or photos
- LayoutLMv3: attends over text tokens + 2D positions on page (purpose-built for this)
- Donut alternative: end-to-end, no OCR preprocessing, raw image → structured JSON
- Both available on HuggingFace and deployable on Azure ML

### 4. Fleet Pro: Risky Driver Detection from Dashcam Video
- Fleet Pro includes GPS + risky driver behavior detection (hard braking, phone use, following distance)
- Video transformer problem: TimeSformer, Video Swin Transformer, or MobileViT for on-device inference

### 5. Job Site Photo QA / Compliance
- "Did tech photograph before AND after?" / "Does photo show completed install vs WIP?"
- ViT binary classification; ST has scale of labeled job photos to fine-tune this
- Reduces QA overhead and enables automated job completion verification

---

## The Data Flywheel Argument (Interview-Critical)

ServiceTitan's moat is **not** the model architecture — it's the labeled dataset:
- Millions of jobs with matched photos, outcomes, and service histories
- A rusted heat exchanger labeled with "replaced 3 months later = $4K job" is not a signal a generic ImageNet model has
- Fine-tuned ViTs on this proprietary dataset are defensible; off-the-shelf models are not

**Infrastructure already in place:**
- TrOCR, Donut, LayoutLMv3 all on HuggingFace
- Azure ML handles ViT fine-tuning and endpoint deployment
- Azure Cognitive Services provides off-the-shelf OCR/Vision APIs as a baseline to beat

---

## Relevant Model Architectures Summary

| Task | Architecture | Notes |
|---|---|---|
| Speech → text | Whisper / Azure Speech | Encoder-decoder transformer |
| Text classification | DistilBERT / RoBERTa | Fine-tune on job transcript data |
| Document OCR | TrOCR / Donut | Nameplate, invoice extraction |
| Doc understanding | LayoutLMv3 | Attends over text + 2D layout |
| Image classification | ViT-B/16, DINOv2 | Equipment condition, photo QA |
| Aerial segmentation | SegFormer | Roofing damage/area |
| Video classification | TimeSformer / MobileViT | Fleet dashcam, on-device |
| Generative / agentic | GPT-4 via Azure OpenAI | Atlas |
