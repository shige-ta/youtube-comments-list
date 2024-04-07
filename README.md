# youtube-comments-list

指定のyoutubeチャンネルのコメントリスト(返信含め)を取得し、csvに吐き出すスクリプト


要設定
```
channelId = "<チャンネルID>"　<- https://www.youtube.com/channel/~~~ の ~~~ を入力
API_KEY = "<APIキー>" <- GCPでプロジェクトを作成し、YouTube Data API v3 を有効化し、APIキーを発行しそのキーを入力
```

実行
```
python youtube-comments-list.py
```

Excelを立ち上げ、データタブで「テキストまたはCSVから」で吐き出したCSVをインポートして変換
