from sqlalchemy import Column, func
from sqlalchemy.sql.sqltypes import TEXT, TIMESTAMP, Integer

from spider.utils.db_adapter import BASE, DBAdapter

db_adapter = DBAdapter(  # nosec
    dotenv_path=".env",
    env_db_host="DB_HOST",  # DB_HOST # SD_DB_HOST # MART_DB_HOST
    env_db_name="DB_NAME",  # DB_NAME # SD_DB_NAME # MART_DB_NAME
    env_db_user="DB_USER",  # DB_USER # SD_DB_USER # MART_DB_USER
    env_db_pass="DB_PASS",  # DB_PASS # SD_DB_PASS # MART_DB_PASS
    db_type="postgresql",
)


class RakutenRecipe(BASE):
    __tablename__ = "rakuten_recipe"
    db_id = Column(Integer, primary_key=True, comment="DBに付与されるID")
    crawled_url = Column(TEXT, nullable=False, comment="参照URL")
    title = Column(TEXT, nullable=False, comment="タイトル")
    serves = Column(TEXT, comment="何人分")
    ingredients = Column(TEXT, comment="材料")
    image_path = Column(TEXT, comment="料理の画像パス")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        comment="作成日時",
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時",
    )

    @staticmethod
    def select_all() -> list[dict[str, str]]:
        """
        レシピ情報をすべて取得
        """
        res = db_adapter.session.query(RakutenRecipe).all()
        return [r.__dict__ for r in res]

    @staticmethod
    def bulk_insert(rakuten_recipe_list: list[dict[str, str]]) -> None:
        """
        レシピ情報をまとめて保存
        """
        rakuten_recipes = [RakutenRecipe(**dc) for dc in rakuten_recipe_list]
        db_adapter.session.bulk_save_objects(
            rakuten_recipes, return_defaults=True
        )
        db_adapter.session.commit()

    @staticmethod
    def bulk_update(rakuten_recipe_list: list[dict[str, str]]) -> None:
        """
        レシピ情報をまとめて更新
        """
        db_adapter.session.bulk_update_mappings(
            RakutenRecipe, rakuten_recipe_list
        )
        db_adapter.session.commit()


class Driver:
    @staticmethod
    def create_tables() -> None:
        """
        テーブルの作成
        """
        db_adapter.make_tables(
            tables=[
                RakutenRecipe,
            ]
        )
