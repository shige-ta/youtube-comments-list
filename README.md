# youtube-comments-list

指定のyoutubeチャンネルのコメントリスト(返信含め)を取得し、csvに吐き出すスクリプト


要設定
https://www.youtube.com/channel/~~~ の ~~~ を入力
```
channelId = "<チャンネルID>"
```
GCPでプロジェクトを作成し、YouTube Data API v3 を有効化し、APIキーを発行しそのキーを入力
```
API_KEY = "<APIキー>"
```

実行
```
python youtube-comments-list.py
```

Excelを立ち上げ、データタブで「テキストまたはCSVから」で吐き出したCSVをインポートして変換
