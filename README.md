# NoSQL_Alex_Fomenko_last_hw_module_3
Итоговое домашнее задание по курсу NoSQL (3 модуль)

---

## Запуск кластера
```bash
chmod +x ./init_mongo/init_shards.sh
docker compose up -d
```

---

## Запусе консольного приложения
```bash
pip install pymongo
python3 console_app.py
```

---

## Результаты нагрузочного тестирования
result_no_shard.txt - для не шардированного кластера </br>
result_shard.txt - для шардированного кластера
