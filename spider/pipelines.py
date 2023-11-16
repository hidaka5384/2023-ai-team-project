import time

from scrapy import Spider

from spider.items import RakutenItem
from spider.models import Driver, RakutenRecipe
from spider.utils.constants import LOG_FILE_PATH
from spider.utils.logger import get_logger
from spider.utils.slack_notify import SlackNotify
from spider.utils.spider_utils import SpiderUtils

logger = get_logger(__name__, LOG_FILE_PATH)


class SpiderPipeline:
    BULK_SIZE = 1000

    def __init__(self) -> None:
        self._rakuten_recipe = RakutenRecipe()
        self._db_driver = Driver()
        self._spider_utils = SpiderUtils()
        self._slack = SlackNotify()
        self._recipes: list[dict[str, str]] = list()
        self._num_recipes: int = 0

    def open_spider(self, spider: Spider) -> None:
        """スパイダーの起動前に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """
        self.start_time = time.time()
        self._db_driver.create_tables()
        self._slack.slack_notify("[楽天レシピ] 収集処理を開始")
        spider.start_urls = self._spider_utils.get_start_urls()

    def process_item(self, item: RakutenItem, spider: Spider) -> RakutenItem:
        """スパイダーからレシピ情報をDBに保存

        Args:
            item (RakutenItem): スパイダーから返されるアイテムオブジェクト
            spider (Spider): スパイダークラスのインスタンス
        Returns:
            item: DBに保存するアイテムオブジェクト
        """
        try:
            if isinstance(item, RakutenItem):
                recipe_rows = dict(item)
                self._recipes.append(recipe_rows)
                if len(self._recipes) == self.BULK_SIZE:
                    logger.info(f"レシピ情報を{self.BULK_SIZE}件、DBに保存しました")
                    self._rakuten_recipe.bulk_insert(self._recipes)
                    self._num_recipes += self.BULK_SIZE
                    self._recipes = list()
                return item
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

    def close_spider(self, spider: Spider) -> None:
        """スパイダー終了時に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """

        try:
            if self._recipes:
                self._rakuten_recipe.bulk_insert(self._recipes)
                self._num_recipes += len(self._recipes)
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

        elapsed_time = int(time.time() - self.start_time)

        elapsed_hour = elapsed_time // 3600
        elapsed_minute = (elapsed_time % 3600) // 60
        elapsed_second = elapsed_time % 3600 % 60

        elapsed_time_format = f"{str(elapsed_hour).zfill(2)}:{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}"

        logger.info(
            f"[楽天レシピ] 追加件数{self._num_recipes}件 収集時間: {elapsed_time_format}"
        )
        self._slack.slack_notify(
            f"[楽天レシピ] 追加件数{self._num_recipes}件 収集時間: {elapsed_time_format}"
        )
