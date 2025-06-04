USE my_database; -- 選擇指定的資料庫

SHOW TABLES; -- 列出所有資料表

DESCRIBE users; -- 查詢表格

SELECT * FROM users; -- 查詢資料內容

DROP TABLE users;	-- 刪除表格

SET SQL_SAFE_UPDATES = 0;	-- 關閉 Worbench 預設模式，沒有關閉就無法使用修改&刪除資料的動作

DELETE FROM `users`;	-- 刪除表格裡所有的資料

SET SQL_SAFE_UPDATES=1; 	-- 開啟 Worbench 預設模式，這樣就不會誤刪資料