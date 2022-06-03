# Модель генерации речи для русского языка с возможностью контроля просодии

Репозиторий предоставляет код и инструкцию по генерации фраз с заданной интонационной конструкцией по Е.А. Брызгуновой на предобученных русских моделях FastPitch и WaveGlow.

Оригинальный код FastPitch, созданный разработчиками NVIDIA: https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch

## Технические требования

Технические требования для запуска генерации речи или обучения FastPitch: 
* Nvidia докер с PyTorch 21.05-py3 NGC контейнером в версии 21.05-py3 или более новой
* Видеокарты с микроархитектурой Nvidia Volta, Turing или Ampere. 

## Инструкция по генерации фраз с заданной ИК

Для того, чтобы сгенерировать фразу с необходимой интонационной конструкцией, нужно выполнить несколько шагов:

1. Склонировать репозиторий.
   ```bash
   git clone https://github.com/safonovanastya/Russian_FastPitch_modified_intonation.git
   cd Russian_FastPitch_modified_intonation/
   ```

2. Построить и запустить контейнер FastPitch PyTorch NGC.

   ```bash
   bash scripts/docker/build.sh
   bash scripts/docker/interactive.sh
   ```

3. Скачать предобученные модели FastPitch и WaveGlow.

   ```bash
   bash scripts/download_fastpitch.sh
   bash scripts/download_waveglow.sh
   ```
   
4. Записать в файл phrases/text.txt необходимую для озвучивания фразу, указав ударения в словах (символом +) и фразовый акцент (символом ++). Обратите внимание, что для всех ИК, кроме ИК-5, необходимо указать один фразовый акцент. Для ИК-5 необходимо указать два фразовых акцента

5. Запустить процесс генерации, указав дополнительный параметр `--pitch-transform-custom` с номером ИК.

   ```bash
   python ../inference.py --cuda --fastpitch ../output_fastpitch/FastPitch_checkpoint_1000.pt --waveglow ../output_waveglow/checkpoint_WaveGlow_450.pt --wn-channels 256 --p-arpabet 0.0 -i phrases/text.txt -o ../output/modified_ik4/ --pitch-transform-custom 4
   ```
   
   Либо воспользоваться кодом в тетрадке jupyter notebook `notebooks/FastPitch_voice_modification_custom.ipynb`


## Предобученные модели
### FastPitch

Модель FastPitch обучалась на аудио корпусе [RUSLAN](https://ruslan-corpus.github.io/) со следующими гиперпараметрами: количество GPU = 4, размер мини бачта (batch size) = 16, градиент аккумуляции (gradient accumulation) = 4, (learning rate) = 0.1. Механизм AMP (Automatic Mixed Precision) не использовался. Всего было обучено 1000 эпох. Ниже приведены значения функции потерь в соответствии с количеством обученных эпох и корпусом, на котором была обучена модель. Данные по корпусу LJSpeech взяты с [официального GitHub проекта](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) для сравнения результатов.

| Loss (Model/Epoch)    |    50 |   250 |   500 |   750 |  1000 |
|:----------------------|------:|------:|------:|------:|------:|
| RUSLAN (русский)      | 2.79  |  2.51 |  2.43 |  2.40 |  2.38 |
| LJSpeech (английский) | 3.37  |  2.88 |  2.78 |  2.71 |  2.68 |

Загрузить предобученную модель FastPitch:

   ```bash
   bash scripts/download_fastpitch.sh
   ```

### WaveGlow

Модель WaveGlow обучалась на аудио корпусе [RUSLAN](https://ruslan-corpus.github.io/) на 4 видеокартах и с базовыми гиперпараметрами: размер мини бачта (batch size) = 4, длина сегмента (segment length) = 8000. Механизм AMP (Automatic Mixed Precision) не использовался. Всего было обучено 550 эпох. Ниже приведены значения функции потерь в соответствии с количеством обученных эпох и корпусом, на котором была обучена модель. Данные по корпусу LJSpeech взяты с [официального GitHub проекта](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) для сравнения результатов.

| Loss (Model/Epoch)    |    1  |   250 |   500  |
|:----------------------|------:|------:|-------:|
| RUSLAN (русский)      | -4.03 | -6.91 |  -7.03 |
| LJSpeech (английский) | -4.46 | -5.93 |  -5.98 |

Загрузить предобученную модель WaveGlow:

   ```bash
   bash scripts/download_waveglow.sh
   ```


## Данные

Для работы использовался датасет [Ruslan](https://ruslan-corpus.github.io/). Текстовые расшифровки хранятся в папке `filelists`. В файлах `ruslan_train.txt` и `ruslan_val.txt` находится полный список аудио с расшифровками, разбитый на выборки для обучения и валидации, а в файлах `ruslan_pitch_train.txt` и `ruslan_pitch_val.txt` те же данные, только с дополнительным указанием на файлы с ЧОТ (которые можно получить после предобработки данных). В файлах `short_ruslan_train.txt`, `short_ruslan_val.txt`, `short_pitch_ruslan_train.txt` и `short_pitch_ruslan_val.txt` находятся сокращенные списки аудио с расшифровками (все те аудио, чья длина расшифровки менее 200 символов) для более быстрого обучения модели.

Скачать аудио данные:

   ```bash
   bash scripts/download_dataset.sh
   ```

Предобработка данных, рассчет ЧОТ и mel-спектрограмм:

   ```bash
   bash scripts/prepare_dataset.sh
   ```

## Fine tuning моделей

Возможно дообучение и fine tuning предобученных русских моделей. Ознакомиться с полной инструкцией по обучению моделей можно на [официальном GitHub репозитории](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch). 





## Обратная связь
Автор кода -- Анастасия Сафонова, an.saphonova@gmail.com
2022 год
