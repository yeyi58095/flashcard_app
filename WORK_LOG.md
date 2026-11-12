# 航電閃卡專案工作日誌

更新日期：2026-11-13（Asia/Taipei）

## 使用者希望完成的事

- 依原 Streamlit 範例完成航電名詞自我檢查 app，含全部題庫與實際啟動驗證。
- 題庫來源包括 alias.txt 與學長的/航電期中考重點整理.pdf；依主題分組。
- 先顯示詞彙、自行回想，翻開全名與解釋，再標記「我知道」或「還不熟」，不需輸入答案批改。
- 保留原 flashcard_app.py、flashcards.txt，航電版使用獨立程式與題庫。
- 推送到 https://github.com/yeyi58095/flashcard_app.git，支援 Streamlit 啟動。

## 已完成

- alias.txt 共 10 個單元、152 張卡；工作區根目錄與 app 目錄內的版本 SHA256 相同。此輪保留既有題庫，未新增或重新校訂 PDF 內容。
- avionics_flashcard_app.py 支援分單元、全部混合練習、歷史錯題複習、隨機出題、翻卡、自評、進度與答對率。
- 不熟的卡立即寫入 wrongs.txt；支援本輪錯題重練、下載，以及歷史錯題依單元與詞彙去重複習。
- 錯題寫入失敗時顯示警告，仍保留本輪錯題、可繼續練習。
- 新增 start.cmd 與 start.ps1：雙擊啟動，自動切換目錄並使用 .venv；缺少依賴時安裝 requirements.txt。
- 原 python 指令指向無法執行的 WindowsApps 別名；已用 Codex 附帶 Python 3.12.14 建立專案 .venv，安裝 Streamlit 1.67.0。
- README.md 已改為中文啟動與操作說明。原範例程式及題庫未修改，個人錯題與 .venv 由 Git 忽略。

## 驗證結果

- 4 個 unittest / Streamlit AppTest 測試全數通過。
- 152 張卡逐張翻開並標記完成，驗證 10 個單元全部載入、卡片不遺漏、自評 100%、可重新開始。
- 驗證混合對錯的答對率、錯題立即保存、本輪錯題重練、歷史去重、切換單元、空歷史提示及寫入失敗處理。測試使用暫存錯題，不污染個人紀錄。
- start.ps1 已實際啟動 http://127.0.0.1:8501 ，首頁與 /_stcore/health 皆回應 HTTP 200。
- Windows PowerShell 的 start.cmd 也已在 8502 埠實際啟動並通過健康檢查；測試服務隨後關閉。
- 沙箱執行測試與本機連線受到限制；上述成功驗證是在核准的正常本機執行環境完成。

## 使用方式

雙擊本資料夾的 start.cmd。若服務仍在執行，可直接開啟 http://127.0.0.1:8501 。關閉啟動視窗或按 Ctrl+C 停止。

PowerShell 亦可執行：

```powershell
cd D:\daniel\GradSchool\115_Fall\DigitalAvionics\flashcard_app
.\start.cmd
```

測試：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Git 紀錄

- 前一版已推送至 master：db8a340（Add avionics self-assessment flashcards）。
- 本輪提交包含啟動捷徑、完整練習模式、測試與更新文件；提交及推送結果見本輪回覆與 Git 歷史。
