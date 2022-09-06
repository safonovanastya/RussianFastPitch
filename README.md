# Prosody Controllable Text-To-Speech Model for Russian (FastPitch and WaveGlow with post-processing)
The repository provides a theoretical description of the work and the following code with instructions for generating phrases with a given intonation construction by E.A. Bryzgunova on pre-trained Russian FastPitch and WaveGlow models.



Table Of Contents: 

[About the work](#about-the-work)

[How to run the code](#how-to-run-the-code)

[License and Copyright](#license-and-copyright)

[About me](#about-me)

---------------------------------------------------------------------
# About the work


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


### Training
#### FastPitch

The FastPitch model was trained on [RUSLAN](https://ruslan-corpus.github.io/) dataset with following hyperparameters: GPU numbers = 4, batch size = 16, gradient accumulation = 4, learning rate = 0.1. The AMP (Automatic Mixed Precision) mechanism have not used. 1000 epoches have been trained. The loss function values according to the number of trained epochs and the body on which the model was trained can be found below. The data on the LJSpeech case is taken from [official FastPitch GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) to compare the results.

| Loss (Model/Epoch)    |    50 |   250 |   500 |   750 |  1000 |
|:----------------------|------:|------:|------:|------:|------:|
| RUSLAN (russian)      | 2.79  |  2.51 |  2.43 |  2.40 |  2.38 |
| LJSpeech (english)    | 3.37  |  2.88 |  2.78 |  2.71 |  2.68 |

To load pre-trained FastPitch model:

   ```bash
   bash scripts/download_fastpitch.sh
   ```

#### WaveGlow

The WaveGlow model was trained on [RUSLAN](https://ruslan-corpus.github.io/) dataset using 4 GPU with basic hyperparameters: batch size = 4, segment length = 8000. The AMP (Automatic Mixed Precision) mechanism have not used. 550 epoches have been trained. The loss function values according to the number of trained epochs and the body on which the model was trained can be found below. The data on the LJSpeech case is taken from [official WaveGlow GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch) to compare the results.

| Loss (Model/Epoch)    |    1  |   250 |   500  |
|:----------------------|------:|------:|-------:|
| RUSLAN (russian)      | -4.03 | -6.91 |  -7.03 |
| LJSpeech (english)    | -4.46 | -5.93 |  -5.98 |

To load pre-trained WaveGlow model:

   ```bash
   bash scripts/download_waveglow.sh
   ```


### Data

The dataset [Ruslan](https://ruslan-corpus.github.io/) was used to train TTS models. Text transcripts are stored in the folder `filelists`. In `ruslan_train.txt` and `ruslan_val.txt` files can be find lists of all wav files and its' transcripts divided into training and validation samples. There are the same information with an additional reference to the c pitch files (which can be obtained after data preprocessing) in `ruslan_pitch_train.txt` and `ruslan_pitch_val.txt` files. The `short_ruslan_train.txt`, `short_ruslan_val.txt`, `short_pitch_ruslan_train.txt` and `short_pitch_ruslan_val.txt` files contain cuted audio lists with transcripts (all those audio whose transcript length is less than 200 characters) for faster training of the model.

Download audio-data:

   ```bash
   bash scripts/download_dataset.sh
   ```

Data pre-processing, pitch and mel-spectrogram calculation:

   ```bash
   bash scripts/prepare_dataset.sh
   ```

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
