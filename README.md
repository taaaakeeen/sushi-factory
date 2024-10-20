# sushi-factory

# 漬けマグロの生産工場
漬けマグロの世界的な需要増加により工場を建設することになりました。
★この物語はフィクションです。実在の人物・団体・事件などには、いっさい関係ありません。

# 目次
- 工場レイアウト
- 生産設備
- 工程設計
- データベース設計






# 物流ヤード＃１、冷蔵室＃１、冷凍室＃１
1. 作業者：原材料をコンテナへ積載し、リーダ端末で荷札の情報とコンテナIDを読み取る
2. PC：原材料に仕入IDを付与し、コンテナIDと紐づけて記録
3. コンベア：原材料に応じて冷凍室/冷蔵室へ搬送
4. 冷蔵室：コンテナIDを読み取り、仕入IDの入庫日時を記録
5. 冷凍室：コンテナIDを読み取り、仕入IDの入庫日時を記録
6. 冷凍室：コンテナIDを読み取り、仕入IDの出庫日時を記録->冷蔵室へコンベアで搬送（解凍）

# 物流ヤード＃２、醤油タンク、みりんタンク、酒タンク、米タンク、水タンク、酢タンク
1. 作業者：原材料をタンクへ投入し、リーダ端末で荷札の情報と設備IDを読み取る
2. PC：原材料に仕入IDを付与し、設備IDと紐づけて記録

# まぐろカット
1. まぐろカット：冷蔵室に搬入リクエスト
2. 冷蔵室：仕入日時が古いまぐろを探す
3. 冷蔵室：対象仕入IDを積載したコンテナをコンベアへ搬出
4. 冷蔵室：コンテナIDを読み取り、対象仕入IDの出庫日時を記録
5. まぐろカット：コンテナのIDを読み取る
6. まぐろカット：まぐろの仕入IDを取得
7. まぐろカット：まぐろを加工後、切身ごとにIDを付与してDBに記録。検査機へ搬出
8. 検査：切身ごとに検査を実施。検査結果をDBに記録

# 漬けダレ
1. 生姜おろし：冷蔵室に搬入リクエスト
2. 冷蔵室：仕入日時が古い生姜を探す
3. 冷蔵室：対象仕入IDを積載したコンテナをコンベアへ搬出
4. 冷蔵室：コンテナIDを読み取り、対象仕入IDの出庫日時を記録
5. 生姜おろし：コンテナのIDを読み取る
6. 生姜おろし：生姜の仕入IDを取得
7. 生姜おろし：生姜を加工後、漬けダレタンクへ供給
8. 漬けダレタンク：各原材料の仕入IDを取得
9. 漬けダレタンク：タンク集中管理に供給リクエスト
10. 検査：漬けダレの検査を実施。検査結果をDBに記録

# 漬け
漬け：漬けダレタンクに供給リクエスト




# 工場レイアウト


# 生産設備

## 保管工程（原材料）
### 物流ヤード
### 冷蔵室＃１
### 冷凍室＃１
### コンベア＃１

## タネ工程
### まぐろカット＃１








### まぐろカット＃２
### コンベア＃２

## シャリ工程
### 水タンク＃１
### 水タンク＃２
### 米タンク＃１
### 酢タンク＃１
### 炊飯＃１
### 炊飯＃２
### 炊飯＃３
### コンベア＃３

## 漬けダレ工程
### 醤油タンク＃１
### 酒タンク＃１
### みりんタンク＃１
### 生姜おろし＃１
### 漬けダレタンク＃１

## 漬け工程
### 漬け＃１
### コンベア＃４

## 握り工程
### 寿司職人＃１
### 寿司職人＃２
### コンベア＃５

## パック工程
### パッキング＃１
### 冷蔵室＃２
### 冷凍室＃２
### コンベア＃６


# データベース設計

# measuring_device_locations 測定機器
- location_id
- location_name

# temperature_humidity_logs 温湿度管理
- location_id
- measured_date_time
- temperature
- humidity

# ingredients 原材料
- ingredient_id 原材料ID
- ingredient_name 原材料名

# ingredient_purchases 原材料仕入管理
- purchase_id 仕入ID
- ingredient_id 原材料ID
- purchase_date_time 仕入日時
- supplier_name 仕入先
- quantity 数量
- unit 単位
- container_id コンテナID（醤油、みりん、酒、米、水、酢に関しては設備ID）

# containers コンテナ管理
- container_id コンテナID
- purchase_ids 運搬中の原材料（仕入ID）

# ingredient_frozen_storage_histories 原材料冷凍倉庫管理
- purchase_id 仕入ID
- storage_in_date_time 入庫日時
- storage_out_date_time 出庫日時

# ingredient_cold_storage_histories  原材料冷蔵倉庫管理
- purchase_id 仕入ID
- storage_in_date_time 入庫日時
- storage_out_date_time 出庫日時

# machines 生産設備
- machine_id 設備ID
- machine_mame 設備名

# pallets パレット管理
- pallet_id パレットID
- sushi_ids 運搬中の寿司ID

# tuna_fillets まぐろ切身管理
- tuna_fillet_id まぐろ切身ID
- machine_id 設備ID
- processed_date_time 製造日時
- tuna_purchase_id まぐろ（仕入ID）
- quality 品質 JSONB

# sushi_rices シャリ管理
- sushi_rice_id シャリID
- machine_id 設備ID
- processed_date_time 製造日時
- rice_purchase_id 米（仕入ID）
- water_purchase_id 水（仕入ID）
- vinegar_purchase_id 酢（仕入ID）

# grated_gingers おろし生姜管理
- grated_ginger_id おろし生姜ID
- machine_id 設備ID
- processed_date_time 製造日時
- ginger_purchase_id 生姜（仕入ID）

# sauces 漬けダレ管理
- sauce_id 漬けダレID
- machine_id 設備ID
- processed_date_time 製造日時
- mirin_purchase_id みりん（仕入ID）
- soy_sauce_purchase_id 醤油（仕入ID）
- sake_purchase_id 酒（仕入ID）
- grated_ginger_id おろし生姜ID

# marinated_tuna_fillets 漬け管理
- marinated_tuna_fillet_id 漬けまぐろID
- machine_id 設備ID
- processed_date_time 製造日時
- tuna_fillet_id まぐろ切身ID
- sauce_id 漬けダレID

# sushis 寿司管理
- sushi_id 寿司ID
- machine_id 設備ID
- processed_date_time 製造日時
- sushi_rice_id シャリID
- marinated_tuna_fillet_id 漬けまぐろID
- pallet_id パレットID
- loaded_date_time パレット積載日時
- sushi_pack_id 寿司パックID

# sushi_packs パッキング管理
- sushi_pack_id 寿司パックID
- machine_id 設備ID
- processed_date_time 製造日時

# ingredient_frozen_storage_histories 寿司冷凍倉庫管理
- sushi_id 寿司ID
- storage_in_date_time 入庫日時
- storage_out_date_time 出庫日時

# ingredient_cold_storage_histories  寿司冷蔵倉庫管理
- sushi_id 寿司ID
- storage_in_date_time 入庫日時
- storage_out_date_time 出庫日時

