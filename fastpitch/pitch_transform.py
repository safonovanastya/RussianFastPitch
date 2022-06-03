import torch
import numpy as np


def is_sound(symb):
    return (ord('а') <= ord(symb) <= ord('ё')) or (ord('А') <= ord(symb) <= ord('Ё'))


def pitch_transform_custom(pitch, pitch_lens, text, ik_index):
    print(text[0])
    accent = text[0].find('++') - 1
    second_accent = text[0].rfind('++') - 1
    scale = 20
    phrase_pitch = pitch[0]
    average = torch.median(phrase_pitch)
    print(average)
    pitch[0] = (pitch[0] - average) / 1.5 + average
    smoothed_values = []
    for i in range(len(text[0])):
        new_value = (pitch[0][0,max(0, i - 1)] + pitch[0][0,i] + pitch[0][0,min(i, len(text[0]) - 1)]) / 3
        smoothed_values.append(new_value)
        
    for i in range(len(text[0])):
        pitch[0][0,i] = smoothed_values[i]
    
    low_border, upper_border = 80, 300
    print(list(zip(pitch[0][0,:].cpu().detach().numpy(), text[0])))

    
    pitch_change = {
        1: {
            'beginning': 0, 
            'before': [0, 0, -.2 * scale], 
            'accent': -.5 * scale, 
            'after': [-1 * scale, -1 * scale], 
            'end': 0
        },
        2: {
            'beginning': 0, 
            'before': [0, 1 * scale, 1.5 * scale], 
            'accent': -1 * scale, 
            'after': [-0.5 * scale, -0.5 * scale], 
            'end': -0.5 * scale,
        },
        3: {
            'beginning': 0, 
            'before': [-1 * scale, -1 * scale, 2 * scale], 
            'accent': 2 * scale, 
            'after': [1 * scale, 1 * scale], 
            'end': 0,
        },
        4: {
            'beginning': 0, 
            'before': [scale, scale, -1.5 * scale], 
            'accent': -1.5 * scale, 
            'after': [1.5 * scale, 1.5 * scale], 
            'end': 0,
        },
        5: {
            'beginning': 0, 
            'before': [0, 0, 2 * scale], 
            'accent_1': 3 * scale, 
            'accent_2': -1 * scale, 
            'after': [0 * scale, 0 * scale], 
            'end': 0,
        },
        6: {
            'beginning': 0, 
            'before': [0, - scale, scale], 
            'accent': 2.5 * scale, 
            'after': [2 * scale, 2 * scale], 
            'end': 2 * scale,
        }
    }
    
    if accent == second_accent:
        if ik_index == 5:
            print('Этот тип интонационной конструкции подразумевает один акцент. Пожалуйста, поставьте один акцент во фразе.')
        
        pitch[0][0, accent] += pitch_change[ik_index]['accent']

        sound_number = 0
        for i in range(accent - 1, -1, -1):
            if sound_number <= 2:
                pitch[0][0, i] += pitch_change[ik_index]['before'][2 - sound_number]
                if is_sound(text[0][i]):
                    sound_number += 1
            else:
                pitch[0][0, i] += pitch_change[ik_index]['beginning']
        sound_number = 0  
        for i in range(accent + 1, len(text[0])):
            if sound_number <= 1:
                pitch[0][0, i] += pitch_change[ik_index]['after'][sound_number]
                if is_sound(text[0][i]):
                    sound_number += 1
            else:
                pitch[0][0, i] += pitch_change[ik_index]['end']
        for i in range(len(text[0])):
            pitch[0][0, i] = max(80, pitch[0][0, i])
    else:
        if ik_index != 5:
            print('Этот тип интонационной конструкции подразумевает два акцента. Пожалуйста, поставьте два акцента во фразе.')
            
        cons = 0
        for i in range(accent, second_accent):
            pitch[0][0, i] += pitch_change[ik_index]['accent_1'] - cons
            cons += 3
        pitch[0][0, second_accent] += pitch_change[ik_index]['accent_2']

        sound_number = 0
        for i in range(accent - 1, -1, -1):
            if sound_number <= 2:
                pitch[0][0, i] += pitch_change[ik_index]['before'][2 - sound_number]
#                if is_sound(text[0][i]):
                sound_number += 1
            else:
                pitch[0][0, i] += pitch_change[ik_index]['beginning']
        sound_number = 0  
        for i in range(second_accent + 1, len(text[0])):
            if sound_number <= 1:
                pitch[0][0, i] += pitch_change[ik_index]['after'][sound_number]
#                if is_sound(text[0][i]):
                sound_number += 1
            else:
                pitch[0][0, i] += pitch_change[ik_index]['end']
        for i in range(len(text[0])):
            pitch[0][0, i] = max(80, pitch[0][0, i])
        
    # smooth non-sounds
    for i, symb in enumerate(text[0]):
        if not is_sound(symb):
            has_left_sound, has_right_sound = False, False
            for j in range(i, -1, -1):
                if is_sound(text[0][j]):
                    left_sound = pitch[0][0, j]
                    has_left_sound = True
                    break
            for j in range(i, len(text[0])):
                if is_sound(text[0][j]):
                    right_sound = pitch[0][0, j]
                    has_right_sound = True
                    break
            
            if has_left_sound:
                pitch[0][0, i] = left_sound
            elif has_right_sound:
                pitch[0][0, i] = right_sound
        
    print(pitch[0])
    print(list(zip(pitch[0][0,:].cpu().detach().numpy(), text[0])))
    
    return pitch
