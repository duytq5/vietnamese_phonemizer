# Vietnamese Phonemizer / Phiên âm Tiếng Việt

[English](#english) | [Tiếng Việt](#tiếng-việt)

---

## English

### Description
A web-based Vietnamese phonemizer application that converts Vietnamese text into phonemic transcription. This project provides an intuitive interface for phonological analysis of Vietnamese language using Gradio framework.

### Features
- Vietnamese text to phonemic transcription conversion

### Prerequisites
Before running this project, you need to install `uv`, a fast Python package installer and resolver.

#### Installing uv
Choose one of the following methods:

**On macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**With pip:**
```bash
pip install uv
```

**With Homebrew (macOS):**
```bash
brew install uv
```

**With Chocolatey (Windows):**
```bash
choco install uv
```

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd vietnamese-phonemizer
```

2. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

Or if you don't have a requirements.txt file yet:
```bash
uv pip install gradio vietnamese-phonemizer
```

### Usage
1. Run the application:
```bash
python main.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:7860`)

3. Enter Vietnamese text in the input field and click "Process Input" to get the phonemic transcription

### Team Members
- Trần Quang Duy - 24C12027
- Đỗ Hoài Nam - 24C12021

### License
This project is created as part of academic coursework.

---

## Tiếng Việt

### Mô tả
Ứng dụng web phiên âm âm vị học tiếng Việt, chuyển đổi văn bản tiếng Việt thành ký hiệu âm vị học. Dự án cung cấp giao diện trực quan để phân tích âm vị học của tiếng Việt sử dụng framework Gradio với module phiên âm tiếng Việt tự viết.

### Tính năng
- Chuyển đổi văn bản tiếng Việt sang phiên âm âm vị học
- Giao diện web đơn giản và thân thiện với người dùng
- Xử lý thời gian thực
- Được xây dựng với Gradio để dễ dàng triển khai

### Yêu cầu hệ thống
Trước khi chạy dự án này, bạn cần cài đặt `uv`, một trình cài đặt và giải quyết gói Python nhanh.

#### Cài đặt uv
Chọn một trong các phương pháp sau:

**Trên macOS và Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Trên Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Với pip:**
```bash
pip install uv
```

**Với Homebrew (macOS):**
```bash
brew install uv
```

**Với Chocolatey (Windows):**
```bash
choco install uv
```

### Cài đặt
1. Clone repository:
```bash
git clone <repository-url>
cd vietnamese-phonemizer
```

2. Cài đặt dependencies bằng uv:
```bash
uv pip install -r requirements.txt
```

Hoặc nếu chưa có file requirements.txt:
```bash
uv pip install gradio vietnamese-phonemizer
```

### Cách sử dụng
1. Chạy ứng dụng:
```bash
python main.py
```
Hoặc 
```bash 
python 3 main.py
```

2. Mở trình duyệt web và truy cập URL được hiển thị trong terminal (thường là `http://127.0.0.1:7860`)

3. Nhập văn bản tiếng Việt vào trường input và nhấn "Process Input" để nhận kết quả phiên âm âm vị học

### Thành viên nhóm
- Trần Quang Duy - 24C12027
- Đỗ Hoài Nam - 24C1202

---
