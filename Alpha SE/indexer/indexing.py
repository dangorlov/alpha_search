import os

from .binary_encoders import encode_sequence
from .doc2words import extract_words
from .docreader import *

index_partition_size = 500000


def clear_index(index):
    for term in index.keys():
        index[term] = [index[term][-1]]


def write_index_partition(filename_pattern, index, encoding):
    terms_dict = {}
    with open(filename_pattern + '.idx', 'wb') as index_file:
        term_offset_in_index = 0
        for term, related_docs_ids in index.items():
            if len(related_docs_ids) < 2:
                continue
            encoded_seq = encode_sequence(related_docs_ids, encoding)
            index_file.write(encoded_seq)
            terms_dict[term] = (term_offset_in_index, len(encoded_seq))
            term_offset_in_index += len(encoded_seq)

    with open(filename_pattern + '.dct', 'wb') as terms_dict_file:
        terms_dict_file.write(struct.pack("Q", len(terms_dict)))
        for term, (offset, seq_len) in terms_dict.items():
            terms_dict_file.write(struct.pack("qII", term, offset, seq_len))
    clear_index(index)


def run(encoding_method, *files):
    path = './temp_idx/'
    if not os.path.exists(path):
        os.makedirs(path)
    index, url_list = {}, []
    reader = DocumentStreamReader(files)
    current_partition_id = 0

    index_is_empty = True
    for doc_idx, doc in enumerate(reader):
        index_is_empty = False
        url_list.append(doc.url + '\n')
        terms = set(extract_words(doc.text))
        for term in terms:
            key = hash(term)
            if key in index:
                index[key].append(doc_idx)
            else:
                # Zero index is used for delta computation for first document in sequence
                index[key] = [0, doc_idx]
        if (doc_idx + 1) % index_partition_size == 0:
            filename = '{0}part{1:03d}'.format(path, current_partition_id)
            write_index_partition(filename, index, encoding_method)
            current_partition_id += 1
            index_is_empty = True
    if not index_is_empty:
        write_index_partition(path + 'part{0:03d}'.format(current_partition_id), index, encoding_method)

    with open(path + 'encoding.ini', 'w') as config_file:
        config_file.write(encoding_method)
    with open(path + 'url_list', 'w') as f:
        f.writelines(url_list)
