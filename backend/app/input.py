import numpy as np
import random
from collections import defaultdict

KEYBOARD_MAPPING = {}

def get_keyboard():
    # Swedish QWERTY Keyboard Layout with Shift and AltGr Layers
    swedish_keyboard_layout = {
        # Base layer (unshifted, 0)
        0: [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '´'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', '¨'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', "'"],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-']
        ],

        # Shift layer (uppercase & shifted symbols, 1)
        1: [
            ['!', '"', '#', '¤', '%', '&', '/', '(', ')', '=', '?', '`'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Å', '^'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', '*'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_']
        ],

        # AltGr layer (symbols, now 2 instead of 1)
        2: [
            ['§', '@', '£', '$', '€', '{', '[', ']', '}', '\\', '|', '~'],
            ['q', 'w', '€', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', '¨'],  # Only '€' differs
            ['ä', 'ß', 'ð', 'đ', 'ŋ', 'ħ', 'j', 'ĸ', 'ł', 'ö', 'ä', "'"],  # Special letters
            ['æ', '©', '¢', 'v', 'b', 'n', 'µ', ',', '.', '-']
        ]
    }

    # Map each key to its (row, col, layer) coordinates
    keyboard_mapping = {}

    for layer in [0, 1, 2]:  # Iterate over base, shift, and AltGr layers
        for row_idx, row in enumerate(swedish_keyboard_layout[layer]):
            for col_idx, key in enumerate(row):
                keyboard_mapping[key] = (row_idx, col_idx, layer)

    return keyboard_mapping

KEYBOARD_MAPPING = get_keyboard()


def key_distance(k1, k2, shift_weight=5, altgr_weight=30):
    """
    Computes the Euclidean distance between two keys in a 3D space.
    Shift layer switches are penalized normally, but AltGr switches are penalized more.
    """

    keyboard_mapping = KEYBOARD_MAPPING
    if k1 in keyboard_mapping and k2 in keyboard_mapping:
        x1, y1, l1 = keyboard_mapping[k1]
        x2, y2, l2 = keyboard_mapping[k2]
        
        # Adjust layer distance weight: Shift (1), AltGr (2)
        layer_distance = abs(l1 - l2)
        if layer_distance == 1:  # Shift key switch
            layer_penalty = shift_weight
        elif layer_distance == 2:  # AltGr key switch (more costly)
            layer_penalty = altgr_weight
        else:
            layer_penalty = 0
        
        # Euclidean distance with layer penalty
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + layer_penalty

    return float('inf')  # Large distance for non-existent keys


def error_probability(k1, k2, alpha=1.5):
    """
    Computes the probability of mistyping k1 as k2 based on keyboard distance.
    Uses an exponential decay function to favor closer mistakes.
    """
    d = key_distance(k1, k2)
    return np.exp(-alpha * d) if d < float('inf') else 0



def generate_candidates(word, typo_rate=0.2):
    """
    Generates probable mistyped versions of a word based on keyboard adjacency.
    Includes substitutions, insertions, and deletions.
    """
    candidates = defaultdict(float)
    keyboard_mapping = KEYBOARD_MAPPING
    for i, letter in enumerate(word):
        if letter in keyboard_mapping:
            # 1. **Substitutions**: Replace letter with a neighboring key
            for key in keyboard_mapping.keys():
                if key != letter:
                    new_word = word[:i] + key + word[i+1:]
                    candidates[new_word] += error_probability(letter, key)
            
            # 2. **Insertions**: Add a random nearby letter
            if random.random() < typo_rate:
                nearby_keys = [k for k in keyboard_mapping.keys() if error_probability(letter, k) > 0.01]
                if nearby_keys:
                    insert_key = random.choice(nearby_keys)
                    new_word = word[:i] + insert_key + word[i:]
                    candidates[new_word] += 0.05  # Small probability for insertions
            
            # 3. **Deletions**: Remove a letter
            if random.random() < typo_rate:
                new_word = word[:i] + word[i+1:]
                candidates[new_word] += 0.05  # Small probability for deletions
    
    # Sort candidates by highest probability
    return dict(sorted(candidates.items(), key=lambda x: -x[1]))