from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, Float, Date, Time, BigInteger, ForeignKey, DateTime

DATABSE_URL = "postgresql://postgres:hoge@localhost:5432/keiba"
engine  = create_engine(DATABSE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 原材料
class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True) # 原材料ID
    ingredient_name = Column(String(255), nullable=False) # 原材料名
    supplier = Column(String(255), nullable=False) # 供給業者
    stock_quantity = Column(Float, nullable=False) # 在庫数
    unit = Column(String(50), nullable=False) # 単位

class Sushi(Base):
    __tablename__ = 'sushi'

    sushi_id = Column(Integer, primary_key=True)  # 寿司ごとのID
    creation_date = Column(Date, nullable=False)  # 寿司の作成日
    pallet_id = Column(Integer, ForeignKey('pallet.pallet_id'))  # 搬送パレットID (外部キー)
    pack_id = Column(Integer, ForeignKey('pack.pack_id'))  # パックID (外部キー)

    pallet = relationship("Pallet", back_populates="sushis")  # 搬送パレットとの関連
    pack = relationship("Pack", back_populates="sushis")  # パックとの関連

class SushiIngredients(Base):
    __tablename__ = 'sushi_ingredients'

    sushi_id = Column(Integer, ForeignKey('sushi.sushi_id'), primary_key=True)  # 寿司ID
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)  # 原材料ID
    quantity_used = Column(Float, nullable=False)  # 寿司に使用された原材料の量

    sushi = relationship(Sushi, back_populates="ingredients")
    ingredient = relationship(Ingredient, back_populates="sushis")

class Pallet(Base):
    __tablename__ = 'pallet'

    pallet_id = Column(Integer, primary_key=True)  # パレットごとのID
    transport_date = Column(Date, nullable=False)  # 搬送日

    sushis = relationship("Sushi", back_populates="pallet")  # パレット上の寿司との関連 (12個)

class Pack(Base):
    __tablename__ = 'pack'

    pack_id = Column(Integer, primary_key=True)  # パックごとのID
    shipment_date = Column(Date, nullable=False)  # 出荷日

    sushis = relationship("Sushi", back_populates="pack")  # パックに含まれる寿司との関連 (24個)

# 設備
class Equipment(Base):
    __tablename__ = 'equipments'

    equipment_id = Column(Integer, primary_key=True) # 設備ID
    equipment_name = Column(String(255), nullable=False) # 設備名
    status = Column(String(50), nullable=False)  # 状態（例：稼働中、メンテナンス中など）

# 品質管理
class QualityControl(Base):
    __tablename__ = 'quality_controls'

    quality_id = Column(Integer, primary_key=True) # 品質ID
    product_id = Column(Integer, ForeignKey('products.produ ct_id'), nullable=False) # 製品ID
    inspection_date = Column(Date, nullable=False) # 検査日
    inspection_result = Column(String(255), nullable=False) # 検査結果

    product = relationship("Product")

# 製品
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True) # 製品ID
    product_name = Column(String(255), nullable=False) # 製品名
    # category = Column(String(50), nullable=False) # カテゴリ（例：冷凍、缶詰、瓶詰など）
    expiration_date = Column(Date, nullable=False) # 賞味期限
    unit_cost = Column(Float, nullable=False) # 単位コスト
    storage_conditions = Column(String(255)) # 保存条件

# 3. 製品レシピデータテーブル
class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True) # レシピID
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False) # 製品ID（外部キー：製品データとのリレーション）
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False) # 原材料ID（外部キー：原材料データとのリレーション）
    required_quantity = Column(Float, nullable=False) # 必要量

    product = relationship("Product")
    ingredient = relationship("Ingredient")

# 4. 生産スケジュールデータテーブル
class ProductionSchedule(Base):
    __tablename__ = 'production_schedules'

    schedule_id = Column(Integer, primary_key=True) # スケジュールID
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False) # 製品ID
    start_date = Column(Date, nullable=False) # 生産開始日
    end_date = Column(Date, nullable=False) # 生産終了日
    production_quantity = Column(Integer, nullable=False) # 生産数

    product = relationship("Product")

# 5. 従業員データテーブル
class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True) # 従業員ID
    name = Column(String(255), nullable=False) # 名前
    position = Column(String(100), nullable=False) # 役職
    shift = Column(String(50), nullable=False) # 勤務シフト



