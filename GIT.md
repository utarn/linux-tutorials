# คู่มือ Git พื้นฐานสำหรับนักวิทยาศาสตร์และ Vibe Coding

เอกสารสอนคำสั่ง `git` พื้นฐาน ตั้งแต่การสร้าง repository, การ commit, การ push, การสร้าง/สลับ branch, การใช้งาน git worktree, การตั้งค่า `.gitignore` ไปจนถึงเทคนิคการแก้ไขไฟล์ที่ติด track ผิดด้วย `git rm --cached -r -f .` แล้วตามด้วย `git add .` พร้อม 3 สถานการณ์ตัวอย่างในการใช้คำสั่งเหล่านี้จริง

---

## 🧠 แนวคิดสำคัญก่อนเริ่ม (Git Mental Model)

ก่อนเรียนคำสั่ง ให้เข้าใจ 3 พื้นที่ของ Git ก่อน:

| พื้นที่ | ความหมาย | คำสั่งที่เกี่ยวข้อง |
|---|---|---|
| **Working Directory** | ไฟล์จริงในโฟลเดอร์ที่คุณแก้ไขอยู่ | แก้ไฟล์ด้วย editor |
| **Staging Area (Index)** | พื้นที่รวบรวมไฟล์ที่ "เตรียม" จะบันทึก | `git add` |
| **Repository (.git)** | ประวัติการบันทึก (commit) ถาวร | `git commit` |

> หลักการ: **แก้ไฟล์ → `git add` (ส่งเข้า Staging) → `git commit` (บันทึกถาวร) → `git push` (ส่งขึ้น server)**

---

## ⚡ คำสั่งที่ต้องรู้ก่อน (Git Survival Kit)

รวมคำสั่ง Git พื้นฐานที่ต้องรู้ พร้อมคอมเมนต์ภาษาไทยอธิบายทีละบรรทัด:

```bash
# 1. สร้าง Git repository ใหม่ในโฟลเดอร์ปัจจุบัน (จะเกิดโฟลเดอร์ .git ซ่อนอยู่)
git init

# 2. ตรวจสอบสถานะไฟล์ (แก้แล้ว / ยังไม่ add / พร้อม commit)
git status

# 3. เพิ่มไฟล์เข้าสู่ Staging Area (เตรียมบันทึก) — จุด . หมายถึงไฟล์ทั้งหมดในโฟลเดอร์
git add .

# 4. เพิ่มเฉพาะไฟล์ที่ระบุเข้า Staging Area
git add ชื่อไฟล์.py

# 5. บันทึกการเปลี่ยนแปลงลงประวัติ (commit) พร้อมข้อความอธิบาย
git commit -m "ข้อความอธิบายว่าแก้อะไร"

# 6. ดูประวัติการ commit ทั้งหมดใน branch ปัจจุบัน
git log --oneline --graph

# 7. เชื่อมต่อ repository ในเครื่องกับ server (GitHub/GitLab) — ทำครั้งเดียว
git remote add origin https://github.com/ชื่อผู้ใช้/ชื่อrepo.git

# 8. ส่ง commit จากเครื่องขึ้น server (push สาขา main ไปยัง remote ชื่อ origin)
git push -u origin main

# 9. ดาวน์โหลดประวัติและไฟล์ล่าสุดจาก server ลงมาเครื่อง
git pull

# 10. สร้าง branch ใหม่และสลับไปทำงานบน branch นั้นทันที
git switch -c ชื่อสาขา

# 11. สลับไปทำงานบน branch ที่มีอยู่แล้ว
git switch ชื่อสาขา

# 12. ดูรายการ branch ทั้งหมดในเครื่อง (เครื่องหมาย * คือ branch ปัจจุบัน)
git branch

# 13. ลบ branch ที่ไม่ใช้แล้ว (ต้องสลับออกก่อน)
git branch -d ชื่อสาขา
```

---

## 🎯 สถานการณ์ตัวอย่าง: นักวิทยาศาสตร์เริ่มใช้ Git เก็บโค้ดวิจัย

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่เคยเก็บโค้ดวิเคราะห์ข้อมูลเป็นไฟล์ `analysis_v1.py`, `analysis_v2_final.py`, `analysis_v2_final_REALLY.py` จนสับสน วันนี้คุณตัดสินใจใช้ Git ให้เป็นระบบ เพื่อให้ Claude Code ช่วยเขียนโค้ดและตามรอยการแก้ไขได้โดยไม่สูญหาย
>
> **ปัญหาเดิม:** กลัวแก้โค้ดแล้วพัง ไม่กล้าลบออกเลย เลยก๊อปปี้ไฟล์สำรองทิ้งไว้เยอะจนหาไม่เจอ
>
> **ทางออก:** ใช้ Git เก็บ "ภาพถ่าย" (commit) ของโค้ดทุกครั้งที่แก้ ถ้าพังก็ย้อนกลับได้ ไม่ต้องก๊อปปี้ไฟล์สำรองอีกต่อไป

---

## 1. การสร้าง Repository และ Commit แรก

### 🎯 สิ่งที่ต้องการเรียนรู้
- สร้าง Git repository ในโปรเจกต์ใหม่
- เพิ่มไฟล์เข้า Staging และบันทึก commit แรก

```bash
# สร้างโฟลเดอร์โปรเจกต์ใหม่สำหรับงานวิจัย
mkdir -p ~/research-project

# ย้ายเข้าไปในโฟลเดอร์โปรเจกต์
cd ~/research-project

# เริ่มต้นสร้าง Git repository (จะสร้างโฟลเดอร์ .git ซ่อนสำหรับเก็บประวัติ)
git init

# เปลี่ยนชื่อ branch หลักเริ่มต้นจาก master เป็น main (ธรรมเนียมปัจจุบัน)
git branch -M main

# สร้างไฟล์โค้ดวิเคราะห์ข้อมูลตัวอย่าง
echo "print('hello research')" > analysis.py

# ดูสถานะ — จะเห็นว่า analysis.py เป็นไฟล์ใหม่ที่ยังไม่ถูก track (Untracked files)
git status

# เพิ่มไฟล์ทั้งหมดในโฟลเดอร์เข้าสู่ Staging Area (เตรียมบันทึก)
git add .

# บันทึกการเปลี่ยนแปลงเป็น commit แรก พร้อมข้อความอธิบาย
git commit -m "เริ่มโปรเจกต์: เพิ่มไฟล์ analysis.py"

# ดูประวัติ commit (จะเห็น commit แรกที่เพิ่งสร้าง)
git log --oneline
```

---

## 2. การ Push ขึ้น Server (GitHub/GitLab)

### 🎯 สิ่งที่ต้องการเรียนรู้
- เชื่อมต่อ repository ในเครื่องกับ remote server
- ส่ง commit ขึ้น server เพื่อเก็บสำรองและแชร์

```bash
# เชื่อม repository ในเครื่องกับ server (ทำครั้งเดียวต่อ repository)
# 'origin' คือชื่อเล่นของ server ที่เราตั้งขึ้น (จะใช้ชื่อนี้เรียกตอน push)
git remote add origin https://github.com/ชื่อผู้ใช้/research-project.git

# ตรวจสอบว่าเชื่อมกับ server อะไรไว้บ้าง
git remote -v

# ส่ง branch main ขึ้น server origin ครั้งแรก
# แฟล็ก -u (set-upstream) ทำให้ครั้งต่อไปพิมพ์แค่ git push ได้เลย ไม่ต้องระบุชื่อ
git push -u origin main

# หลังจากนี้เวลาแก้โค้ดแล้ว commit ใหม่ ส่งขึ้น server แค่พิมพ์สั้นๆ:
git push
```

---

## 3. การสร้าง Branch และสลับ Branch

### 🎯 สิ่งที่ต้องการเรียนรู้
- แยก branch เพื่อทดลองโค้ดใหม่โดยไม่กระทบงานเดิม
- สลับไปมาระหว่าง branch

```bash
# ดู branch ทั้งหมด (ตอนนี้จะมีแค่ * main)
git branch

# สร้าง branch ใหม่ชื่อ 'experiment-new-model' และสลับไปทำงานบนนั้นทันที
# แฟล็ก -c ย่อมาจาก create
git switch -c experiment-new-model

# ตอนนี้คุณอยู่บน branch experiment-new-model — ลองแก้โค้ดดู
echo "print('new model')" >> analysis.py

# เพิ่มและบันทึกการเปลี่ยนแปลงบน branch นี้
git add .
git commit -m "ทดลองโมเดลใหม่บน branch แยก"

# สลับกลับไป branch main (โค้ดที่แก้บน branch experiment จะหายไปจากหน้าจอ แต่ยังอยู่ในประวัติ)
git switch main

# สลับกลับไป branch ทดลองอีกครั้ง (โค้ดที่แก้จะกลับมา)
git switch experiment-new-model

# ถ้าพอใจผลทดลองแล้ว รวมกลับเข้า main:
# สลับไป main ก่อน
git switch main

# ดึงการแก้ไขจาก branch ทดลองมารวมเข้า main (merge)
git merge experiment-new-model

# ลบ branch ทดลองทิ้งเมื่อไม่ใช้แล้ว
git branch -d experiment-new-model
```

---

## 4. การใช้งาน Git Worktree (ทำงานหลาย branch พร้อมกัน)

### 🎯 สิ่งที่ต้องการเรียนรู้
- สร้าง worktree เพื่อเปิด branch ต่างๆ ในโฟลเดอร์คนละอันพร้อมกันได้
- สลับไปมาระหว่าง worktree โดยไม่ต้อง stash หรือ commit งานค้าง

> **ทำไมต้อง Worktree?** ปกติเวลา `git switch` ไป branch อื่น ไฟล์ในโฟลเดอร์เดียวกันจะเปลี่ยนตาม — ถ้ามีงานค้างก็ต้อง stash ก่อน แต่ `git worktree` สร้างโฟลเดอร์แยกให้แต่ละ branch ทำให้เปิด VS Code ดู main และ branch ทดลองได้พร้อมกัน

```bash
# สร้าง worktree ใหม่สำหรับ branch ชื่อ 'feature-plot' ในโฟลเดอร์ ../research-plot
# คำสั่งนี้จะสร้างโฟลเดอร์ ../research-plot และ checkout branch นั้นไว้ให้ทันที
git worktree add ../research-plot feature-plot

# ถ้ายังไม่มี branch และอยากสร้างใหม่พร้อม worktree ในคำสั่งเดียว ใช้แฟล็ก -b
git worktree add -b feature-plot ../research-plot

# ดูรายการ worktree ทั้งหมด (จะเห็นโฟลเดอร์หลัก + โฟลเดอร์ที่เพิ่งสร้าง)
git worktree list

# ย้ายเข้าไปทำงานใน worktree ใหม่ (เหมือนเข้าโฟลเดอร์ปกติ)
cd ../research-plot

# ตอนนี้คุณอยู่บน branch feature-plot ในโฟลเดอร์คู่แข่ง แก้ไขได้อิสระ ไม่กระทบโฟลเดอร์หลัก
# (แก้ไขไฟล์, commit, push ได้ปกติเหมือน repository ทั่วไป)

# เมื่อทำเสร็จและรวมเข้า main แล้ว ลบ worktree ออกจากระบบ
# (ต้องย้ายออกจากโฟลเดอร์นั้นก่อน)
cd ../research-project
git worktree remove ../research-plot

# ทำความสะอาด worktree ที่โดนลบไฟล์ไปแล้วตามด้วย pruning metadata
git worktree prune
```

> **ข้อควรระวัง:** แต่ละ worktree ต้องอยู่คนละ branch — ห้ามเปิด branch เดียวกันใน 2 worktree พร้อมกัน

---

## 5. การใช้ `.gitignore` และการแก้ไฟล์ที่ติด track ผิด

### 🎯 สิ่งที่ต้องการเรียนรู้
- บอก Git ให้เพิกเฉยไฟล์ที่ไม่ควรเก็บ (เช่นข้อมูลวิจัยขนาดใหญ่, โฟลเดอร์ cache)
- แก้กรณีไฟล์/โฟลเดอร์ถูก commit เข้าไปแล้ว แล้วอยากเอาออกจากการ track แต่ยังเก็บไฟล์จริงไว้ในเครื่อง

```bash
# สร้างไฟล์ .gitignore เพื่อบอก Git ว่าไฟล์ไหนไม่ต้อง track
cat << 'EOF' > .gitignore
# ไฟล์ข้อมูลวิจัยขนาดใหญ่ — ไม่ควรเก็บใน Git (ใช้ Git LFS หรือเก็บใน server แยก)
*.csv
*.h5
data/

# โฟลเดอร์เก็บผลลัพธ์ที่สร้างได้ใหม่จากโค้ด
output/
results/

# สภาพแวดล้อม Python (venv) และไฟล์คอมไพล์
__pycache__/
*.pyc
venv/
.env

# ไฟล์ระบบจาก macOS/Windows
.DS_Store
Thumbs.db

# โฟลเดอร์ VS Code (ปกติเก็บได้ แต่ถ้าเป็นส่วนตัวก็เพิกเฉยได้)
# .vscode/
EOF

# ดูสถานะ — ไฟล์ที่ตรงเงื่อนไข .gitignore จะไม่ขึ้นใน untracked แล้ว
git status

# เพิ่ม .gitignore เข้า repository และ commit
git add .gitignore
git commit -m "เพิ่ม .gitignore เพื่อเพิกเฉยไฟล์ข้อมูลและ cache"
```

### 🛠️ กรณีฉุกเฉิน: ไฟล์/โฟลเดอร์ถูก commit เข้าไปแล้ว ต้องการเอาออกจากการ track

บางครั้งเรา commit ไฟล์ขนาดใหญ่ (เช่น `data/` หรือ `output/`) เข้าไปก่อนตั้ง `.gitignore` คำสั่งธรรมดาจะไม่เอาออกจากประวัติ ต้องใช้ `git rm --cached`:

```bash
# ดูสถานะปัจจุบัน (สมมติว่าไฟล์ใน data/ ถูก track อยู่)
git status

# เอาไฟล์ทุกอย่างออกจาก Staging/Index แต่ยังเก็บไฟล์จริงไว้ในเครื่อง
# --cached  = เอาออกจาก index เท่านั้น (ไม่ลบไฟล์จริง)
# -r        = ทำแบบ recursive (กรณีเป็นโฟลเดอร์)
# -f        = force บังคับลบแม้จะมีการเปลี่ยนแปลง
# จุด .     = หมายถึงไฟล์ทุกอย่างในโฟลเดอร์ปัจจุบัน
git rm --cached -r -f .

# ตอนนี้ไฟล์ทั้งหมดกลายเป็น "untracked" แต่ไฟล์จริงยังอยู่ในเครื่องไม่หาย
git status

# เพิ่มไฟล์กลับเข้า Staging ใหม่ — คราวนี้ .gitignore จะทำงาน
# ไฟล์ที่ตรงเงื่อนไขใน .gitignore (เช่น data/, *.csv) จะไม่ถูก add กลับ
git add .

# บันทึกการเปลี่ยนแปลง — commit นี้จะ "เอาไฟล์เหล่านั้นออกจาก repository"
# (แต่ไฟล์จริงในเครื่องยังอยู่ เพราะเราใช้ --cached ไม่ได้ลบจริง)
git commit -m "เอาไฟล์ข้อมูล/cache ออกจากการ track ตาม .gitignore"

# ส่งการแก้ไขขึ้น server
git push
```

> **สรุปแพทเทิร์น:** `git rm --cached -r -f .` → `git add .` → `git commit` → `git push`
> ใช้เมื่อเพิ่งตั้ง/แก้ `.gitignore` แล้วอยากให้ไฟล์ที่เคยติด track ออกจาก repository โดยไม่ลบไฟล์จริงในเครื่อง

> **หมายเหตุ:** คำสั่งนี้เอาไฟล์ออกจาก commit ปัจจุบันเท่านั้น ไม่ได้ลบจากประวัติเดิม ถ้าไฟล์ใหญ่มาก/มีข้อมูลลับที่ติดไปในอดีต ต้องใช้เครื่องมืออย่าง `git filter-repo` หรือ BFG Repo-Cleaner เพื่อล้างประวัติแบบถาวร

---

## 🧪 สถานการณ์ตัวอย่างทั้ง 3 แบบ (Practice Scenarios)

ด้านล่างคือ 3 สถานการณ์ที่นำคำสั่งข้างต้นมาใช้จริงตามลำดับ ตั้งแต่เริ่มโปรเจกต์จนถึงขั้นสูง

---

### 🧪 สถานการณ์ที่ 1: เริ่มโปรเจกต์วิจัยใหม่ตั้งแต่ต้น จน push ขึ้น GitHub

> **เป้าหมาย:** นักวิทยาศาสตร์สร้างโปรเจกต์ `climate-analysis` ตั้งแต่โฟลเดอร์ว่าง จนมี commit แรกขึ้น GitHub

```bash
# สร้างและเข้าโฟลเดอร์โปรเจกต์ใหม่
mkdir -p ~/climate-analysis && cd ~/climate-analysis

# สร้าง Git repository ในโฟลเดอร์นี้
git init

# ตั้งชื่อ branch หลักเป็น main
git branch -M main

# สร้างไฟล์ .gitignore เพื่อเพิกเฉยไฟล์ข้อมูลขนาดใหญ่ตั้งแต่เริ่มต้น
cat << 'EOF' > .gitignore
# เพิกเฉยไฟล์ข้อมูล climate ขนาดใหญ่ และผลลัพธ์
*.nc
*.grib
data/
output/
__pycache__/
*.pyc
EOF

# สร้างไฟล์โค้ดหลัก
cat << 'EOF' > main.py
print("Climate analysis starter")
EOF

# ดูสถานะ — จะเห็น main.py และ .gitignore รอการเพิ่ม
git status

# เพิ่มไฟล์ทั้งหมดเข้า Staging
git add .

# บันทึก commit แรก
git commit -m "เริ่มโปรเจกต์ climate-analysis: main.py และ .gitignore"

# เชื่อมกับ repository บน GitHub (สมมติสร้าง repo ว่างบน GitHub ไว้แล้ว)
git remote add origin https://github.com/ชื่อผู้ใช้/climate-analysis.git

# ส่ง branch main ขึ้น server ครั้งแรก
git push -u origin main
```

---

### 🧪 สถานการณ์ที่ 2: ทดลองโมเดลใหม่ด้วย Branch และ Merge กลับ

> **เป้าหมาย:** ลองเปลี่ยนวิธีวิเคราะห์บน branch แยก ถ้าดีก็รวมกลับเข้า main ถ้าไม่ดีก็ทิ้งได้โดยงานเดิมไม่กระทบ

```bash
# สร้าง branch ใหม่สำหรับทดลองโมเดลใหม่ และสลับไปทันที
git switch -c experiment-neural-net

# แก้ไฟล์ main.py เพิ่มโค้ดทดลอง (จำลองด้วย echo)
echo "# ทดลองใช้ neural network" >> main.py

# เพิ่มและ commit บน branch ทดลอง
git add .
git commit -m "ทดลองใช้ neural network สำหรับ climate"

# สลับกลับไป main (โค้ดทดลองจะหายไปจากหน้าจอ แต่ยังอยู่ในประวัติ)
git switch main

# สมมติว่าผลทดลองดี อยากรวมเข้า main
git merge experiment-neural-net

# ลบ branch ทดลองทิ้งหลังรวมเรียบร้อย
git branch -d experiment-neural-net

# ส่งผลการ merge ขึ้น server
git push

# --- ทางเลือก: ถ้าทดลองแล้วไม่ดี ไม่ต้อง merge ก็ได้ ---
# สลับกลับ main แล้วลบ branch ทดลองทิ้งเลย (งานเดิมบน main ไม่กระทบ):
# git switch main
# git branch -D experiment-neural-net   # -D บังคับลบ แม้ยังไม่ได้ merge
```

---

### 🧪 สถานการณ์ที่ 3: ใช้ Git Worktree ทำงาน 2 branch พร้อมกัน + แก้ไฟล์ติด track ผิด

> **เป้าหมาย:** ขณะรันโค้ดบน main อยู่ อยากลองแก้ plot บน branch ใหม่โดยไม่หยุดงาน main พร้อมแก้ปัญหาโฟลเดอร์ `data/` ขนาดใหญ่ที่เผลอ commit เข้าไป

```bash
# สร้าง worktree ใหม่สำหรับ branch ทดลอง plot ในโฟลเดอร์ข้างๆ
# -b สร้าง branch ใหม่ชื่อ feature-plot พร้อม checkout ในโฟลเดอร์ ../climate-plot
git worktree add -b feature-plot ../climate-plot

# ดูรายการ worktree ทั้งหมด (จะเห็น 2 โฟลเดอร์: หลัก + climate-plot)
git worktree list

# ย้ายเข้าไปทำงานใน worktree ใหม่
cd ../climate-plot

# แก้โค้ด plot ได้อิสระ — โฟลเดอร์หลักที่เปิดค้างไว้ไม่กระทบ
echo "# เพิ่ม plot function" >> main.py
git add .
git commit -m "เพิ่มฟังก์ชัน plot บน worktree"

# กลับไปโฟลเดอร์หลักเพื่อแก้ปัญหา data/ ที่ติด track ผิด
cd ../climate-analysis

# สมมติว่าเราเผลอ commit โฟลเดอร์ data/ (ขนาดใหญ่มาก) เข้าไปก่อนตั้ง .gitignore
# ปรับ .gitignore ให้เพิกเฉย data/ ก่อน (เพิ่มบรรทัด data/ ถ้ายังไม่มี)
echo "data/" >> .gitignore

# เอาไฟล์ทุกอย่างออกจาก index แต่ไม่ลบไฟล์จริง (--cached -r -f .)
git rm --cached -r -f .

# ตอนนี้ไฟล์ทั้งหมดกลายเป็น untracked แต่ไฟล์จริงยังอยู่
git status

# เพิ่มไฟล์กลับใหม่ — data/ จะไม่ถูก add ตาม .gitignore
git add .

# commit เพื่อเอา data/ ออกจาก repository (ไฟล์จริงในเครื่องยังอยู่)
git commit -m "เอา data/ ขนาดใหญ่ออกจาก track ตาม .gitignore"

# ส่งการแก้ไขขึ้น server
git push

# กลับไป worktree ทดลอง plot เพื่อทำต่อ
cd ../climate-plot

# พอเสร็จและ merge เข้า main แล้ว กลับมาลบ worktree
cd ../climate-analysis
git worktree remove ../climate-plot

# ทำความสะอาด metadata ของ worktree ที่เหลือ
git worktree prune

# ดูประวัติทั้งหมดเป็นกราฟสวยๆ
git log --oneline --graph --all
```

---

## 📌 สรุปคำสั่งตามสถานการณ์ (Cheat Sheet)

| สถานการณ์ | คำสั่ง |
|---|---|
| เริ่ม repo ใหม่ | `git init` → `git add .` → `git commit -m "..."` |
| ส่งขึ้น server | `git remote add origin <url>` → `git push -u origin main` |
| ทดลองโดยไม่กระทบงานเดิม | `git switch -c branch` → แก้ → `git commit` → `git switch main` → `git merge branch` |
| ทำ 2 branch พร้อมกัน | `git worktree add -b branch ../folder` → `cd ../folder` |
| ดู/ลบ worktree | `git worktree list` → `git worktree remove ../folder` → `git worktree prune` |
| บอก Git เพิกเฉยไฟล์ | สร้าง `.gitignore` → `git add .gitignore` → `git commit` |
| แก้ไฟล์ติด track ผิด | `git rm --cached -r -f .` → `git add .` → `git commit` → `git push` |

---

## ⚠️ ข้อควรระวังสำหรับนักวิทยาศาสตร์

- **อย่า commit ไฟล์ข้อมูลขนาดใหญ่** (เช่น `.csv`, `.nc`, `.h5`, ภาพถ่ายดาวเทียม) เข้า Git โดยตรง — ใช้ `.gitignore` หรือ [Git LFS](https://git-lfs.com/) สำหรับไฟล์ใหญ่
- **อย่า commit ข้อมูลลับ** (API key, ข้อมูลคนไข้) — ใส่ใน `.gitignore` ทันที (เช่น `.env`)
- **`git rm --cached` ไม่ได้ลบไฟล์จริง** แต่ถ้าเคย commit ข้อมูลลับไปแล้ว มันยังอยู่ในประวัติเดิม ต้องใช้ `git filter-repo` ล้าง
- **Commit บ่อยๆ ข้อความชัดๆ** — เช่น `"เพิ่มฟังก์ชันคำนวณค่าเฉลี่ย"` ดีกว่า `"update"`
- **ก่อน push ทุกครั้ง** ตรวจด้วย `git status` ก่อนว่าไม่มีไฟล์ที่ไม่ควรขึ้นไป
