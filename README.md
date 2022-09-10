# Prosody Controllable Text-To-Speech Model for Russian (FastPitch and WaveGlow with post-processing)
The repository provides a theoretical description of the work and the relevant code with instructions for generating phrases with a specific intonational construction (as per the classification by E.A. Bryzgunova) using pre-trained Russian FastPitch and WaveGlow models and post-processing.



Table Of Contents: 

* [About the work](#about-the-work)
   * [Training](#training)
   * [Data](#data)
   * [Post-processing](#post-processing)
   * [Results](#results)

* [How to run the code](#how-to-run-the-code)

* [License and Copyright](#license-and-copyright)

* [About me](#about-me)

---------------------------------------------------------------------
# About the work
The full text (in Russian) can be found by the [following link](https://drive.google.com/file/d/1L4B0SCs-klUOENGMS--M5r3KUi4Bvqjr/view?usp=sharing).

To do a prosody controllable TTS model for Russian, the FastPitch and WaveGlow models were trained on Russian data. The next step was writing a post-processing script which creates one of 6 intonational constructions (IC) described by Elena Bryzgunova and used in Russian academic linguistics society.

## Training

One can get all detailed information about *FastPitch* model on [the official website](https://fastpitch.github.io/) or [GitHub repo](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch). Details about the *WaveGlow* model is on the [official GitHub repo](https://github.com/NVIDIA/waveglow).

### FastPitch

The FastPitch model was trained on [RUSLAN](https://ruslan-corpus.github.io/) dataset with following hyperparameters: GPU numbers = 4, batch size = 16, gradient accumulation = 4, learning rate = 0.1. The AMP (Automatic Mixed Precision) mechanism have not used. 1000 epoches have been trained. The loss function values according to the number of trained epochs and the body on which the model was trained can be found below. The data on the LJSpeech case is taken from [official FastPitch GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) to compare the results.

| Loss (Model/Epoch)    |    50 |   250 |   500 |   750 |  1000 |
|:----------------------|------:|------:|------:|------:|------:|
| RUSLAN (russian)      | 2.79  |  2.51 |  2.43 |  2.40 |  2.38 |
| LJSpeech (english)    | 3.37  |  2.88 |  2.78 |  2.71 |  2.68 |

To load Russian pre-trained FastPitch model:

   ```bash
   bash scripts/download_fastpitch.sh
   ```

### WaveGlow

The WaveGlow model was trained on [RUSLAN](https://ruslan-corpus.github.io/) dataset using 4 GPU with basic hyperparameters: batch size = 4, segment length = 8000. The AMP (Automatic Mixed Precision) mechanism have not used. 550 epoches have been trained. The loss function values according to the number of trained epochs and the body on which the model was trained can be found below. The data on the LJSpeech case is taken from [official WaveGlow GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) to compare the results.

| Loss (Model/Epoch)    |    1  |   250 |   500  |
|:----------------------|------:|------:|-------:|
| RUSLAN (russian)      | -4.03 | -6.91 |  -7.03 |
| LJSpeech (english)    | -4.46 | -5.93 |  -5.98 |

To load Russian pre-trained WaveGlow model:

   ```bash
   bash scripts/download_waveglow.sh
   ```

## Data

The dataset [Ruslan](https://ruslan-corpus.github.io/) was used to train TTS models. Text transcripts are stored in the folder `filelists`. The lists of all wav files and its' transcripts divided into training and validation samples can be found in `ruslan_train.txt` and `ruslan_val.txt` files. There are the same information with an additional reference to the pitch files (which can be obtained after data preprocessing) in `ruslan_pitch_train.txt` and `ruslan_pitch_val.txt` files. The `short_ruslan_train.txt`, `short_ruslan_val.txt`, `short_pitch_ruslan_train.txt` and `short_pitch_ruslan_val.txt` files contain cuted audio lists with transcripts (all those audio whose transcript length is less than 200 characters) for faster training of the model.

Download audio-data:

   ```bash
   bash scripts/download_dataset.sh
   ```

Data pre-processing, pitch and mel-spectrogram calculation:

   ```bash
   bash scripts/prepare_dataset.sh
   ```

## Post-processing
### About intonational constructions
IC is a minimal intonational unit that distinguishes the phrase meaning. Traditionally, there are 6 intonation constructions, differing in the pitch movement on the five phrase parts: beginning, pre-accent, accent syllable, post-accent and final. Below one can find short descriptions with pictures showing different ICs (the accent syllable is highlighted with dotted lines).
1. **The 1st IC**: a smoothly descending pitch movement. It is typical for completed narrative sentence 
      
<img src="https://drive.google.com/uc?export=view&id=1ArYB6yaymZ1iO2Cxsctg7IWEZAzwe0X3" width="500">

2. **The 2nd IC**: a sharp downward pitch movement with a slight rising in the pre-accent part. It is typical for interrogative sentences with a question word, appeals and expressions of will, and completed narrative sentences with a brighter accent (compared to IK-1). 
      
<img src="https://drive.google.com/uc?export=view&id=1xaYgFu4osb-3NJfVsggfqr7GtqRtBGOn" width="500">

3. **The 3rd IC**: an ascending tone followed by a fall. Is used in general question, enumeration, incompleteness.
      
<img src="https://drive.google.com/uc?export=view&id=1lEcoPwMR2N2-joX7Bkl4XMZelX9UBLyT" width="500">

4. **The 4th IC**: a descending-ascending pitch. It is used in incomplete interrogative sentences with a comparative union and enumerations (like IC-3).
      
<img src="https://drive.google.com/uc?export=view&id=1aTfT7x6brYnKdaaIDe3oJG6JYNW-pFqf" width="500">

5. **The 5th IC**: has two accents – the pitch rises on the first accent, and decreases on the second accent. It is typical for sentences that convey a bright degree of expression of any feature.
      
<img src="https://drive.google.com/uc?export=view&id=17fSZkuRVn-cQ6HJppcHzD-Bu95fGR-6A" width="500">

6. **The 6th IC**: an rising tone, followed by keeping the tone at a high level. Is used in evaluative exclamations and expressions of bewilderment.
      
<img src="https://drive.google.com/uc?export=view&id=1jSn9HmDUNybnd_U79oGUBwmXi-hfZUrP" width="500">

### About the post-processing code

The post-processing code can be found in jupyter notebook `notebooks/FastPitch_voice_modification_custom.ipynb`. The algorithm averages the originally generated intonation by a factor of 1.5 (the value was set experimentally) in order to smooth the synthesized accents. Also, the lower and upper boundaries of the pitch were set, 80 and 300 Hz, below and above which the pitch should not change. These values were chosen based on the speaker's average pitch (about 110 Hz). Then for each sound a certain level of pitch is set, according to the given intonational contour. The algorithm determines all the desired intervals for each type of IC (beginning, pre-accent, accent, post-accent and final) and sets the desired pitch values on them by subtracting or adding a certain value to the value that is on the sound after averaging.


## Results
Examples of generating phrases with post-processing based on Bryzgunova's intonation constructions and without it are in the `audio` folder. A preference test was conducted: 300 people listened to each received example pair (generating by TTS without post-processing & with post-processing) and answered the question "which audio sounds more natural?" (using [Yandex Toloka](https://toloka.yandex.ru/)). The test results are below:


|     Number of votes     |  IC-1 |  IC-2 | IC-3  |  IC-4 |  IC-5 |  IC-6 |
|:------------------------|------:|------:|------:|------:|------:|------:|
| without post-processing | 1058  |  1036 |  676  |  599  |  891  | 1005  |
| with post-processing    | 442   |  464  |  824  |  901  |  609  |  495  |

As can be seen, in most cases users preferred intonation without additional modification, except for entries with IC-3 and IC-4. This can be explained by the fact that these are rising intonations in question sentences, which the speech synthesizer itself does not handle well - most often a descending or flat, affirmative tone is generated in questions, which seems inappropriate to the native speaker for the context. FastPitch generates affirmative sentences plausibly, which is what the survey results show. In addition, it can be noted that among all the affirmative statements, IC-5 has the smallest preference difference: 891 for the original versus 609 for the modification. This may be due to the fact that this IC performs more of an emotional function than a syntactic one, unlike IC-1 and IC-2, and the model also does emotional coloring poorly. However, this is not observed with IC-6, which is close to IC-5 in meaning.


# How to run the code

### Requirements

Technical requirements for launching speech generation or training a FastPitch model: 
* [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker)
* [PyTorch 21.05-py3 NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) container or newer
* supported GPUs: [NVIDIA Volta architecture](https://www.nvidia.com/en-us/data-center/volta-gpu-architecture/); [NVIDIA Turing architecture](https://www.nvidia.com/ru-ru/geforce/turing/); [NVIDIA Ampere architecture](https://www.nvidia.com/en-us/data-center/ampere-architecture/)

### Instructions for generating phrases with a specified intonation construction

In order to generate a phrase with the necessary specified IC (intonation construction), you need to follow several steps:

1. Clone the repository.
   ```bash
   git clone https://github.com/safonovanastya/Russian_FastPitch_modified_intonation.git
   cd Russian_FastPitch_modified_intonation/
   ```

2. Build and run the FastPitch PyTorch NGC container.

   ```bash
   bash scripts/docker/build.sh
   bash scripts/docker/interactive.sh
   ```

3. Download pre-trained FastPitch и WaveGlow models.

   ```bash
   bash scripts/download_fastpitch.sh
   bash scripts/download_waveglow.sh
   ```
   
4. Write in `phrases/text.txt` file a phrase, specifying the accents in the words (with the + symbol) and the phrasal accent (with the ++ symbol). Please note that for all IC, except IC-5, you must specify one phrasal accent. For the IC-5, you must indicate two phrasal accents.

5. Start the generation process by setting an additional parameter `--pitch-transform-custom` with the IR number.

   ```bash
   python ../inference.py --cuda --fastpitch ../output_fastpitch/FastPitch_checkpoint_1000.pt --waveglow ../output_waveglow/checkpoint_WaveGlow_450.pt --wn-channels 256 --p-arpabet 0.0 -i phrases/text.txt -o ../output/modified_ik4/ --pitch-transform-custom 4
   ```
   
   Or run the code from jupyter notebook `notebooks/FastPitch_voice_modification_custom.ipynb`

Examples of generating phrases based on Bryzgunova's intonation constructions can be found in the folder `audio`.

### Fine-tuning

One can fine-tune pre-trained russian models. The full instructions for training models could be found in [the official GitHub repository](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch). 



# License and Copyright
All the rights to the FastPitch and WaveGlow code belong to the [respective authors from NVIDIA](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch). Minimal changes were made to adapt the existing code to the Russian data by me.
All the rights to the data belong to the respective authors: [RUSLAN](https://ruslan-corpus.github.io/)

Everything else (including the post-processing script) is licensed under the [MIT license](https://github.com/ftyers/fieldasr/blob/main/LICENSE.md)

# About me
Anastasia Safonova, an.saphonova@gmail.com 

The project was made like a graduate project (NRU HSE, "Computational Linguistics" master program) under the supervision of Mikhail Kudinov.

2022
