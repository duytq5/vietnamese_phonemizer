# Báo cáo: So sánh số lượng âm tiết khả dĩ và âm tiết thực tế trong tiếng Việt

## 1. Cấu trúc âm tiết tiếng Việt

Âm tiết tiếng Việt được mô hình hóa theo công thức:


## Âm tiết = Âm đầu + Âm đệm + Âm chính + Âm cuối + Thanh điệu


- **Âm đầu**: {ONSETS_COUNT} phụ âm ({ONSETS_LIST}).  
- **Âm đệm**: chỉ có {GLIDES_COUNT} ({GLIDES_LIST}).  
- **Âm chính**: khoảng {NUCLEI_COUNT} ({NUCLEI_LIST}).  
- **Âm cuối**: {CODAS_COUNT} ({CODAS_LIST}).  
- **Thanh điệu**: {TONES_COUNT} ({TONES_LIST}).  

---

## 2. Kết quả tính toán số lượng âm tiết

Áp dụng công thức tổ hợp:


## {ONSETS_COUNT} * {GLIDES_COUNT} * {NUCLEI_COUNT} * {CODAS_COUNT} * {TONES_COUNT} = {POSSIBLE_SYLLABLES}


→ Đây là số lượng **âm tiết khả dĩ** theo lý thuyết.

Khi thống kê từ điển chuẩn, số lượng âm tiết **thực tế** chỉ có khoảng **{SYLLABLE_COUNT}**.

---

## 3. Giải thích sự khác biệt

Sự chênh lệch giữa số lượng âm tiết khả dĩ và thực tế xuất phát từ **các ràng buộc ngữ âm, chính tả và phân bố**:

### 3.1. Quan hệ giữa âm đầu và âm đệm

- **Âm đầu /k/ (k, q, c):**  
  - `q` luôn đi với âm đệm `u`.  
  - `k` và `c` thường không có âm đệm đi kèm.  
  - **Ví dụ đúng:** `quà` (`q` + `u`), `kẻ` (`k` không có âm đệm)  
  - **Ví dụ sai:** `*qa`, `*ko`  

- **Âm đệm /-u-/:**  
  - **Ràng buộc:**  
    - Kết hợp với các phụ âm đầu môi (**b, m, ph, v**) **rất hiếm**, thường chỉ xuất hiện trong **từ mượn**.  
    - Không kết hợp trước các nguyên âm **tròn môi** (`u, uô, ơ, o`) hoặc nguyên âm **khép** (`ư, ươ`).  
  - **Ví dụ đúng phổ biến (thuần Việt):**  
    - `hoa` (`h` + `o` + `a`)  
    - `khuya` (`kh` + `uya`)  
  - **Ví dụ đúng hiếm / từ mượn:**  
    - `buýt`  
    - `moay-ơ`  
    - `huơ`  
  - **Ví dụ sai (không hợp lệ trong tiếng Việt thuần):**  
    - `*vuơ` (âm đầu môi + âm đệm /u/ + nguyên âm ơ)  
    - `*muo` (âm đầu môi + âm đệm /u/ + nguyên âm o)  


### 3.2. Quan hệ giữa âm đầu và âm chính
- **k, gh, ngh:** Chỉ đi với nguyên âm dòng trước **e, ê, i, iê**  
  - **Ví dụ Đúng:** `kẻ`, `ghi`, `nghèo`  
  - **Ví dụ Sai:** `*kà` (phải là `cà`), `*gê` (phải là `ghê`)  

- **c, g, ng:** Đi với các nguyên âm còn lại  
  - **Ví dụ Đúng:** `cà`, `gỗ`, `ngõ`  
  - **Ví dụ Sai:** `*cẻ` (phải là `kẻ`), `*ngi` (phải là `nghi`)  

### 3.3. Phân bố /-u-/

- **Ràng buộc:**  
  - **Không đứng trước các nguyên âm tròn môi** (`u, o, uô, ơ`) hoặc **nguyên âm khép** (`ư, ươ`).  
  - Vi phạm ràng buộc này tạo ra **âm tiết không tồn tại trong tiếng Việt thuần**.  

- **Ví dụ đúng (thuần Việt):**  
  - `huy` (`h` + `uy`)  
  - `hoa` (`h` + `oa`)  

- **Ví dụ sai:**  
  - `huo` (`u` đến trước nguyên âm tròn môi `o`)  
  - `cuơ` (`u` đến trước nguyên âm tròn môi `ơ`)  
  - `ưo` (`o` đến sau nguyên âm khép `ư`)  


### 3.4. Hạn chế về âm cuối
- Tiếng Việt chỉ có **8 phụ âm cuối hợp lệ**: -c, -ch, -m, -n, -ng, -nh, -p, -t  
- **Ví dụ Đúng:** `ác`, `làm`, `tin`, `tập`  
- **Ví dụ Sai:** `*đab`, `*tag`  

### 3.5. Quan hệ giữa âm chính và âm cuối
- Một số âm cuối chỉ xuất hiện sau nguyên âm dòng trước **i, e, ê, iê**  
- **Ví dụ Đúng:** `ích`, `inh`  
- **Ví dụ Sai:** `*uch`  

### 3.6. Quan hệ giữa âm cuối và thanh điệu
- Âm cuối tắc (-p, -t, -c, -ch) chỉ đi với **thanh sắc và nặng**  
- **Ví dụ Đúng:** `tập` (nặng), `ác` (sắc)  
- **Ví dụ Sai:** `*tàp`, `*ảc`  

---

## 4. Kết luận

- Số lượng âm tiết khả dĩ tính theo tổ hợp lý thuyết rất lớn (**{POSSIBLE_SYLLABLES}**).  
- Tuy nhiên, do các **ràng buộc ngữ âm – chính tả – thanh điệu** của tiếng Việt, chỉ có khoảng **{SYLLABLE_COUNT} âm tiết thực sự tồn tại trong từ điển**.  
- Điều này phản ánh rõ sự khác biệt giữa **khả năng ngữ âm hình thức** và **tính hiện thực ngôn ngữ**.
