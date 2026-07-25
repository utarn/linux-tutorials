# คู่มือโมเดล LLM/VLM สำหรับ OCR และเปรียบเทียบ Benchmark

เอกสารสรุปโมเดลภาษาขนาดใหญ่ (LLM) และโมเดลเข้าใจภาพ-ภาษา (Vision-Language Model, VLM) ที่ใช้สำหรับ **OCR** (Optical Character Recognition — การสกัดข้อความจากภาพ/เอกสาร) พร้อมตัวเลข Benchmark อ้างอิงจากหน้าโมเดลอย่างเป็นทางการบน Hugging Face, เว็บไซต์ Google DeepMind และ Qwen Blog

> หมายเหตุ: ตัวเลข Benchmark มาจากการดึงข้อมูลด้วย `curl` จาก Hugging Face API (`huggingface.co/api/models` และไฟล์ `README.md` ดิบ) และการอ่านหน้าเว็บของ Google DeepMind/Qwen ณ วันที่ 24 กรกฎาคม 2026 ค่าต่าง ๆ อาจมีการอัปเดตโดยผู้พัฒนาโมเดล

---

## สารบัญ

1. [ภาพรวม Benchmark ที่เกี่ยวกับ OCR](#1-ภาพรวม-benchmark-ที่เกี่ยวกับ-ocr)
2. [รายชื่อโมเดลสำหรับ OCR](#2-รายชื่อโมเดลสำหรับ-ocr)
3. [ตารางเปรียบเทียบ Benchmark OCR](#3-ตารางเปรียบเทียบ-benchmark-ocr)
4. [รายละเอียดรายโมเดล](#4-รายละเอียดรายโมเดล)
5. [คำแนะนำการเลือกใช้งาน](#5-คำแนะนำการเลือกใช้งาน)
6. [แหล่งข้อมูล (Sources)](#6-แหล่งข้อมูล-sources)

---

## 1. ภาพรวม Benchmark ที่เกี่ยวกับ OCR

| Benchmark | วัดอะไร | ช่วงคะแนน |
|---|---|---|
| **OCRBench** | ความสามารถ OCR รวม (ข้อความในภาพ ป้าย ใบเสร็จ ฯลฯ) | 0–1000 (คลาสสิก) หรือ 0–100 (เวอร์ชันใหม่/ปรับสเกล) |
| **OCRBench v2** | เวอร์ชัน 2 มี Format/Reasoning/Content Recognition แยก | รายงานเป็นคู่ `format/content` เช่น 61.5/63.7 |
| **CC-OCR** | OCR หลายภาษา/หลายสภาพแวดล้อม ของ Qwen | 0–100 |
| **OmniDocBench1.5** | OCR/เข้าใจเอกสารหลายรูปแบบ (PDF, สไลด์, ตำรา ฯลฯ) | 0–100 |
| **MMLongBench-Doc** | เข้าใจเอกสารยาวหลายหน้า (long-document) | 0–100 |
| **DocVQA** | ถาม-ตอบจากเอกสาร (Document Visual Question Answering) | 0–100 (สูง = ดี) |
| **InfoVQA** | ถาม-ตอบจากเอกสารที่มีข้อมูลหนาแน่น (infographics) | 0–100 |
| **ChartQA** | ทำความเข้าใจและถาม-ตอบจากแผนภูมิ | 0–100 |
| **AI2D** | ทำความเข้าใจไดอะแกรมวิทยาศาสตร์ | 0–100 |
| **TextVQA** | ถาม-ตอบโดยใช้ข้อความในภาพ | 0–100 |
| **CharXiv** | สกัด/เข้าใจข้อมูลจากแผนภูมิซับซ้อน | 0–100 |
| **MMMU** | ความเข้าใจมัลติโมดอลระดับวิทยาลัย (ภาพรวม ไม่ใช่ OCR โดยตรง) | 0–100 |

> ระวัง: **OCRBench มี 2 สเกล** — สเกลเดิม (0–1000, เช่น Qwen2.5-VL-7B = 864) และสเกลใหม่/ปรับใหม่ (0–100, เช่น Qwen3.6-27B = 89.4) ห้ามนำมาเปรียบเทียบข้ามสเกลโดยตรง

---

## 2. รายชื่อโมเดลสำหรับ OCR

### ตระกูล Gemini (Google) — ปัจจุบันใช้รุ่น 3.x
- **Gemini 3.6 Flash** — โมเดลหลักเสถียรรุ่นปัจจุบัน, รองรับ text/image/video/audio/PDF, context 1M tokens, output 64k
- **Gemini 3.5 Flash-Lite** — รุ่นประหยัด/ต่ำ latency, เหมาะกับงาน OCR ปริมาณมาก เช่น ใบเสร็จ, สกัดข้อมูลง่าย ๆ

### ตระกูล Qwen (Alibaba) — รุ่นล่าสุด Qwen3.6 (เป็น VLM อยู่แล้ว ไม่มี `-VL` ต่อท้าย)
- **Qwen3.6-27B** — Dense model, 27B params, pipeline `image-text-to-text` (มี Vision Encoder)
- **Qwen3.6-35B-A3B** — MoE, 35B params รวม / 3B active, pipeline `image-text-to-text`
- รุ่นก่อนหน้า (VLM เช่นกัน ไม่มี `-VL` ต่อท้าย): **Qwen3.5-9B / 27B / 35B-A3B / 397B-A17B** (และรุ่นอื่น ๆ ในตระกูล เช่น 4B, 122B-A10B)
- รุ่นเก่ากว่า (ใช้ชื่อ `-VL` ชัดเจน): **Qwen3-VL-4B / 8B / 30B-A3B / 32B**, **Qwen2.5-VL-3B / 7B / 32B / 72B**

### ตระกูล Typhoon OCR (SCB 10X / OpenTyphoon) — เน้นเอกสารไทย-อังกฤษ
- **typhoon-ai/typhoon-ocr-7b** — fine-tune จาก Qwen2.5-VL-7B-Instruct, ภาษา ไทย/อังกฤษ, สัญญาอนุญาต Apache-2.0, downloads ~64k, likes 80
- **typhoon-ai/typhoon-ocr-3b** — fine-tune จาก Qwen2.5-VL-3B-Instruct, downloads ~390k
- **typhoon-ai/typhoon-ocr1.5-3b-qat** — เวอร์ชัน QAT (Quantization-Aware Training), ปี 2025

---

## 3. ตารางเปรียบเทียบ Benchmark OCR

### 3.1 Qwen3.6 (รุ่นปัจจุบัน) — จาก HF model card ทางการ

คอลัมน์เรียงตามการ์ด: `Qwen3.5-27B | Qwen3.5-397B-A17B | Gemma4-31B | Claude 4.5 Opus | Qwen3.6-35B-A3B | Qwen3.6-27B`

| Benchmark | Qwen3.5-27B | Qwen3.5-397B-A17B | Gemma4-31B | Claude 4.5 Opus | **Qwen3.6-35B-A3B** | **Qwen3.6-27B** |
|---|---|---|---|---|---|---|
| MMMU | 82.3 | 85.0 | 80.4 | 80.7 | 81.7 | **82.9** |
| MMMU-Pro | 75.0 | 79.0 | 76.9 | 70.6 | 75.3 | 75.8 |
| RealWorldQA | 83.7 | 83.9 | 72.3 | 77.0 | 85.3 | 84.1 |
| **CC-OCR** | 81.0 | 82.0 | 75.7 | 76.9 | **81.9** | 81.2 |
| **OCRBench** | 89.4 | — | 86.1 | — | **90.0** | 89.4 |
| CharXiv RQ | 79.5 | 80.8 | 67.9 | 68.5 | 78.0 | 78.4 |

> OCRBench ของ Qwen3.6 อยู่ในสเกล 0–100 (ค่าสูง = ดี)

### 3.2 Qwen3.5 (รุ่นก่อน Qwen3.6 — VLM ทุกขนาด ไม่มี `-VL` ต่อท้าย)

Qwen3.5 รายงาน Benchmark เกี่ยวกับ OCR/เอกสารได้ละเอียดกว่า Qwen3.6 มีทั้ง **OCRBench, OmniDocBench1.5, MMLongBench-Doc, CharXiv, CC-OCR, AI2D** ครบ

**3.2.1 Qwen3.5-9B** — คอลัมน์: `GPT-5-Nano | Gemini-2.5-Flash-Lite | Qwen3-VL-30B-A3B | Qwen3.5-9B | Qwen3.5-4B`

| Benchmark | GPT-5-Nano | Gemini-2.5-Flash-Lite | Qwen3-VL-30B-A3B | **Qwen3.5-9B** | Qwen3.5-4B |
|---|---|---|---|---|---|
| OmniDocBench1.5 | 55.9 | 79.4 | 86.8 | **86.2** | 87.7 |
| CharXiv (RQ) | 50.1 | 56.1 | 56.6 | **70.8** | 73.0 |
| MMLongBench-Doc | 31.8 | 46.5 | 47.4 | **54.2** | 57.7 |
| CC-OCR | 58.9 | 72.9 | 77.8 | **76.7** | 79.3 |
| AI2D_TEST | 81.9 | 85.7 | 86.9 | **89.6** | 90.2 |
| **OCRBench** (0–100) | 75.3 | 82.5 | 83.9 | **85.0** | 89.2 |
| VlmsAreBlind | 66.7 | 68.4 | 72.5 | **92.6** | 93.7 |

**3.2.2 Qwen3.5-27B / 35B-A3B** — คอลัมน์: `GPT-5-mini | Claude-Sonnet-4.5 | Qwen3-VL-235B-A22B | Qwen3.5-122B-A10B | Qwen3.5-27B | Qwen3.5-35B-A3B`

| Benchmark | GPT-5-mini | Claude-Sonnet-4.5 | Qwen3-VL-235B-A22B | Qwen3.5-122B-A10B | **Qwen3.5-27B** | **Qwen3.5-35B-A3B** |
|---|---|---|---|---|---|---|
| OmniDocBench1.5 | 77.0 | 85.8 | 84.5 | 89.8 | 88.9 | **89.3** |
| CharXiv (RQ) | 68.6 | 67.2 | 66.1 | 77.2 | **79.5** | 77.5 |
| MMLongBench-Doc | 50.3 | — | 56.2 | 59.0 | **60.2** | 59.5 |
| CC-OCR | 70.8 | 68.1 | 81.5 | 81.8 | **81.0** | 80.7 |
| AI2D_TEST | 88.2 | 87.0 | 89.2 | 93.3 | **92.9** | 92.6 |
| **OCRBench** (0–100) | 82.1 | 76.6 | 87.5 | 92.1 | 89.4 | **91.0** |

**3.2.3 Qwen3.5-397B-A17B** (MoE ใหญ่สุด) — คอลัมน์: `GPT-5.2 | Claude 4.5 Opus | Gemini-3 Pro | Qwen3-VL-235B-A22B | K2.5-1T-A32B | Qwen3.5-397B-A17B`

| Benchmark | GPT-5.2 | Claude 4.5 Opus | Gemini-3 Pro | Qwen3-VL-235B-A22B | K2.5-1T-A32B | **Qwen3.5-397B-A17B** |
|---|---|---|---|---|---|---|
| OmniDocBench1.5 | 85.7 | 87.7 | 88.5 | 84.5 | 88.8 | **90.8** |
| CharXiv (RQ) | 82.1 | 68.5 | 81.4 | 66.1 | 77.5 | **80.8** |
| MMLongBench-Doc | — | 61.9 | 60.5 | 56.2 | 58.5 | **61.5** |
| CC-OCR | 70.3 | 76.9 | 79.0 | 81.5 | 79.7 | **82.0** |
| AI2D_TEST | 92.2 | 87.7 | 94.1 | 89.2 | 90.8 | **93.9** |
| **OCRBench** (0–100) | 80.7 | 85.8 | 90.4 | 87.5 | 92.3 | **93.1** |

> สรุปแนวโน้มขนาดพารามิเตอร์ Qwen3.5: ยิ่งขนาดใหญ่ คะแนน OCR/เอกสารยิ่งสูงขึ้น — **OCRBenck** 9B=85.0 → 27B=89.4 → 35B-A3B=91.0 → 397B-A17B=93.1; **OmniDocBench1.5** 9B=86.2 → 397B-A17B=90.8; **CC-OCR** 9B=76.7 → 397B-A17B=82.0

### 3.3 Qwen3.6-35B-A3B เปรียบเทียบกับรุ่นอ้างอิงอื่น

คอลัมน์: `Qwen3.5-27B | Claude-Sonnet-4.5 | Gemma4-31B | Gemma4-26BA4B | Qwen3.5-35B-A3B | Qwen3.6-35B-A3B`

| Benchmark | Qwen3.5-27B | Claude-Sonnet-4.5 | Gemma4-31B | Gemma4-26BA4B | Qwen3.5-35B-A3B | **Qwen3.6-35B-A3B** |
|---|---|---|---|---|---|---|
| MMMU | 82.3 | 79.6 | 80.4 | 78.4 | 81.4 | **81.7** |
| MMMU-Pro | 75.0 | 68.4 | 76.9* | 73.8* | 75.1 | 75.3 |
| RealWorldQA | 83.7 | 70.3 | 72.3 | 72.2 | 84.1 | **85.3** |
| **CC-OCR** | 81.0 | 68.1 | 75.7 | 74.5 | 80.7 | **81.9** |
| **AI2D_TEST** | 92.9 | 87.0 | 89.0 | 88.3 | 92.6 | **92.7** |

### 3.4 Qwen2.5-VL (รุ่นก่อนหน้า) — สเกล OCRBench 0–1000

จาก HF README ของ Qwen2.5-VL-32B-Instruct (เปรียบเทียบภายในตระกูล)

| Benchmark | Qwen2-VL-72B | Qwen2.5-VL-32B | Qwen2.5-VL-72B |
|---|---|---|---|
| OCRBench v2 (format/content) | 47.8/46.1 | 57.2/59.1 | **61.5/63.7** |
| CC-OCR | 68.7 | 77.1 | **79.8** |
| DocVQA | 96.5 | 94.8 | **96.4** |
| InfoVQA | 84.5 | 83.4 | **87.3** |

จาก HF README ของ Qwen2.5-VL-7B-Instruct (สเกล OCRBench 0–1000)

| Benchmark | InternVL2.5-8B | MiniCPM-o 2.6 | GPT-4o-mini | Qwen2-VL-7B | **Qwen2.5-VL-7B** |
|---|---|---|---|---|---|
| DocVQA (test) | 93 | 93 | — | 94.5 | **95.7** |
| InfoVQA (test) | 77.6 | — | — | 76.5 | **82.6** |
| ChartQA (test) | 84.8 | — | — | 83.0 | **87.3** |
| TextVQA (val) | 79.1 | 80.1 | — | 84.3 | **84.9** |
| **OCRBench** (0–1000) | 822 | 852 | 785 | 845 | **864** |
| CC-OCR | 57.7 | — | — | 61.6 | **77.8** |

> ขนาดพารามิเตอร์ของตระกูล Qwen2.5-VL: **3B / 7B / 32B / 72B** — ยิ่งขนาดใหญ่ คะแนน OCR/DocVQA ยิ่งสูงขึ้นตามลำดับ

### 3.5 Gemini 3.6 Flash & 3.5 Flash-Lite — จากหน้า Performance ของ DeepMind

Gemini รุ่น 3.x รายงาน Benchmark ภาพในรูปแบบเฉพาะ เช่น CharXiv (สกัดข้อมูลจากแผนภูมิซับซ้อน) และ OSWorld-Verified (Agent ควบคุมคอมพิวเตอร์) แทน DocVQA/OCRBench แบบดั้งเดิม

**Gemini 3.6 Flash**

| Benchmark | Gemini 3.6 Flash | Gemini 3.5 Flash | Gemini 3.1 Pro | GPT-5.6 Luna | Grok 4.5 | Claude Sonnet 5 |
|---|---|---|---|---|---|---|
| CharXiv (No tools) | **85.2** | 84.2 | 83.3 | 82.7 | 81.6 | 77.0 |
| CharXiv (With tools) | **89.4** | 84.9 | 83.2 | — | — | 88.3 |
| OSWorld-Verified | **83.0** | 78.4 | 76.2 | 72.6 | — | 81.2 |

**Gemini 3.5 Flash-Lite** (รุ่นประหยัด)

| Benchmark | Gemini 3.5 Flash-Lite | Gemini 3.1 Flash-Lite | GPT-5.4 mini | Claude Haiku 4.5 |
|---|---|---|---|---|
| CharXiv (No tools) | 74.5 | 73.2 | **80.3** | 61.7 |
| CharXiv (With tools) | **76.5** | 75.6 | — | — |
| OSWorld-Verified | **74.0** | 54.3 | 72.1 | 50.7 |

### 3.6 Typhoon OCR — เอกสารไทย

Typhoon-OCR-7B รายงานผลเป็นภาพกราฟิกใน 3 โดเมน: **finance / government / book** (ค่าตัวเลขดิบใน README เป็นรูปภาพ จึงไม่สามารถสกัดเป็นตัวเลขได้) แต่มีข้อความสรุปชัดเจน:

> *"Typhoon OCR outperforms both **GPT-4o** and **Gemini 2.5 Flash** in Thai document understanding, particularly on documents with complex layouts and mixed-language content."*

ข้อจำกัด: ในโดเมน Thai books ประสิทธิภาพลดลงเล็กน้อยเพราะมีรูปภาพฝังมากและหลากหลาย ซึ่งเป็นจุดที่ทีมงานระบุว่าควรปรับปรุงต่อไป

---

## 4. รายละเอียดรายโมเดล

### 4.1 Qwen3.6-27B (Dense)
- **ประเภท:** Causal Language Model with Vision Encoder (เป็น VLM โดยสมบูรณ์ ไม่มี `-VL` ต่อท้ายชื่อ)
- **พารามิเตอร์:** 27B (Dense)
- **Context:** สูงสุด 262,144 tokens
- **โหมด:** Thinking mode โดย default (มี `<think>...</think>` ก่อนคำตอบ)
- **การใช้งาน:** รองรับผ่าน vLLM (`vllm>=0.19.0`), SGLang, และ transformers ใหม่ล่าสุด
- **OCRBench:** 89.4 | **CC-OCR:** 81.2 | **MMMU:** 82.9
- Hugging Face: `Qwen/Qwen3.6-27B`

### 4.2 Qwen3.6-35B-A3B (MoE)
- **ประเภท:** Causal Language Model with Vision Encoder (VLM)
- **พารามิเตอร์:** 35B รวม / **3B active** (Mixture-of-Experts → เร็วและประหยัดตอน inference)
- **Context:** สูงสุด 262,144 tokens
- **OCRBench:** **90.0** (สูงสุดในตระกูล Qwen3.6) | **CC-OCR:** 81.9 | **AI2D:** 92.7
- Hugging Face: `Qwen/Qwen3.6-35B-A3B`
- ข้อสังเกต: แม้ active params น้อยกว่า แต่คะแนน OCR ดีกว่า/ใกล้เคียง 27B เพราะใช้พารามิเตอร์รวมทั้งหมด 35B

### 4.3 Qwen3.5 (รุ่นก่อน Qwen3.6 — VLM ทุกขนาด)
ตระกูล Qwen3.5 เป็น VLM โดยสมบูรณ์เหมือน Qwen3.6 (ไม่มี `-VL` ต่อท้าย) มีหลายขนาด:

| รุ่น | ประเภท | OCRBench | OmniDocBench1.5 | CC-OCR | AI2D |
|---|---|---|---|---|---|
| **Qwen3.5-9B** | Dense 9B | 85.0 | 86.2 | 76.7 | 89.6 |
| **Qwen3.5-27B** | Dense 27B | 89.4 | 88.9 | 81.0 | 92.9 |
| **Qwen3.5-35B-A3B** | MoE 35B/3B active | 91.0 | 89.3 | 80.7 | 92.6 |
| **Qwen3.5-397B-A17B** | MoE 397B/17B active | **93.1** | **90.8** | **82.0** | **93.9** |

- รุ่นอื่นในตระกูล: **4B** (OCRBench 89.2), **122B-A10B** (MoE, OCRBench 92.1)
- **จุดเด่นของ Qwen3.5:** รายงาน Benchmark ครบ ทั้ง `OmniDocBench1.5` (เอกสารหลายรูปแบบ), `MMLongBench-Doc` (เอกสารยาว), `CharXiv` (แผนภูมิ) — ตรงกับงาน OCR มากกว่า Qwen3.6 ที่รายงานน้อยกว่า
- Hugging Face: `Qwen/Qwen3.5-9B`, `Qwen/Qwen3.5-27B`, `Qwen/Qwen3.5-35B-A3B`, `Qwen/Qwen3.5-397B-A17B`

### 4.4 Qwen2.5-VL (รุ่นก่อนหน้า — อ้างอิง)
มีทั้งขนาด **3B / 7B / 32B / 72B** ตัวเลขหลัก ๆ:
- **OCRBench (สเกล 0–1000):** 7B = 864 (สูงกว่า GPT-4o-mini ที่ 785)
- **DocVQA (test):** 7B = 95.7 | 72B = 96.4
- **ChartQA (test):** 7B = 87.3
- **CC-OCR:** 7B = 77.8 | 72B = 79.8

### 4.5 Typhoon-OCR-7B
- **Base model:** `Qwen/Qwen2.5-VL-7B-Instruct` (fine-tune เฉพาะทาง OCR)
- **ภาษา:** ไทย + อังกฤษ (bilingual)
- **สัญญาอนุญาต:** Apache-2.0
- **รูปแบบเอกสารที่รองรับ:**
  - *Structured documents* (รายงานการเงิน, งานวิจัย, หนังสือ, ฟอร์มราชการ) → ส่งออกเป็น **Markdown** หรือ **HTML** (สำหรับตารางที่มี merged cells)
  - *Layout-heavy/informal documents* (ใบเสร็จ, เมนู, ตั๋ว, infographic) → Markdown แบบรู้ layout
- **จุดเด่น:** เหนือกว่า GPT-4o และ Gemini 2.5 Flash ในเอกสารไทยที่ layout ซับซ้อน/มีภาษาผสม
- **การใช้งาน:**
  ```bash
  pip install typhoon-ocr          # ใช้ผ่าน API
  # หรือรัน local ด้วย vLLM (ต้องมี GPU)
  vllm serve scb10x/typhoon-ocr-7b --max-model-len 32000 --served-model-name typhoon-ocr-preview
  ```
- **พารามิเตอร์แนะนำ:** `temperature=0.1`, `top_p=0.6`, `repetition_penalty=1.2`
- **ข้อควรมอบหมาย:** ต้องใช้ prompt เฉพาะ (`default` หรือ `structure`) เท่านั้น ใช้ prompt อื่นจะไม่ทำงาน
- มีเวอร์ชัน 3B (`typhoon-ocr-3b`, downloads ~390k) สำหรับทรัพยากรน้อยกว่า

### 4.6 Gemini 3.6 Flash
- **รุ่นปัจจุบัน** ของตระกูล Flash (สเถียร, GA)
- **Input:** text/image/video/audio/PDF, **Context:** 1M tokens, **Output:** 64k
- **ราคา:** $1.50 / 1M input, $7.50 / 1M output (ไม่มี caching)
- **จุดเด่น OCR-related:** CharXiv (No tools) = **85.2** (สูงสุดในตารางเปรียบเทียบ)
- เหมาะกับงาน OCR/เอกสารที่ต้องการคุณภาพสูงและ context ยาวมาก

### 4.7 Gemini 3.5 Flash-Lite
- **รุ่นประหยัด** ของตระกูล Flash (GA)
- **Input:** text/image/video/audio/PDF, **Context:** 1M tokens, **Output:** 64k
- **ราคา:** $0.30 / 1M input, $2.50 / 1M output (ถูกมาก)
- **CharXiv (No tools):** 74.5 | (With tools): 76.5
- เหมาะกับ **OCR ปริมาณมาก** เช่น ใบเสร็จ, สกัดข้อมูลง่าย ๆ ที่ต้องการ latency ต่ำและต้นทุนต่ำ (เคสตัวอย่างจริง: Ramp ใช้สำหรับ receipt extraction)

---

## 5. คำแนะนำการเลือกใช้งาน

| สถานการณ์ | โมเดลแนะนำ | เหตุผล |
|---|---|---|
| **เอกสารไทยเป็นหลัก** (รายงานการเงิน, ราชการ, layout ซับซ้อน) | **Typhoon-OCR-7B** | ออกแบบเฉพาะ OCR ไทย-อังกฤษ, เหนือกว่า GPT-4o/Gemini 2.5 Flash ในเอกสารไทย |
| เอกสารไทยทรัพยากรจำกัด | **Typhoon-OCR-3B** | ขนาดเล็ก, downloads สูง (~390k) |
| OCR คุณภาพสูง รันบนเครื่องตัวเอง, ไม่จำกัดภาษา | **Qwen3.6-35B-A3B** | OCRBench 90.0 สูงสุดในตระกูล, MoE ทำให้ inference ประหยัด |
| รันบนเครื่อง GPU ขนาดกลาง, ไม่ต้อง MoE | **Qwen3.6-27B** | Dense 27B, OCRBench 89.4 |
| OCR เอกสารครบ มี Benchmark ละเอียด (OmniDocBench/MMLongBench) | **Qwen3.5-27B / 35B-A3B** | OCRBench 89.4/91.0, มี benchmark เอกสารครบ |
| OCR คุณภาพสูงสุดในตระกูล Qwen โดยไม่จำกัดทรัพยากร | **Qwen3.5-397B-A17B** | OCRBench 93.1, OmniDocBench 90.8 (สูงสุด) |
| ทรัพยากรจำกัด แต่ต้องการ VLM คุณภาพดี | **Qwen3.5-9B** | Dense 9B, OCRBench 85.0 |
| งาน OCR ปริมาณมากมาก, ต้นทุนสำคัญ (ใบเสร็จ, extraction ง่าย) | **Gemini 3.5 Flash-Lite** | $0.30/$2.50 ต่อ 1M, latency ต่ำ, รองรับ PDF |
| เอกสาร/ภาพซับซ้อน คุณภาพสูงสุด, ยอมจ่าย | **Gemini 3.6 Flash** | CharXiv 85.2 สูงสุด, context 1M |
| ต้องการสเกล OCRBench 0–1000 เปรียบเทียบข้ามรุ่นเก่า | **Qwen2.5-VL-7B/32B/72B** | มีตัวเลขครบทุกขนาดพารามิเตอร์ |

### ข้อควรระวัง
1. **อย่าเปรียบเทียบ OCRBench ข้ามสเกล** — Qwen2.5-VL (0–1000) กับ Qwen3.6 (0–100) คำนวณต่างกัน
2. **Typhoon-OCR ใช้ prompt เฉพาะ** เท่านั้น (`default`/`structure`) — ใช้ prompt อื่นจะไม่ทำงาน
3. **GGUF ของ Typhoon** (llama.cpp/LM Studio) อาจมีปัญหาความแม่นยำ ทีมแนะนำให้ใช้ vLLM หรือ Ollama build ที่ `ollama.com/scb10x`
4. **Gemini 3.x ไม่รายงาน DocVQA/OCRBench แบบดั้งเดิม** จึงเปรียบเทียบตรงข้ามตระกูลไม่ได้โดยตรง — ใช้ CharXiv หรือทดสอบบนข้อมูลตัวเอง

---

## 6. แหล่งข้อมูล (Sources)

ข้อมูลดึงด้วย `curl` จาก Hugging Face API และอ่านจากหน้าเว็บทางการ:

**Hugging Face (ดึงด้วย `curl https://huggingface.co/.../raw/main/README.md` และ `/api/models`)**
- Qwen3.6-27B — https://huggingface.co/Qwen/Qwen3.6-27B
- Qwen3.6-35B-A3B — https://huggingface.co/Qwen/Qwen3.6-35B-A3B
- Qwen3.5-9B — https://huggingface.co/Qwen/Qwen3.5-9B
- Qwen3.5-27B — https://huggingface.co/Qwen/Qwen3.5-27B
- Qwen3.5-35B-A3B — https://huggingface.co/Qwen/Qwen3.5-35B-A3B
- Qwen3.5-397B-A17B — https://huggingface.co/Qwen/Qwen3.5-397B-A17B
- Qwen2.5-VL-32B-Instruct — https://huggingface.co/Qwen/Qwen2.5-VL-32B-Instruct
- Qwen2.5-VL-7B-Instruct — https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct
- typhoon-ocr-7b — https://huggingface.co/typhoon-ai/typhoon-ocr-7b
- typhoon-ocr-3b — https://huggingface.co/typhoon-ai/typhoon-ocr-3b
- typhoon-ocr1.5-3b-qat — https://huggingface.co/typhoon-ai/typhoon-ocr1.5-3b-qat

**Google DeepMind (หน้า Performance ทางการ)**
- Gemini 3.6 Flash — https://deepmind.google/models/gemini/flash/
- Gemini 3.5 Flash-Lite — https://deepmind.google/models/gemini/flash-lite/
- Gemini API model docs — https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite

**Qwen / Typhoon**
- Qwen3.6-27B blog — https://qwen.ai/blog?id=qwen3.6-27b
- Qwen3.6-35B-A3B blog — https://qwen.ai/blog?id=qwen3.6-35b-a3b
- Typhoon OCR release blog — https://opentyphoon.ai/blog/en/typhoon-ocr-release
- Typhoon OCR GitHub — https://github.com/scb-10x/typhoon-ocr
- Typhoon OCR arXiv (2601.14722) — https://arxiv.org/abs/2601.14722
- Typhoon OCR Demo — https://ocr.opentyphoon.ai/
