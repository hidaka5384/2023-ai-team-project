# YOLOv4

## DB 設計

[DB 設計](https://github.com/dumbled0re/2022-AI-TeamProject/blob/feature/%236_refactor/spider/models.py#L16)

## ディレクトリ構造

```
2022-AI-TeamProject
│    ├── images
│    ├── logs
│    ├── spider
│    │   ├── spiders
│    │   │  └── rakuten_recipe_spider.py : クローラー実行
│    │   ├── utils
│    │   │  ├── constants.py             : 定数定義
│    │   │  ├── db_adapter.py            : DB接続
│    │   │  ├── logger.py                : ログ出力
│    │   │  ├── slack_notify.py          : slack通知
│    │   │  └── spider_utils.py          : スパイダーutilsモジュール
│    │   ├── items.py                    : スパイダーが取得するデータ定義
│    │   ├── middlewares.py              : スパイダーの設定
│    │   ├── models.py                   : DBテーブル定義
│    │   ├── pipelines.py                : DBに保存する処理
│    │   └── settings.py                 : スパイダー全体の設定
│    ├── tests
│    │   ├── data
│    │   │   └── table_operations.py     : テスト用のテーブル作成
│    │   ├── docker
│    │   │   ├── docker-compose.yaml
│    │   │   └── Dockerfile
│    │   ├── train
│    │   ├── val
│    │   └── unittest
│    ├── yolov4
│    └── yolov4-tiny
├── utils.py
├── yolov4-tiny.ipynb
├── yolov4.ipynb
├── .env.sample
├── .flake8
├── .gitattibutes
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile　　　　　　　　　　
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── README.md
├── scrapy.cfg
└── setup.cfg
```

## Git rules

- コミットメッセージは下記の prefix を使用する。[参考 URL](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)
  - feat: 新しい機能追加
  - fix: バグ修正
  - docs: ドキュメント修正
  - style: コードスタイル修正
  - refactor: リファクタリング
  - perf: パフォーマンスチューニング
  - test: テストの追加/修正
  - chore: 基盤の修正、ライブラリの追加/削除

## プッシュ前にやること

```
make pre-commit-check
```

## 環境構築

poetry インストール後 以下実行

```
make install
```

env ファイルコピー 記入

```
cp .env.sample .env
```

## 動作確認(Docker を使う場合)

```
# ビルド
make db_local_build

# テーブル作成
make data_create_table

# テーブル削除
make data_drop_table

# 終了
make db_local_down
```

デフォルトで port = 5432 に postgresql DB が起動する

### 接続情報

```
POSTGRES_HOST=127.0.0.1
POSTGRES_DB=app
POSTGRES_PASSWORD=pass
POSTGRES_USER=postgres
POSTGRES_DOCKER_PORT=5432
```

## 実行

```
# 新規追加
make crawl
```

## YOLOv4 デモ映像

https://user-images.githubusercontent.com/61057861/174428761-1dd8b1db-7ccc-4fb0-8b69-617f17af41b8.mp4

## YOLOv4-tiny デモ映像

https://user-images.githubusercontent.com/61057861/174428771-93adec64-b4bc-4aa6-a941-8700e934869a.mp4
