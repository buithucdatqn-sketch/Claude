# Ảnh nguồn · Tập 7

Bài: `AH-Decode-Decor/bai-03-3-bai-hoc-anh-sang-tu-nhien-noi-that/bai-03.md`, nhánh `AH-Interior-notes`, commit `dad48a5494ea48cfecd8e479089e94c1e7e80c13`. Tập đầu tiên theo nguyên tắc mới mục 2b (ít nhất hai ảnh chụp + mặt cắt/mặt bằng định vị). Engine v8 (nhiều ảnh nguồn, đổi ảnh = mờ chéo 0,7 giây).

| Khoá | Loại | Ảnh trong kho | Bản làm việc | Cảnh | Credit |
|---|---|---|---|---|---|
| main | ảnh chụp | `anh/07-doodle-cua-cao-ban-an.jpg`; nền `anh/goc/07-goc-cua-cao-ban-an.jpg` | `source.png` (gốc), `source_orig.png` (có doodle) 1600×2400 | 1, 2, 6, 8, 9, 10, 11 | Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking |
| lam | ảnh chụp | `anh/06-doodle-vach-lam-cau-thang.jpg`; nền `anh/goc/06-goc-vach-lam-cau-thang.jpg` | `source_lam.png`, `source_lam_orig.png` 1600×2400 | 7 | như trên |
| sodo | sơ đồ | `anh/05-diagram-cua-thap-cua-cao.png` | `source_sodo.png` 2160×2400 | 3, 4 | Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014) |
| catdoc | mặt cắt | `anh/04-mat-cat-doc-union-street.png` | `source_catdoc.png` 2400×1749 | 5 | Mặt cắt dọc: bản vẽ Prior Barraclough, nguồn ArchDaily (2023) |

- Lớp nét (`engine_ep07/doodle_ep07.npz`) = hiệu giữa ảnh doodle và ảnh gốc của bài (khớp pixel, không cần inpaint). Chỉ dùng mũi tên và nhãn nhỏ; tiêu đề lớn, dòng phụ và credit vẽ tay của bài không dùng.
- Sơ đồ và mặt cắt giữ nguyên nhãn có sẵn, không vẽ thêm.
- Hạn chế: chữ nhỏ trong mặt cắt chỉ nhìn được dáng ở khung 1080×1920, lời đọc và tiêu đề khung gánh phần giải thích; đoạn mũi tên gốc đi qua vùng trời trắng ở ảnh 07 bị đứt trong lớp nét nhưng trên nền trời trắng không nhận ra.
