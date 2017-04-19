from itertools import islice
import os

from torch.utils.data import Dataset


class KompasTempo:
    def __init__(self, data_dir=os.path.join(os.getenv('DATA_DIR'), 'input'),
                 which='train', max_sentences=None):
        self.data_dir = data_dir
        self.which = which
        self.max_sentences = max_sentences

        self._dataset_file = os.path.join(self.data_dir, f'{which}.txt')

    def _get_iterator(self):
        with open(self._dataset_file) as f:
            yield from f

    def __iter__(self):
        return islice(self._get_iterator(), self.max_sentences)


class KompasTempoDataset(Dataset):
    def __init__(self, iterator):
        self.lines = list(iterator)

    def _to_chars(self, line):
        return ['<s>'] + list(line) + ['</s>']

    def __getitem__(self, index):
        chars = self._to_chars(self.lines[index])
        return chars[:-1], chars[1:]

    def __len__(self):
        return len(self.lines)