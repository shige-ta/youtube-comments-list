import requests
import urllib.parse as parse
import csv
import pickle
from datetime import datetime, timedelta

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

# チャンネル情報を読み込む
try:
    with open('channel_info.pickle', 'rb') as f:
        channel_info = pickle.load(f)
except FileNotFoundError:
    channel_info = {}

# チャンネル情報を更新
if channelId not in channel_info:
    channel_info[channelId] = {'last_run_date': datetime(2000, 1, 1)}

last_run_date = datetime.combine(channel_info[channelId]['last_run_date'], datetime.min.time())
current_run_date = datetime.now().date()
channel_info[channelId]['last_run_date'] = current_run_date

# チャンネル情報を保存
with open('channel_info.pickle', 'wb') as f:
    pickle.dump(channel_info, f)

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
        published_at = datetime.strptime(top_level_comment['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

        # 前回の実行日以降のコメントのみ処理
        if published_at > last_run_date:
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
                published_at = datetime.strptime(reply_comment['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

                # 前回の実行日以降の返信のみ処理
                if published_at > last_run_date:
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

# CSVファイル名に取得日時の範囲を含める
csv_filename = f"youtube-comments-list_{channelId}_{last_run_date.strftime('%Y%m%d')}-{current_run_date.strftime('%Y%m%d')}.csv"

# CSVで出力
f = open(csv_filename, 'w', newline='', encoding='UTF-8')
writer = csv.writer(f)
writer.writerows(items_output)
f.close()
