import numpy as np
import torch
import set_model_ctc
import htk_io
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn as nn
import ctc_decode

gpu_dtype = torch.cuda.FloatTensor

eps = 1e-8


# mean and variance of the training data will be extracted from this file
stat_file = "/home/michal/Documents/CTC-speech-recognition/preprocessing/mvstats/stat"
# a list of phones, in the same order as the CTC output, excluding the blank label
mapping_file = 'hmmlist'
layers = 4
hidden_size = 256
num_dirs = 2
decoder_type = 'Greedy'      # Beam or Beam_LM or Greedy
out_mlf = 'result61.mlf'     # output mlf file, containing the decoded strings


def create_mapping(map_file):
    labels = ['_']

    with open(map_file) as m:
        for line in m:
            line = line.strip()
            if line:
                labels.append(line)
    return labels


def read_mv(stat):
    mean_flag = var_flag = False
    m = v = None
    with open(stat) as s:
        for line in s:
            line = line.strip()
            if len(line) < 1:
                continue
            if "MEAN" in line:
                mean_flag = True
                continue
            if mean_flag:
                m = list(map(float, line.split()))
                mean_flag = False
                continue
            if "VARIANCE" in line:
                var_flag = True
                continue
            if var_flag:
                v = list(map(float, line.split()))
                var_flag = False
                continue
    return np.array(m, dtype=np.float64), np.array(v, dtype=np.float64)


def org_data(utt_feat, skip_frames=0):
    num_frames, num_channels = utt_feat.shape

    if skip_frames > 0:
        utt_feat = np.pad(utt_feat, ((0, skip_frames), (0, 0)),
                          mode='edge')    # pad the ending frames
        utt_feat = utt_feat[skip_frames:, :]

    return utt_feat.reshape(1, num_frames, num_channels)


def gen_decoded(feat_list, model_path):
    model = set_model_ctc.Layered_RNN(rnn_input_size=25, nb_layers=layers, rnn_hidden_size=hidden_size,
                                      bidirectional=True if num_dirs == 2 else False, batch_norm=True, num_classes=61)
    model = model.type(gpu_dtype)
    model.load_state_dict(torch.load(model_path))     # load model params
    # Put the model in test mode (the opposite of model.train(), essentially)
    model.eval()

    decoder_type == 'Greedy'
    labels = create_mapping(mapping_file)
    decoder = ctc_decode.GreedyDecoder_test(
        labels, output='char', space_idx=-1)     # setup greedy decoder

    m, v = read_mv(stat_file)
    if m is None or v is None:
        raise Exception("mean or variance vector does not exist")

    with open(feat_list) as f:
        with open(out_mlf, 'w') as fw:
            fw.write('#!MLF!#\n')
            for line in f:
                line = line.strip()
                if len(line) < 1:
                    continue
                print("recognizing file %s" % line)
                out_name = '"' + line[:line.rfind('.')] + '.rec' + '"'
                fw.write(out_name + '\n')
                io = htk_io.fopen(line)
                utt_feat = io.getall()
                utt_feat -= m       # normalize mean
                utt_feat /= (np.sqrt(v) + eps)     # normalize var
                feat_numpy = org_data(utt_feat, skip_frames=5)
                feat_tensor = torch.from_numpy(feat_numpy).type(gpu_dtype)
                x = Variable(feat_tensor.type(gpu_dtype), volatile=True)
                input_sizes_list = [x.size(1)]
                x = nn.utils.rnn.pack_padded_sequence(
                    x, input_sizes_list, batch_first=True)
                probs = model(x, input_sizes_list)
                probs = probs.data.cpu()
                decoded = decoder.decode(probs, input_sizes_list)[0]
                for word in decoded:
                    fw.write(word + '\n')
                fw.write('.\n')
                print(' '.join(decoded))


def main_test_fun(feat_list, model_path):
    gen_decoded(feat_list=feat_list, model_path=model_path)

if __name__ == '__main__':
    gen_decoded(
        feat_list='/home/michal/Documents/CTC-speech-recognition/preprocessing/test_features_files.scp',
        model_path='/home/michal/Documents/models/weights_ctc-29-01-2022/epoch9_lr0.001_cvtensor(74.5483).pkl'
    )
