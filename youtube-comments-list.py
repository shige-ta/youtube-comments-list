import requests
import urllib.parse as parse
import csv

API_KEY = ""
URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
nextPageToken = ''
item_count = 0
items_output = [
    ['videoId'] + ['textDisplay'] + ['textOriginal'] + ['authorDisplayName'] + ['authorProfileImageUrl'] +
    ['authorChannelUrl'] + ['authorChannelId'] + ['canRate'] + ['viewerRating'] + ['likeCount'] +
    ['publishedAt'] + ['updatedAt'] + ['replyCount']
]

# パラメータ設定
channelId = ""
exe_num = 100

for i in range(exe_num):
    # APIパラメータセット
    param = {
        'key': API_KEY,
        'part': 'snippet,replies',
        'allThreadsRelatedToChannelId': channelId,
        'maxResults': '100',
        'moderationStatus': 'published',
        'pageToken': nextPageToken,
        'textFormat': 'plainText',
    }

    # リクエストURL作成
    target_url = URL_HEAD + (parse.urlencode(param))

    # データ取得
    res = requests.get(target_url).json()
    print(res)

    # 件数
    item_count += len(res['items'])
    print(str(item_count) + "件")

    # コメント情報を変数に格納
    for item in res['items']:
        # トップレベルのコメント情報を取得
        top_level_comment = item['snippet']['topLevelComment']['snippet']
        items_output.append(
            [str(top_level_comment['videoId'])] +
            [str(top_level_comment['textDisplay'].replace('\n', ''))] +
            [str(top_level_comment['textOriginal'])] +
            [str(top_level_comment['authorDisplayName'])] +
            [str(top_level_comment['authorProfileImageUrl'])] +
            [str(top_level_comment['authorChannelUrl'])] +
            [str(top_level_comment['authorChannelId']['value'])] +
            [str(top_level_comment['canRate'])] +
            [str(top_level_comment['viewerRating'])] +
            [str(top_level_comment['likeCount'])] +
            [str(top_level_comment['publishedAt'])] +
            [str(top_level_comment['updatedAt'])] +
            [str(item['snippet']['totalReplyCount'])]
        )

        # 返信情報を取得
        if 'replies' in item:
            for reply in item['replies']['comments']:
                reply_comment = reply['snippet']
                items_output.append(
                    [str(reply_comment['videoId'])] +
                    [str(reply_comment['textDisplay'].replace('\n', ''))] +
                    [str(reply_comment['textOriginal'])] +
                    [str(reply_comment['authorDisplayName'])] +
                    [str(reply_comment['authorProfileImageUrl'])] +
                    [str(reply_comment['authorChannelUrl'])] +
                    [str(reply_comment['authorChannelId']['value'])] +
                    [str(reply_comment['canRate'])] +
                    [str(reply_comment['viewerRating'])] +
                    [str(reply_comment['likeCount'])] +
                    [str(reply_comment['publishedAt'])] +
                    [str(reply_comment['updatedAt'])] +
                    ['0']  # 返信の場合は0を設定
                )

    # nextPageTokenがなくなったら処理ストップ
    if 'nextPageToken' in res:
        nextPageToken = res['nextPageToken']
    else:
        break

# CSVで出力
f = open('youtube-comments-list.csv', 'w', newline='', encoding='UTF-8')
writer = csv.writer(f)
writer.writerows(items_output)
f.close()
