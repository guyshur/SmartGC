import time
from Bio import SeqIO
import streamlit as st
from io import StringIO, BytesIO


codon_to_gc_bias = {
    'UUU': 0,
    'UUC': 1,
    'UUA': 0,
    'UUG': 1,
    'CUU': 0,
    'CUC': 1,
    'CUA': 0,
    'CUG': 1,
}


def smart_gc_at():
    smart_gc, smart_at = {}, {}
    with open('codons.txt', mode='r') as in_file:
        for line in in_file:
            codon, gc, ta = line.strip().split(' ', 2)
            smart_gc[codon], smart_at[codon] = int(gc.strip()), int(ta.strip())
    return smart_gc, smart_at


if 'smart_gc' not in st.session_state:
    st.session_state.smart_gc, st.session_state.smart_at = smart_gc_at()


def smart_gc_single(seq):
    gc, at = 0, 0
    for i in range(0, len(seq), 3):
        codon = seq[i:i + 3]
        gc += st.session_state.smart_gc[codon]
        at += st.session_state.smart_at[codon]
    return round(gc / (gc + at), 5)


def smartgc(fasta):
    try:
        try:
            fasta = StringIO(fasta)
        except Exception:
            fasta = BytesIO(fasta)
            fasta = StringIO(fasta.read().decode('utf-8'))
        seen_ids = set()
        sequences = list(SeqIO.parse(fasta, 'fasta'))
        results = {}
        for seq in sequences:
            seq_id = seq.id
            if seq_id in seen_ids:
                raise ValueError(f"Duplicate sequence ID: {seq_id}")
            seen_ids.add(seq_id)
            if not len(seq) % 3 == 0:
                raise ValueError(
                    f"Sequence {seq.id} length is not a multiple of 3.")
            results[seq.id] = smart_gc_single(str(seq.seq))
        return results
    except Exception as e:
        raise e
