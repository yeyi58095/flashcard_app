# 航電名詞閃卡

使用 alias.txt 的 10 個單元、152 張卡。先自行回想，翻開全名與解釋，再標記「我知道」或「還不熟」，不需要輸入答案。

## Windows 啟動

雙擊 start.cmd，即可使用專案的 Python 環境啟動。第一次缺少依賴時會自動安裝，需要網路。關閉終端視窗或按 Ctrl+C 即可停止。

也可以從 PowerShell 執行：

```powershell
cd D:\daniel\GradSchool\115_Fall\DigitalAvionics\flashcard_app
.\start.cmd
```

瀏覽器沒有自動開啟時，開啟終端顯示的網址，預設為 http://127.0.0.1:8501 。

## 一般 Python 環境

需要 Python 3.10 以上。啟動器可使用 PATH 上的 Python，或本機 Codex 附帶的 Python 建立 .venv。也可手動設定：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run avionics_flashcard_app.py
```

## 功能與紀錄

- 分單元練習、全部混合練習、歷史錯題複習，每輪隨機排列。
- 顯示來源單元、進度、自評答對率及不熟的卡。
- 可只重練本輪錯題、下載本輪錯題，或重練整組。
- 「還不熟」即時追加到 wrongs.txt，歷史複習依單元與詞彙去重並使用最新題庫解釋。歷史紀錄保留所有曾標記不熟的詞，不會因後來答對而移除。
- 切換單元或練習方式會開始新一輪；重新整理瀏覽器後，本輪進度可能重設，歷史錯題仍保留。

題庫格式為 [單元名稱]，下面每行為「縮寫: 全名: 解釋」或「名詞: 解釋」。app 讀取本資料夾的 alias.txt；工作區根目錄的 alias.txt 是相同內容的副本。

原 flashcard_app.py 與 flashcards.txt 保留不修改。.venv 和個人錯題 wrongs.txt 不提交到 Git。

## 驗證

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
