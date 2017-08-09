from CreateAllEmphOptions import *
from fastdtw import fastdtw

from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from scipy.spatial.distance import euclidean
from os import listdir
from operator import itemgetter
import ntpath
jar_path = r'C:/Users/akiva/OneDrive/Coding_Projects/final_project/netbeans_workspace/FreeTTS-master'


def get_audio_sentence(audio_file_path):
    head, tail = ntpath.split(audio_file_path)
    try:
     return tail[:-4]
    except:
     print('trying to get audio sentence in dtwAlgo. The input file is NOT .wav')


def algo(all_options_path, input_file_name):     # input_file_name -> must include dir + name.

    audio_sentence = get_audio_sentence(input_file_name)
    # creates all the emphasis options:
    create_all_emph_options(all_options_path, audio_sentence)

    # dtw:
    frames = 50  # 20
    first_frame = 30
    mfccs = 20  # upto 26!
    test_frac = 0.2

    # input_file_name = './DTW single file/see%the%bombers fly up.wav'
    # Extract MFCCs from input wav file
    print(input_file_name)
    (rate, sig) = wav.read(input_file_name)
    mfcc_feat = mfcc(sig, rate)
    curr = logfbank(sig, rate)
    input_file_data = curr[first_frame:(first_frame + frames), 0:mfccs] / 20

    # Extract MFCCs from each permutation of 1 emphasized word
    file_names = []
    distances = []
    for file_name in listdir('./DTW single file'):
        print(file_name)
        file_names.append(file_name)
        (rate, sig) = wav.read("./DTW single file/" + file_name)
        mfcc_feat = mfcc(sig, rate)
        curr = logfbank(sig, rate)
        current_file_data = curr[first_frame:(first_frame + frames), 0:mfccs] / 20
        distance, path = fastdtw(input_file_data, current_file_data, dist=euclidean)
        distances.append(distance)

    print(file_names)
    print(distances)
    min_distance_index = min(enumerate(distances), key=itemgetter(1))[0]
    print(min_distance_index)

    s = file_names[min_distance_index]
    c = '%'
    start_end_indexes = [pos for pos, char in enumerate(s) if char == c]
    print(start_end_indexes)
    answer = file_names[min_distance_index][start_end_indexes[0] + 1:start_end_indexes[1]]
    print(answer)
'''
all_options_path = r'C:/Users/akiva/Desktop/algo'
input_file_name =
audio_sentence = 'see the bombers fly up'
'''




