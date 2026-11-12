# 航電閃卡專案工作日誌

更新日期：2026-11-13（Asia/Taipei）

## 最新進度：題庫情境化與手機使用說明

- 使用者指出 R 單獨出題缺乏提示，要求重新整理題庫並說明手機使用方式。
- 全部 152 張卡已加上完整問句（alias.txt 的「? 」行）；兩份 alias.txt 同步更新，仍為 10 個單元。
- U/V/W 與 P/Q/R 明確標示為機體座標系的線速度或角速度分量，說明大小寫與容易混淆的同名符號；翻開前不直接透露對應答案。
- 依課程期中整理、FAA／NASA／ICAO 來源檢查易混淆項目，修正 Angle of Incidence、Load Factor、側滑角與氣動中心等解釋；擴充六個運動分量與故障後可運作的適用條件。
- app 改成顯示完整問題，保留原詞彙索引與錯題相容性；題庫內容變更會重開本輪，避免保留舊答案。
- 6 項測試通過：含逐張完成 152 卡、每卡皆有問題、兩份題庫相同，以及 R 翻開前有機體角速度情境、翻開後才有 Yaw Rate 答案。
- 更新後本機服務健康檢查 HTTP 200。
- README 已加入 Streamlit Community Cloud 的實際儲存庫／master 分支／avionics_flashcard_app.py／Python 3.12 設定與同 Wi-Fi 使用步驟。尚未登入或建立雲端部署。
- 已說明本版本歷史錯題是服務端共用檔案，未實作個人帳號同步；Community Cloud 不保證檔案永久保留，應下載需要保存的錯題。
- 上一輪完成版本為 8bc5781；本輪提交與推送結果見 Git 歷史。

## 使用者希望完成的事

- 依原 Streamlit 範例完成航電名詞自我檢查 app，含全部題庫與實際啟動驗證。
- 題庫來源包括 alias.txt 與學長的/航電期中考重點整理.pdf；依主題分組。
- 先顯示詞彙、自行回想，翻開全名與解釋，再標記「我知道」或「還不熟」，不需輸入答案批改。
- 保留原 flashcard_app.py、flashcards.txt，航電版使用獨立程式與題庫。
- 推送到 https://github.com/yeyi58095/flashcard_app.git，支援 Streamlit 啟動。

## 已完成

- 初版 alias.txt 共 10 個單元、152 張卡；工作區根目錄與 app 目錄內的版本相同。最新題庫校訂見上方進度。
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
