import streamlit as st
import pandas as pd
from Bio import SeqIO
from io import StringIO

# Streamlit UI
st.title("Cas13d Guide RNA Grouping App")

# Upload FASTA file
fasta_file = st.file_uploader("Upload your FASTA exon-2 sequences file", type=['fasta', 'fas'])

# Upload guide RNA result files (multiple CSVs)
guide_files = st.file_uploader("Upload guide RNA result CSV files", type=['csv'], accept_multiple_files=True)

if fasta_file and guide_files:

    # Parse FASTA sequences
    fasta_io = StringIO(fasta_file.getvalue().decode("utf-8"))
    sequences = {record.id: str(record.seq) for record in SeqIO.parse(fasta_io, "fasta")}

    st.success(f"Loaded {len(sequences)} sequences from FASTA file.")

    # Read guide RNA files
    guide_dict = {}
    for guide_file in guide_files:
        seq_id = guide_file.name.split('_')[1]  # Assuming filenames contain sequence IDs, adapt as needed
        df = pd.read_csv(guide_file)
        for guide in df['GuideSeq']:
            guide_dict.setdefault(guide, set()).add(seq_id)

    # Categorize guides
    total_sequences = set(sequences.keys())
    specific_guides, multi_guides, global_guides = [], [], []

    for guide, seq_ids in guide_dict.items():
        if len(seq_ids) == 1:
            specific_guides.append((guide, list(seq_ids)))
        elif seq_ids == total_sequences:
            global_guides.append((guide, list(seq_ids)))
        else:
            multi_guides.append((guide, list(seq_ids)))

    # Display Results
    st.subheader("Guide RNA Categories")

    st.write(f"### Global Guides (work for all {len(total_sequences)} sequences):")
    st.write(pd.DataFrame(global_guides, columns=["Guide Sequence", "Targeted Sequences"]))

    st.write(f"### Multi-target Guides (work for multiple but not all sequences):")
    st.write(pd.DataFrame(multi_guides, columns=["Guide Sequence", "Targeted Sequences"]))

    st.write("### Specific Guides (work only for one sequence):")
    st.write(pd.DataFrame(specific_guides, columns=["Guide Sequence", "Targeted Sequence"]))

else:
    st.info("Please upload both your FASTA and guide RNA CSV files to proceed.")