# Формулировка задания
В папках с данными лежат файлы с логами работы некоторой программы, которая скачивает данные RNA-seq. Необходимо написать скрипт, который для каждой папки выведет список образцов которые не загрузились. 
Скачиваемые файлы имеют название, наподобие SRR5117471.fastq.gz или SRR6384380_1.fastq.gz (для некоторых образцов существует два файла). Список не загрузившихся образцов вывести на экран в формате ниже:

```
data_1:
SRR5117471
SRR6384380
data_2:
SRR6384382
```

Если для образца существует два файла, то вывести, если хотя бы один из файлов не загрузился. То есть, если не загрузился SRR6384380_1 или SRR6384380_2, вывести SRR6384380.
Скрипт можно написать с помощью python или в командной строке linux. В качестве результата выполнения необходим код скрипта.

# Решение
Скрипт `get_not_downloaded_files.py` запускается со следующим интерфейсом:

```
usage: get_not_downloaded_files.py [-h] [--strict] mask [mask ...]

positional arguments:
  mask        Folders that contains `data_{1,2,3,4,5}` subfolders

optional arguments:
  -h, --help  show this help message and exit
  --strict    Whether to fail on file processing errors
```

Пример запуска:

```bash
./get_not_downloaded_files.py data_1/report_1.txt
# data_1

./get_not_downloaded_files.py data_?/report_?.txt
# data_1
# data_2
# data_3
SRR5633034 
SRR5633035 
...
```

Простая проверка на разумность выдаваемого результата:

```bash
grep 'not complete' data_?/report_?.txt | wc -l
362
./get_not_downloaded_files.py data_?/report_?.txt | wc -l
355
```

Т.е. строчек с `not complete` чуть больше, чем файлов, найденных скриптом -- что логично, ведь это значило бы что какие-то файлы не скачались несколько раз.
