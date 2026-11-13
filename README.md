# 航電複習閃卡

使用 alias.txt 的 30 個單元、452 張情境題。每張卡有完整問句，指出需回想的全名、功能、原理或符號定義；自行回想後翻開答案，再標記「我知道」或「還不熟」。


## 四小時火車複習：新增 300 題作業型練習

原 152 張名詞卡保留，另新增 20 個單元，每單元 15 題，共 300 題。依 HW1–3、Practice_HW 及 Handout 1–7 的既有教材改寫，包含完整申論、因果解釋、系統架構、回授訊號、比較、故障情境、推導與數值計算。各新增單元在 alias.txt 的註解標示來源；題目編號以 HW- 開頭，部分為依課程範圍自編，並非全部作業原題。

| 單元 | 主題 |
|---|---|
| 11–14 | 數位航電取捨、取樣量化、CNS、GNC 與回授架構 |
| 15–17 | 為什麼需要 FBW、FBW 方塊圖、控制律與操縱品質 |
| 18–20 | 高度自駕、航向自駕、冗餘與故障處理 |
| 21–25 | 氣動力、升力與載荷計算、靜穩定、六自由度與線性化 |
| 26–30 | INS 架構與誤差、DR 與融合、GPS 架構與增強 |

可選「作業與申論混合」直接練新增 300 題，或在「分單元練習」挑選主題。架構題先自行畫方塊、箭頭與回授，再翻開答案；計算題先列公式、單位與假設，再核對數值。答案使用「 || 」分段，在 app 內分開顯示。

建議時間安排（按熟悉度調整，不必一次做完）：第一小時練 15–19 的 FBW 與自駕；第二小時練 20、23、25 的冗餘與穩定模型；第三小時練 26–30 的 INS／GPS；最後一小時補 22 的計算題、其他弱項與錯題。

App 的「上車前下載」區提供 offline_review.html 與 review_guide.txt，均含全部 452 題。HTML 在支援 JavaScript 的瀏覽器中可離線翻卡、自評與保存本機進度；手機檔案預覽器若不支援，改看文字題本。離線進度不與 Streamlit 同步。

維護題庫後可執行 `python tools/build_review.py` 重新產生兩份離線檔；產生器會檢查缺題、空答案與重複索引。

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

題庫格式為 [單元名稱]，卡片前加「? 題目」，下一行保留「縮寫: 全名: 解釋」或「名詞: 解釋」。例如：

```text
? 在機體座標系中，角速度分量 r（本題庫索引 R，非旋轉矩陣）代表哪種旋轉？繞哪個軸？
R: Yaw Rate（r）: 機體角速度沿 z 軸的分量，即繞機體垂直軸的偏航角速度。
```

app 讀取本資料夾的 alias.txt；工作區根目錄的 alias.txt 是相同內容的副本。原有詞彙索引保持不變，歷史錯題仍可比對。舊格式若缺少問句，app 會提供包含單元的預設問句。更新題庫後，正在進行的一輪會重新開始，避免顯示舊答案。

原 flashcard_app.py 與 flashcards.txt 保留不修改。.venv 和個人錯題 wrongs.txt 不提交到 Git。

## 用手機：部署到 Streamlit Community Cloud

部署後用手機瀏覽器開啟網址即可，不需要電腦一直開著。以下依 [Streamlit 官方部署說明](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)：

1. 前往 https://share.streamlit.io ，登入並連接你的 GitHub 帳號。
2. 按 Create app；若詢問是否已有程式，選 Yup, I have an app。
3. 填入 Repository：`yeyi58095/flashcard_app`，Branch：`master`，Main file path：`avionics_flashcard_app.py`。這裡是儲存庫根目錄，不用再加 flashcard_app/。
4. Advanced settings 選 Python 3.12，與目前已驗證的本機版本一致；此 app 不需填 secrets。
5. 按 Deploy，等待安裝完成。requirements.txt 已在儲存庫中。
6. 把產生的 https://某個名稱.streamlit.app 網址用手機開啟並加入書籤。

目前只準備好程式與部署設定，尚未替帳號建立雲端部署。

錯題記錄寫在執行服務的主機，而非手機；目前沒有登入或個別使用者資料庫，分享同一個部署會共用歷史錯題。Community Cloud 的本機檔案[不保證永久保留](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data)，需要保存時請下載本輪錯題。不同手機或瀏覽器的練習進度不會自動同步。

## 用手機：與電腦連同一個 Wi-Fi

不部署也可使用，但電腦必須持續開機且 app 持續執行。在本資料夾 PowerShell 執行下列命令（使用 8502，避免與一般啟動的 8501 衝突）：

```powershell
.\.venv\Scripts\python.exe -m streamlit run avionics_flashcard_app.py --server.address 0.0.0.0 --server.port 8502
```

另開 PowerShell 執行 `ipconfig`，找實際連線 Wi-Fi 的 IPv4 位址。手機連相同 Wi-Fi，在瀏覽器輸入 `http://電腦的IPv4:8502`；例如 `http://192.168.1.23:8502`，請替換成自己的 IP。手機不能使用電腦的 127.0.0.1，0.0.0.0 也不是手機要開的位址。

Windows 防火牆若詢問 Python 的網路權限，允許目前可信任的私人網路；校園或訪客 Wi-Fi 若隔離裝置，改用可互通的網路或 Community Cloud。此方式不需做路由器埠轉送。監聽位址設定見 [Streamlit 官方設定說明](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)。

## 題庫校訂參考

- 課程工作區的學長期中整理與講義。
- [FAA 航空機體手冊](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_65-15a.pdf)：固定翼的 angle of incidence 是翼弦與機身縱軸的安裝夾角，與 AOA 分開。
- [NASA 飛行動力學符號資料](https://ntrs.nasa.gov/api/citations/19840008144/downloads/19840008144.pdf)：機體速度 u/v/w 與角速度 p/q/r。
- [ICAO upset recovery 資料](https://www.icao.int/sites/default/files/safety/LOCI/AUPRTA/full.html)：升力與重量及載荷因數的基本關係。

## 驗證

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
