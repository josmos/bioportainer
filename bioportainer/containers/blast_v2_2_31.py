import os
from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config


class Blast_v2_2_31(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_blastn_params()
        self.set_blastp_params()
        self.set_makeblastdb_params()

    def get_opt_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if v == "threads":
                v = str(config.container_threads)
            if type(v) == bool and v is True:
                l += ["-" + k]
            elif type(v) == bool and v is False:
                continue
            else:
                l += ["-" + k, v]

        return l

    @MultiCmdContainer.impl_set_opt_params
    def set_makeblastdb_params(self):
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_blastn_params(self, import_search_strategy=False, export_search_strategy=False,
                          task=False, dbsize=False, gilist=False, seqidlist=False,
                          negative_gilist=False, entrez_query=False, db_soft_mask=False,
                          db_hard_mask=False, subject=False, subject_loc=False,  evalue=False,
                          word_size=False, gapopen=False, gapextend=False,perc_identity=False,
                          qcov_hsp_perc=False, max_hsps=False, xdrop_ungap=False, xdrop_gap=False,
                          xdrop_gap_final=False, searchsp=False, sum_stats=False, penalty=False,
                          reward=False, no_greedy=False, min_raw_gapped_score=False,
                          template_type=False, template_length=False, dust=False, filtering_db=False,
                          window_masker_taxid=False, window_masker_db=False, soft_masking=False,
                          ungapped=False, culling_limit=False, best_hit_overhang=False,
                          best_hit_score_edge=False, window_size=False, off_diagonal_range=False,
                          use_index=False, index_name=False, lcase_masking=False, query_loc=False,
                          strand=False, parse_deflines=False, outfmt=False, show_gis=False,
                          num_descriptions=False, num_alignments=False, line_length=False, html=False,
                          max_target_seqs=False, num_threads="threads"):
        """USAGE
blastn [-h] [-help] [-import_search_strategy filename]
[-export_search_strategy filename] [-task task_name] [-db database_name]
[-dbsize num_letters] [-gilist filename] [-seqidlist filename]
[-negative_gilist filename] [-entrez_query entrez_query]
[-db_soft_mask filtering_algorithm] [-db_hard_mask filtering_algorithm]
[-subject subject_input_file] [-subject_loc range] [-query input_file]
[-out output_file] [-evalue evalue] [-word_size int_value]
[-gapopen open_penalty] [-gapextend extend_penalty]
[-perc_identity float_value] [-qcov_hsp_perc float_value]
[-max_hsps int_value] [-xdrop_ungap float_value] [-xdrop_gap float_value]
[-xdrop_gap_final float_value] [-searchsp int_value]
[-sum_stats bool_value] [-penalty penalty] [-reward reward] [-no_greedy]
[-min_raw_gapped_score int_value] [-template_type type]
[-template_length int_value] [-dust DUST_options]
[-filtering_db filtering_database]
[-window_masker_taxid window_masker_taxid]
[-window_masker_db window_masker_db] [-soft_masking soft_masking]
[-ungapped] [-culling_limit int_value] [-best_hit_overhang float_value]
[-best_hit_score_edge float_value] [-window_size int_value]
[-off_diagonal_range int_value] [-use_index boolean] [-index_name string]
[-lcase_masking] [-query_loc range] [-strand strand] [-parse_deflines]
[-outfmt format] [-show_gis] [-num_descriptions int_value]
[-num_alignments int_value] [-line_length line_length] [-html]
[-max_target_seqs num_sequences] [-num_threads int_value] [-remote]
[-version]

DESCRIPTION
Nucleotide-Nucleotide BLAST 2.2.31+

OPTIONAL ARGUMENTS
-h
Print USAGE and DESCRIPTION;  ignore all other parameters
-help
Print USAGE, DESCRIPTION and ARGUMENTS; ignore all other parameters
-version
Print version number;  ignore other arguments

*** Input query options
-query <File_In>
Input file name
Default = `-'
-query_loc <String>
Location on the query sequence in 1-based offsets (Format: start-stop)
-strand <String, `both', `minus', `plus'>
Query strand(s) to search against database/subject
Default = `both'

*** General search options
-task <String, Permissible values: 'blastn' 'blastn-short' 'dc-megablast'
            'megablast' 'rmblastn' >
Task to execute
Default = `megablast'
-db <String>
BLAST database name
* Incompatible with:  subject, subject_loc
-out <File_Out>
Output file name
Default = `-'
-evalue <Real>
Expectation value (E) threshold for saving hits
Default = `10'
-word_size <Integer, >=4>
Word size for wordfinder algorithm (length of best perfect match)
-gapopen <Integer>
Cost to open a gap
-gapextend <Integer>
Cost to extend a gap
-penalty <Integer, <=0>
Penalty for a nucleotide mismatch
-reward <Integer, >=0>
Reward for a nucleotide match
-use_index <Boolean>
Use MegaBLAST database index
Default = `false'
-index_name <String>
MegaBLAST database index name

*** BLAST-2-Sequences options
-subject <File_In>
Subject sequence(s) to search
* Incompatible with:  db, gilist, seqidlist, negative_gilist,
db_soft_mask, db_hard_mask
-subject_loc <String>
Location on the subject sequence in 1-based offsets (Format: start-stop)
* Incompatible with:  db, gilist, seqidlist, negative_gilist,
db_soft_mask, db_hard_mask, remote

*** Formatting options
-outfmt <String>
alignment view options:
 0 = pairwise,
 1 = query-anchored showing identities,
 2 = query-anchored no identities,
 3 = flat query-anchored, show identities,
 4 = flat query-anchored, no identities,
 5 = XML Blast output,
 6 = tabular,
 7 = tabular with comment lines,
 8 = Text ASN.1,
 9 = Binary ASN.1,
10 = Comma-separated values,
11 = BLAST archive format (ASN.1),
12 = JSON Seqalign output,
13 = JSON Blast output,
14 = XML2 Blast output

Options 6, 7, and 10 can be additionally configured to produce
a custom format specified by space delimited format specifiers.
The supported format specifiers are:
    qseqid means Query Seq-id
       qgi means Query GI
      qacc means Query accesion
   qaccver means Query accesion.version
      qlen means Query sequence length
    sseqid means Subject Seq-id
 sallseqid means All subject Seq-id(s), separated by a ';'
       sgi means Subject GI
    sallgi means All subject GIs
      sacc means Subject accession
   saccver means Subject accession.version
   sallacc means All subject accessions
      slen means Subject sequence length
    qstart means Start of alignment in query
      qend means End of alignment in query
    sstart means Start of alignment in subject
      send means End of alignment in subject
      qseq means Aligned part of query sequence
      sseq means Aligned part of subject sequence
    evalue means Expect value
  bitscore means Bit score
     score means Raw score
    length means Alignment length
    pident means Percentage of identical matches
    nident means Number of identical matches
  mismatch means Number of mismatches
  positive means Number of positive-scoring matches
   gapopen means Number of gap openings
      gaps means Total number of gaps
      ppos means Percentage of positive-scoring matches
    frames means Query and subject frames separated by a '/'
    qframe means Query frame
    sframe means Subject frame
      btop means Blast traceback operations (BTOP)
   staxids means unique Subject Taxonomy ID(s), separated by a ';'
         (in numerical order)
 sscinames means unique Subject Scientific Name(s), separated by a ';'
 scomnames means unique Subject Common Name(s), separated by a ';'
sblastnames means unique Subject Blast Name(s), separated by a ';'
         (in alphabetical order)
sskingdoms means unique Subject Super Kingdom(s), separated by a ';'
         (in alphabetical order)
    stitle means Subject Title
salltitles means All Subject Title(s), separated by a '<>'
   sstrand means Subject Strand
     qcovs means Query Coverage Per Subject
   qcovhsp means Query Coverage Per HSP
When not provided, the default value is:
'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
evalue bitscore', which is equivalent to the keyword 'std'
Default = `0'
-show_gis
Show NCBI GIs in deflines?
-num_descriptions <Integer, >=0>
Number of database sequences to show one-line descriptions for
Not applicable for outfmt > 4
Default = `500'
* Incompatible with:  max_target_seqs
-num_alignments <Integer, >=0>
Number of database sequences to show alignments for
Default = `250'
* Incompatible with:  max_target_seqs
-line_length <Integer, >=1>
Line length for formatting alignments
Not applicable for outfmt > 4
Default = `60'
-html
Produce HTML output?

*** Query filtering options
-dust <String>
Filter query sequence with DUST (Format: 'yes', 'level window linker', or
'no' to disable)
Default = `20 64 1'
-filtering_db <String>
BLAST database containing filtering elements (i.e.: repeats)
-window_masker_taxid <Integer>
Enable WindowMasker filtering using a Taxonomic ID
-window_masker_db <String>
Enable WindowMasker filtering using this repeats database.
-soft_masking <Boolean>
Apply filtering locations as soft masks
Default = `true'
-lcase_masking
Use lower case filtering in query and subject sequence(s)?

*** Restrict search or results
-gilist <String>
Restrict search of database to list of GI's
* Incompatible with:  negative_gilist, seqidlist, remote, subject,
subject_loc
-seqidlist <String>
Restrict search of database to list of SeqId's
* Incompatible with:  gilist, negative_gilist, remote, subject,
subject_loc
-negative_gilist <String>
Restrict search of database to everything except the listed GIs
* Incompatible with:  gilist, seqidlist, remote, subject, subject_loc
-entrez_query <String>
Restrict search with the given Entrez query
* Requires:  remote
-db_soft_mask <String>
Filtering algorithm ID to apply to the BLAST database as soft masking
* Incompatible with:  db_hard_mask, subject, subject_loc
-db_hard_mask <String>
Filtering algorithm ID to apply to the BLAST database as hard masking
* Incompatible with:  db_soft_mask, subject, subject_loc
-perc_identity <Real, 0..100>
Percent identity
-qcov_hsp_perc <Real, 0..100>
Percent query coverage per hsp
-max_hsps <Integer, >=1>
Set maximum number of HSPs per subject sequence to save for each query
-culling_limit <Integer, >=0>
If the query range of a hit is enveloped by that of at least this many
higher-scoring hits, delete the hit
* Incompatible with:  best_hit_overhang, best_hit_score_edge
-best_hit_overhang <Real, (>0 and <0.5)>
Best Hit algorithm overhang value (recommended value: 0.1)
* Incompatible with:  culling_limit
-best_hit_score_edge <Real, (>0 and <0.5)>
Best Hit algorithm score edge value (recommended value: 0.1)
* Incompatible with:  culling_limit
-max_target_seqs <Integer, >=1>
Maximum number of aligned sequences to keep
Not applicable for outfmt <= 4
Default = `500'
* Incompatible with:  num_descriptions, num_alignments

*** Discontiguous MegaBLAST options
-template_type <String, `coding', `coding_and_optimal', `optimal'>
Discontiguous MegaBLAST template type
* Requires:  template_length
-template_length <Integer, Permissible values: '16' '18' '21' >
Discontiguous MegaBLAST template length
* Requires:  template_type

*** Statistical options
-dbsize <Int8>
Effective length of the database
-searchsp <Int8, >=0>
Effective length of the search space
-sum_stats <Boolean>
Use sum statistics

*** Search strategy options
-import_search_strategy <File_In>
Search strategy to use
* Incompatible with:  export_search_strategy
-export_search_strategy <File_Out>
File name to record the search strategy used
* Incompatible with:  import_search_strategy

*** Extension options
-xdrop_ungap <Real>
X-dropoff value (in bits) for ungapped extensions
-xdrop_gap <Real>
X-dropoff value (in bits) for preliminary gapped extensions
-xdrop_gap_final <Real>
X-dropoff value (in bits) for final gapped alignment
-no_greedy
Use non-greedy dynamic programming extension
-min_raw_gapped_score <Integer>
Minimum raw gapped score to keep an alignment in the preliminary gapped and
traceback stages
-ungapped
Perform ungapped alignment only?
-window_size <Integer, >=0>
Multiple hits window size, use 0 to specify 1-hit algorithm
-off_diagonal_range <Integer, >=0>
Number of off-diagonals to search for the 2nd hit, use 0 to turn off
Default = `0'

*** Miscellaneous options
-parse_deflines
Should the query and subject defline(s) be parsed?
-num_threads <Integer, >=1>
Number of threads (CPUs) to use in the BLAST search
Default = `1'
* Incompatible with:  remote
-remote
Execute search remotely?
* Incompatible with:  gilist, seqidlist, negative_gilist, subject_loc,
num_threads"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_blastp_params(self, import_search_strategy=False, export_search_strategy=False, task=False,
                          dbsize=False, gilist=False, seqidlist=False, negative_gilist=False,
                          entrez_query=False, db_soft_mask=False, db_hard_mask=False, subject=False,
                          subject_loc=False, evalue=False, word_size=False, gapopen=False,
                          gapextend=False, qcov_hsp_perc=False, max_hsps=False, xdrop_ungap=False,
                          xdrop_gap=False, xdrop_gap_final=False, searchsp=False, sum_stats=False,
                          seg=False, soft_masking=False, matrix=False, threshold=False,
                          culling_limit=False, best_hit_overhang=False, best_hit_score_edge=False,
                          window_size=False, lcase_masking=False, query_loc=False,
                          parse_deflines=False, outfmt=False, show_gis=False, num_descriptions=False,
                          num_alignments=False, line_length=False, html=False, max_target_seqs=False,
                          num_threads="threads", ungapped=False, comp_based_stats=False, use_sw_tback=False):
        """USAGE
blastp [-h] [-help] [-import_search_strategy filename]
[-export_search_strategy filename] [-task task_name] [-db database_name]
[-dbsize num_letters] [-gilist filename] [-seqidlist filename]
[-negative_gilist filename] [-entrez_query entrez_query]
[-db_soft_mask filtering_algorithm] [-db_hard_mask filtering_algorithm]
[-subject subject_input_file] [-subject_loc range] [-query input_file]
[-out output_file] [-evalue evalue] [-word_size int_value]
[-gapopen open_penalty] [-gapextend extend_penalty]
[-qcov_hsp_perc float_value] [-max_hsps int_value]
[-xdrop_ungap float_value] [-xdrop_gap float_value]
[-xdrop_gap_final float_value] [-searchsp int_value]
[-sum_stats bool_value] [-seg SEG_options] [-soft_masking soft_masking]
[-matrix matrix_name] [-threshold float_value] [-culling_limit int_value]
[-best_hit_overhang float_value] [-best_hit_score_edge float_value]
[-window_size int_value] [-lcase_masking] [-query_loc range]
[-parse_deflines] [-outfmt format] [-show_gis]
[-num_descriptions int_value] [-num_alignments int_value]
[-line_length line_length] [-html] [-max_target_seqs num_sequences]
[-num_threads int_value] [-ungapped] [-remote] [-comp_based_stats compo]
[-use_sw_tback] [-version]

DESCRIPTION
Protein-Protein BLAST 2.2.31+

OPTIONAL ARGUMENTS
-h
Print USAGE and DESCRIPTION;  ignore all other parameters
-help
Print USAGE, DESCRIPTION and ARGUMENTS; ignore all other parameters
-version
Print version number;  ignore other arguments

*** Input query options
-query <File_In>
Input file name
Default = `-'
-query_loc <String>
Location on the query sequence in 1-based offsets (Format: start-stop)

*** General search options
-task <String, Permissible values: 'blastp' 'blastp-fast' 'blastp-short' >
Task to execute
Default = `blastp'
-db <String>
BLAST database name
* Incompatible with:  subject, subject_loc
-out <File_Out>
Output file name
Default = `-'
-evalue <Real>
Expectation value (E) threshold for saving hits
Default = `10'
-word_size <Integer, >=2>
Word size for wordfinder algorithm
-gapopen <Integer>
Cost to open a gap
-gapextend <Integer>
Cost to extend a gap
-matrix <String>
Scoring matrix name (normally BLOSUM62)
-threshold <Real, >=0>
Minimum word score such that the word is added to the BLAST lookup table
-comp_based_stats <String>
Use composition-based statistics:
   D or d: default (equivalent to 2 )
   0 or F or f: No composition-based statistics
   1: Composition-based statistics as in NAR 29:2994-3005, 2001
   2 or T or t : Composition-based score adjustment as in Bioinformatics
21:902-911,
   2005, conditioned on sequence properties
   3: Composition-based score adjustment as in Bioinformatics 21:902-911,
   2005, unconditionally
Default = `2'

*** BLAST-2-Sequences options
-subject <File_In>
Subject sequence(s) to search
* Incompatible with:  db, gilist, seqidlist, negative_gilist,
db_soft_mask, db_hard_mask
-subject_loc <String>
Location on the subject sequence in 1-based offsets (Format: start-stop)
* Incompatible with:  db, gilist, seqidlist, negative_gilist,
db_soft_mask, db_hard_mask, remote

*** Formatting options
-outfmt <String>
alignment view options:
 0 = pairwise,
 1 = query-anchored showing identities,
 2 = query-anchored no identities,
 3 = flat query-anchored, show identities,
 4 = flat query-anchored, no identities,
 5 = XML Blast output,
 6 = tabular,
 7 = tabular with comment lines,
 8 = Text ASN.1,
 9 = Binary ASN.1,
10 = Comma-separated values,
11 = BLAST archive format (ASN.1),
12 = JSON Seqalign output,
13 = JSON Blast output,
14 = XML2 Blast output

Options 6, 7, and 10 can be additionally configured to produce
a custom format specified by space delimited format specifiers.
The supported format specifiers are:
    qseqid means Query Seq-id
       qgi means Query GI
      qacc means Query accesion
   qaccver means Query accesion.version
      qlen means Query sequence length
    sseqid means Subject Seq-id
 sallseqid means All subject Seq-id(s), separated by a ';'
       sgi means Subject GI
    sallgi means All subject GIs
      sacc means Subject accession
   saccver means Subject accession.version
   sallacc means All subject accessions
      slen means Subject sequence length
    qstart means Start of alignment in query
      qend means End of alignment in query
    sstart means Start of alignment in subject
      send means End of alignment in subject
      qseq means Aligned part of query sequence
      sseq means Aligned part of subject sequence
    evalue means Expect value
  bitscore means Bit score
     score means Raw score
    length means Alignment length
    pident means Percentage of identical matches
    nident means Number of identical matches
  mismatch means Number of mismatches
  positive means Number of positive-scoring matches
   gapopen means Number of gap openings
      gaps means Total number of gaps
      ppos means Percentage of positive-scoring matches
    frames means Query and subject frames separated by a '/'
    qframe means Query frame
    sframe means Subject frame
      btop means Blast traceback operations (BTOP)
   staxids means unique Subject Taxonomy ID(s), separated by a ';'
         (in numerical order)
 sscinames means unique Subject Scientific Name(s), separated by a ';'
 scomnames means unique Subject Common Name(s), separated by a ';'
sblastnames means unique Subject Blast Name(s), separated by a ';'
         (in alphabetical order)
sskingdoms means unique Subject Super Kingdom(s), separated by a ';'
         (in alphabetical order)
    stitle means Subject Title
salltitles means All Subject Title(s), separated by a '<>'
   sstrand means Subject Strand
     qcovs means Query Coverage Per Subject
   qcovhsp means Query Coverage Per HSP
When not provided, the default value is:
'qseqid sseqid pident length mismatch gapopen qstart qend sstart send
evalue bitscore', which is equivalent to the keyword 'std'
Default = `0'
-show_gis
Show NCBI GIs in deflines?
-num_descriptions <Integer, >=0>
Number of database sequences to show one-line descriptions for
Not applicable for outfmt > 4
Default = `500'
* Incompatible with:  max_target_seqs
-num_alignments <Integer, >=0>
Number of database sequences to show alignments for
Default = `250'
* Incompatible with:  max_target_seqs
-line_length <Integer, >=1>
Line length for formatting alignments
Not applicable for outfmt > 4
Default = `60'
-html
Produce HTML output?

*** Query filtering options
-seg <String>
Filter query sequence with SEG (Format: 'yes', 'window locut hicut', or
'no' to disable)
Default = `no'
-soft_masking <Boolean>
Apply filtering locations as soft masks
Default = `false'
-lcase_masking
Use lower case filtering in query and subject sequence(s)?

*** Restrict search or results
-gilist <String>
Restrict search of database to list of GI's
* Incompatible with:  negative_gilist, seqidlist, remote, subject,
subject_loc
-seqidlist <String>
Restrict search of database to list of SeqId's
* Incompatible with:  gilist, negative_gilist, remote, subject,
subject_loc
-negative_gilist <String>
Restrict search of database to everything except the listed GIs
* Incompatible with:  gilist, seqidlist, remote, subject, subject_loc
-entrez_query <String>
Restrict search with the given Entrez query
* Requires:  remote
-db_soft_mask <String>
Filtering algorithm ID to apply to the BLAST database as soft masking
* Incompatible with:  db_hard_mask, subject, subject_loc
-db_hard_mask <String>
Filtering algorithm ID to apply to the BLAST database as hard masking
* Incompatible with:  db_soft_mask, subject, subject_loc
-qcov_hsp_perc <Real, 0..100>
Percent query coverage per hsp
-max_hsps <Integer, >=1>
Set maximum number of HSPs per subject sequence to save for each query
-culling_limit <Integer, >=0>
If the query range of a hit is enveloped by that of at least this many
higher-scoring hits, delete the hit
* Incompatible with:  best_hit_overhang, best_hit_score_edge
-best_hit_overhang <Real, (>0 and <0.5)>
Best Hit algorithm overhang value (recommended value: 0.1)
* Incompatible with:  culling_limit
-best_hit_score_edge <Real, (>0 and <0.5)>
Best Hit algorithm score edge value (recommended value: 0.1)
* Incompatible with:  culling_limit
-max_target_seqs <Integer, >=1>
Maximum number of aligned sequences to keep
Not applicable for outfmt <= 4
Default = `500'
* Incompatible with:  num_descriptions, num_alignments

*** Statistical options
-dbsize <Int8>
Effective length of the database
-searchsp <Int8, >=0>
Effective length of the search space
-sum_stats <Boolean>
Use sum statistics

*** Search strategy options
-import_search_strategy <File_In>
Search strategy to use
* Incompatible with:  export_search_strategy
-export_search_strategy <File_Out>
File name to record the search strategy used
* Incompatible with:  import_search_strategy

*** Extension options
-xdrop_ungap <Real>
X-dropoff value (in bits) for ungapped extensions
-xdrop_gap <Real>
X-dropoff value (in bits) for preliminary gapped extensions
-xdrop_gap_final <Real>
X-dropoff value (in bits) for final gapped alignment
-window_size <Integer, >=0>
Multiple hits window size, use 0 to specify 1-hit algorithm
-ungapped
Perform ungapped alignment only?

*** Miscellaneous options
-parse_deflines
Should the query and subject defline(s) be parsed?
-num_threads <Integer, >=1>
Number of threads (CPUs) to use in the BLAST search
Default = `1'
* Incompatible with:  remote
-remote
Execute search remotely?
* Incompatible with:  gilist, seqidlist, negative_gilist, subject_loc,
num_threads
-use_sw_tback
Compute locally optimal Smith-Waterman alignments?"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_makeblastdb_params(self, input_type=False, dbtype="nucl", title=False,
                               parse_seqids=False, hash_index=False, mask_data=False, mask_id=False,
                               mask_desc=False, gi_mask=False, gi_mask_name=False, out=False,
                               max_file_sz=False, taxid=False, taxid_map=False, logfile=False):
        """USAGE
  makeblastdb [-h] [-help] [-in input_file] [-input_type type]
    -dbtype molecule_type [-title database_title] [-parse_seqids]
    [-hash_index] [-mask_data mask_data_files] [-mask_id mask_algo_ids]
    [-mask_desc mask_algo_descriptions] [-gi_mask]
    [-gi_mask_name gi_based_mask_names] [-out database_name]
    [-max_file_sz number_of_bytes] [-taxid TaxID] [-taxid_map TaxIDMapFile]
    [-logfile File_Name] [-version]

DESCRIPTION
   Application to create BLAST databases, version 2.2.29+

REQUIRED ARGUMENTS
 -dbtype <String, `nucl', `prot'>
   Molecule type of target db

OPTIONAL ARGUMENTS
 -h
   Print USAGE and DESCRIPTION;  ignore all other parameters
 -help
   Print USAGE, DESCRIPTION and ARGUMENTS; ignore all other parameters
 -version
   Print version number;  ignore other arguments

 *** Input options
 -in <File_In>
   Input file/database name
   Default = `-'
 -input_type <String, `asn1_bin', `asn1_txt', `blastdb', `fasta'>
   Type of the data specified in input_file
   Default = `fasta'

 *** Configuration options
 -title <String>
   Title for BLAST database
   Default = input file name provided to -in argument
 -parse_seqids
   Option to parse seqid for FASTA input if set, for all other input types
   seqids are parsed automatically
 -hash_index
   Create index of sequence hash values.

 *** Sequence masking options
 -mask_data <String>
   Comma-separated list of input files containing masking data as produced by
   NCBI masking applications (e.g. dustmasker, segmasker, windowmasker)
 -mask_id <String>
   Comma-separated list of strings to uniquely identify the masking algorithm
    * Requires:  mask_data
    * Incompatible with:  gi_mask
 -mask_desc <String>
   Comma-separated list of free form strings to describe the masking algorithm
   details
    * Requires:  mask_id
 -gi_mask
   Create GI indexed masking data.
    * Requires:  parse_seqids
    * Incompatible with:  mask_id
 -gi_mask_name <String>
   Comma-separated list of masking data output files.
    * Requires:  mask_data, gi_mask

 *** Output options
 -out <String>
   Name of BLAST database to be created
   Default = input file name provided to -in argumentRequired if multiple
   file(s)/database(s) are provided as input
 -max_file_sz <String>
   Maximum file size for BLAST database files
   Default = `1GB'

 *** Taxonomy options
 -taxid <Integer, >=0>
   Taxonomy ID to assign to all sequences
    * Incompatible with:  taxid_map
 -taxid_map <File_In>
   Text file mapping sequence IDs to taxonomy IDs.
   Format:<SequenceId> <TaxonomyId><newline>
    * Requires:  parse_seqids
    * Incompatible with:  taxid
 -logfile <File_Out>
   File to which the program log should be redirected
"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="blastn", mount=("path/to/db",), out_postfix=""):
        if subcmd == "blastn":
            of = sample_io.id + "_" + subcmd + "_" + out_postfix + ".txt"
            if mount == ("path/to/db",):
                raise IOError("No db specified")

            else:
                db = os.path.split(mount[0])[1]

            self.cmd = [subcmd, "-db", db, "-query", sample_io.files[0].name, "-out", of] \
                       + self.get_opt_params("blastn_params")

        elif subcmd == "blastp":
            of = sample_io.id + "_" + subcmd + "_" + out_postfix + ".txt"
            if subcmd == "blastn":
                if not mount:
                    raise IOError("No db specified")

                else:
                    db = os.path.split(mount[0])[1]

                self.cmd = [subcmd, "-db", db, "-query", sample_io.files[0].name, "-out", of] \
                           + self.get_opt_params("blastp_params")

        elif subcmd == "makeblastdb":
            input_file = os.path.split(mount[0])[1]
            self.cmd = [subcmd, "-in", input_file] + self.get_opt_params("makeblastdb_params")

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="blastn", mount=("path/to/db",), out_postfix=""):
        pass


