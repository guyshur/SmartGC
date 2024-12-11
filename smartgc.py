import time
from Bio import SeqIO
import streamlit as st
from io import StringIO, BytesIO


def smart_gc_at():
    smart_gc, smart_at = {}, {}
    with open('codons.txt', mode='r') as in_file:
        for line in in_file:
            codon, gc, ta = line.strip().split(' ', 2)
            smart_gc[codon], smart_at[codon] = int(gc.strip()), int(ta.strip())
    return smart_gc, smart_at


def smart_gc_single(seq, smart_gc_dict, smart_at_dict):
    gc, at = 0, 0
    for i in range(0, len(seq), 3):
        codon = seq[i:i + 3]
        gc += smart_gc_dict[codon]
        at += smart_at_dict[codon]
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
        smart_gc_dict, smart_at_dict = smart_gc_at()
        for seq in sequences:
            seq_id = seq.id
            if seq_id in seen_ids:
                raise ValueError(f"Duplicate sequence ID: {seq_id}")
            seen_ids.add(seq_id)
            if not len(seq) % 3 == 0:
                raise ValueError(
                    f"Sequence {seq.id} length is not a multiple of 3.")
            results[seq.id] = smart_gc_single(
                str(seq.seq), smart_gc_dict, smart_at_dict)
        return results
    except Exception as e:
        raise e
