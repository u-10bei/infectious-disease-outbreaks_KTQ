
-----

# :hospital: 北九州市の感染症発生動向（定点報告）

[](https://infectious-disease-outbreaks-ktq.streamlit.app/)

[北九州市オープンデータ](https://odcs.bodik.jp/401005/)のウェブサイトから取得した感染症発生動向を可視化するStreamlitアプリケーションです。

## 使用技術

[![Python](https://img.shields.io/badge/Python-3.11-gray?style=for-the-badge&labelColor=blue)](https://docs.python.org/ja/3.11/installing/index.html) 
[![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B?style=for-the-badge)](https://streamlit.io/)


## 目次

1.  [プロジェクトについて](https://www.google.com/search?q=%23%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
2.  [ディレクトリ構成](https://www.google.com/search?q=%23%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E6%A7%8B%E6%88%90)
3.  [ローカルでの実行方法](https://www.google.com/search?q=%23%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%81%A7%E3%81%AE%E5%AE%9F%E8%A1%8C%E6%96%B9%E6%B3%95)

## プロジェクトについて

本プロジェクトは、[北九州市オープンデータ](https://odcs.bodik.jp/401005/)として公開されている[感染症発生動向](https://www.google.com/search?q=https://data.bodik.jp/dataset/401005_kansensyohasseidoko_teitenhokoku/resource/dd3b77f0-05c0-4899-892c-04909fd210e0)のデータを、グラフや表を用いて分かりやすく可視化するためのアプリケーションです。

主な機能：

  * 過去1年間、去年と今年、過去3年間の感染症データをグラフで比較
  * 各感染症の今週、先週、昨年同週の定点当たり患者数を表示

## ディレクトリ構成

```
.
├── streamlit_app.py  # Streamlitアプリケーションのメインスクリプト
├── datas.py          # データ取得・加工用モジュール
└── README.md         # このファイル
```

## ローカルでの実行方法

### 1\. 必要なライブラリのインストール

プロジェクトの実行には、以下のライブラリが必要です。`requirements.txt`を作成し、管理することをお勧めします。

```bash
pip install streamlit pandas requests
```

### 2\. Streamlitアプリケーションの起動

以下のコマンドを実行して、ローカルサーバーでアプリケーションを起動します。

```bash
streamlit run streamlit_app.py
```

コマンド実行後、Webブラウザで指定されたURL（通常は `http://localhost:8501`）にアクセスすると、アプリケーションが表示されます。