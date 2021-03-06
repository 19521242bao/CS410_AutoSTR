from __future__ import absolute_import

import string

from . import to_torch, to_numpy

def get_vocabulary(voc_type, EOS='EOS', PADDING='PADDING', UNKNOWN='UNKNOWN'):
  '''
  voc_type: str: one of 'LOWERCASE', 'ALLCASES', 'ALLCASES_SYMBOLS'
  '''
  voc = None
  types = ['LOWERCASE', 'ALLCASES', 'ALLCASES_SYMBOLS']
  if voc_type == 'LOWERCASE':
    voc = list(string.digits + "aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfghiìỉĩíịjklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwxyỳỷỹýỵz")
  elif voc_type == 'ALLCASES':
    voc = list(string.digits +'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ')
  elif voc_type == 'ALLCASES_SYMBOLS':
    voc = list('aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
  else:
    raise KeyError('voc_type must be one of "LOWERCASE", "ALLCASES", "ALLCASES_SYMBOLS"')

  # update the voc with specifical chars
  voc.append(EOS)
  voc.append(PADDING)
  voc.append(UNKNOWN)

  return voc

## param voc: the list of vocabulary
def char2id(voc):
  return dict(zip(voc, range(len(voc))))

def id2char(voc):
  return dict(zip(range(len(voc)), voc))

def labels2strs(labels, id2char, char2id):
  # labels: batch_size x len_seq
  if labels.ndimension() == 1:
    labels = labels.unsqueeze(0)
  assert labels.dim() == 2
  labels = to_numpy(labels)
  strings = []
  batch_size = labels.shape[0]

  for i in range(batch_size):
    label = labels[i]
    string = []
    for l in label:
      if l == char2id['EOS']:
        break
      else:
        string.append(id2char[l])
    string = ''.join(string)
    strings.append(string)

  return strings


class dataset_info:

    voc_type = 'ALLCASES_SYMBOLS'
    EOS = 'EOS'
    PADDING = 'PADDING'
    UNKNOWN = 'UNKNOWN'
    voc = get_vocabulary(voc_type, EOS=EOS, PADDING=PADDING, UNKNOWN=UNKNOWN)
    char2id = dict(zip(voc, range(len(voc))))
    id2char = dict(zip(range(len(voc)), voc))
    rec_num_classes = len(voc)
    end_label = char2id[EOS]
    unknown_label = char2id[UNKNOWN]