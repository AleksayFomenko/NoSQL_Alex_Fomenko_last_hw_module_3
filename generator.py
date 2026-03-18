import matplotlib.pyplot as plt
import numpy as np

# Данные
labels = ['Without Sharding', 'With Sharding']
read_avg = [242.21, 250.47]
update_avg = [414.80, 548.42]
read_99 = [306, 365]
update_99 = [1575, 1736]
throughput = [3007.07, 2476.78]

x = np.arange(len(labels))  # позиции для группировки
width = 0.2

fig, ax = plt.subplots(figsize=(12,6))

# Построение столбцов для latency
ax.bar(x - width*1.5, read_avg, width, label='Read Avg Latency (µs)', color='#FFB347')
ax.bar(x - width/2, update_avg, width, label='Update Avg Latency (µs)', color='#87CEEB')
ax.bar(x + width/2, read_99, width, label='Read 99th Percentile (µs)', color='#FF7F50')
ax.bar(x + width*1.5, update_99, width, label='Update 99th Percentile (µs)', color='#1E90FF')

# Настройки осей и заголовков
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Latency (µs)')
ax.set_title('YCSB MongoDB: Сравнение метрик с шардингом и без')
ax.legend(loc='upper left')
'''
# Вторая ось для Throughput
ax2 = ax.twinx()
ax2.plot(x, throughput, color='green', marker='o', linestyle='--', label='Throughput (ops/sec)')
ax2.set_ylabel('Throughput (ops/sec)')
ax2.legend(loc='upper right')
'''
plt.tight_layout()
plt.show()
