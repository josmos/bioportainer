from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config
import psutil
import os


class Cgview_v1_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_cgview_params()
        self.set_cgview_xml_builder_params()

    def get_perl_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if type(v) == bool and v is True:
                l += ["-" + k, "T"]
            elif type(v) == bool and v is False:
                continue
            else:
                l += ["-" + k, v]

        return l

    @MultiCmdContainer.impl_set_opt_params
    def set_cgview_params(self, A=False, c=False, D=False, d=False, E=False, e=False, f="PNG", h=False, H=False, I=False,
                       L=False, p=False, r=False, R=False, s=False, S=False, u=False, U=False, W=False, x=False,
                       z=False):
        """-A <integer> Specifies a label font size.
-c <integer> Specifies the base to center on when zooming.
-D <integer> Specifies a legend font size.
-d <real> Specifies tick density, between 0 and 1.0. Default is 1.0.
-E <boolean> Whether or not to embed vector-based text in SVG output.
-e <boolean> Whether or not to exclude SVG output from image series.
-f <format> The format of the output: PNG, JPG, SVG, or SVGZ.
-h <file> HTML file to create.
-H <integer> The height of the map.
-i <file> The input file to parse.
-I <boolean> Whether or not to draw labels on the inside of the backbone circle.
-L <integer> The width of an external legend.
-o <file> The image file to create.
-p <path> The path to the image file in the HTML file created using the -h option.
-r <boolean> Whether or not to remove legends.
-R <boolean> Whether or not to remove labels.
-s <directory> Directory to receive an image series.
-S <boolean> Whether or not to reference external stylesheet in HTML output.
-u <boolean> Whether or not to reference overlib.js in HTML output.
-U <integer> Specifies a sequence ruler font size.
-W <integer> The width of the map.
-x <string> Comma separated zoom values for image series.
-z <real> The factor to zoom in by.
Example usage: java -jar cgview.jar -f png -i cybercell.xml -o my_picture.png -h view_image.html.
Example usage: java -jar cgview.jar -i cybercell.xml -s directory_for_series -e true."""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_cgview_xml_builder_params(self,reading_frames=False,orfs=False, combined_orfs=False,orf_size=False,
                                      starts=False, stops=False, gc_content=False, gc_skew=False, at_skew=False,
                                      average=False, scale=False, step=False, window=False, size=False, linear=False,
                                      tick_density=False, title=False, details=False, legend=False,
                                      parse_reading_frame=False, show_queries=False, condensed=False,
                                      feature_labels=False, gene_labels=False, hit_labels=False, orf_labels=False,
                                      gene_decoration=False, global_label=False, use_opacity=False,
                                      show_sequence_features=False, draw_divider_rings=False, genes=False,
                                      analysis=False, blast=False,verbose=False, log=False):
        """cgview_xml_builder.pl
This script requires bioperl-1.4 or newer.

This script accepts a variety of input files pertaining to microbial
genomes and generates an XML file for the CGView genome drawing
program. There are several command line options for specifying which
input files should be used, and for controlling which features should
be drawn.

The CGView software is available at:
http://bioinformatics.org/cgview/download.html

Stothard P, Wishart DS. Circular genome visualization and exploration
using CGView. Bioinformatics. 21:537-539.

To create a simple map, try the following:
------------------------------------------

perl cgview_xml_builder.pl -sequence sample_input/R_denitrificans.gbk -output R_denitrificans.xml -tick_density 0.7

java -jar -Xmx1500m ../cgview.jar -i R_denitrificans.xml -o R_denitrificans.png -f png

To create a more complex map, try the following:
------------------------------------------------

perl cgview_xml_builder.pl -sequence sample_input/R_denitrificans.gbk -output R_denitrificans_b.xml -orfs T -at_content T -at_skew T -genes sample_input/R_denitrificans.cogs

java -jar -Xmx1500m ../cgview.jar -i R_denitrificans_b.xml -o R_denitrificans_b.png -f png


Note:
-----
There are numerous options for displaying additional information on
the maps created using this script. These options are described in
detail below.

If CGView runs out of memory (usually when an x-large map is drawn),
increase the memory available to Java using '-Xmx' option. For
example, try '-Xmx2000m'

To see other examples, run the test.sh script. It may take more than
an hour for all the examples to be created.

To create smoother base composition plots, specify a larger sliding
window value using the '-window' option in cgview_xml_builder.pl

If the base composition plots appear to be comprised of lines, specify
a smaller step value using the '-step' option in cgview_xml_builder.pl

To reduce the number of tick marks, specify a smaller tick density
value using the '-tick_density' option in cgview_xml_builder.pl


Required command line parameters:
---------------------------------

-sequence - The microbial genome sequence in FASTA, EMBL, or GenBank
format. [File]. Required.

-output - The CGView XML file to create. [File]. Required.

Optional command line parameters:
---------------------------------
#######Open reading frame options:
#######---------------------------

-reading_frames - Whether the positions of start and stop codons
should be drawn. [T/F]. Default is F. Optional.

-orfs - Whether open reading frames (ORFs) should be drawn, with each
reading frame (1, 2, 3, -1, -2, -3) represented by a separate
ring. [T/F]. Default is F. Optional.

-combined_orfs - Whether open reading frames (ORFs) should be drawn,
with each strand (forward, reverse) represented by a separate
ring. [T/F]. Default is F. Optional.

-orf_size - The minimum length of ORFs (in codons) to show when using
the '-orfs' or '-combined_orfs' options. [Integer]. Default is
100. Optional.

-starts - The start codons to use when plotting open reading frames
or stop and start codons. [String]. The default value is
'atg|ttg|att|gtg|ctg'. Optional.

-stops - The stop codons to use when plotting open reading frames or
stop and start codons. [String]. The default value is
'taa|tag|tga'. Optional.

#######Base composition plot options:
#######------------------------------

-gc_content - Whether GC content should be shown. [T/F]. Default is
T. Optional.

-gc_skew - Whether GC skew should be shown. [T/F]. Default is
F. Optional.

-at_content - Whether AT content should be shown. [T/F]. Default is
F. Optional.

-at_skew - Whether AT skew should be shown. [T/F]. Default is
F. Optional.

-average - Whether the GC, GC skew, AT, and AT skew plots should show
the deviation of each value from the average for the entire
genome. The default method of plotting shows each value as
calculated. Specifying "-average" allows plots to better show regions
that differ from the rest of the genome, but the results cannot be
easily compared between genomes. [T/F]. Default is T. Optional.

-scale - Whether the GC, GC skew, AT, and AT skew plots should be
scaled to fill the available Y-axis space on the map. This scaling
allows differences to be observed more easily, but the results cannot
be easily compared between genomes. [T/F]. Default is T. Optional.

-step - The step value to use when generating the GC, GC skew, AT,
and AT skew plots. This value should be decreased (to a minimum of 1)
if in the final map the lines comprising the plots can be
seen. [Integer]. Default is to let program choose step
value. Optional.

-window - The size of the sliding window for base composition
plots. Using a larger window size gives smoother graphs, but may hide
details. [Integer]. Default is to let program choose step
value. Optional.

#######Map appearance options:
#######------------------------------

-size - The size of the map. [small/medium/large/x-large]. Default is
medium. Optional.

-linear - Whether this genome is linear. Linear genomes are drawn as
a circle with a line drawn between the start and end of the
sequence. [T/F]. Default is to read this setting from the GenBank or
EMBL file, if available, otherwise the value is set to F. Optional.

-tick_density - The density of the tick marks on the map. Use a
smaller value to make the ticks less dense. [Real between 0 and
1]. Default is 0.5.

-title - A title for the sequence, to appear on the
map. [String]. Default is to obtain a title from the input sequence
file (for FASTA, GenBank, and EMBL input). Optional.

-details - Whether a sequence information legend should be
drawn. [T/F]. Default is T. Optional.

-legend - Whether a feature legend should be drawn. [T/F]. Default is
T. Optional.

-parse_reading_frame - Whether BLAST results should be split into
separate feature rings on the map, based on the reading frame and
strand of the query. Requires specially formatted BLAST
results. [T/F]. Default is F. Optional.

-show_queries - Whether faint boxes should be drawn to indicate the
positions of the BLAST queries relative to the genome
sequence. [T/F]. Default is F. Optional.

-condensed - Whether thin feature rings should be used regardless of
the size of the map. This option may be useful when numerous feature
rings are drawn. [T/F]. Default is F. Optional.

-feature_labels - Whether feature labels read from the GenBank or
EMBL file should be drawn. [T/F]. Default is F. Optional.

-gene_labels - Whether labels read using the '-genes' or
'-expression' option should be drawn. [T/F]. Default is F. Optional.

-hit_labels - Whether labels for BLAST hits read using the '-blast'
option should be drawn. [T/F]. Default is F. Optional.

-orf_labels - Whether labels for ORFs that are drawn using the
'-orfs' or '-combined_orfs' should be shown. [T/F]. Default is
F. Optional.

-gene_decoration - Whether genes should be drawn as an arc or as an
arrow. [String]. Default is 'arrow'.

-global_label - Controls how drawing a zoomed map affects labels. Set
to T to always show labels, F to always show no labels, or 'auto' to
show labels when a zoomed map is drawn. When set to F, no labels are
shown, regardless of the other label settings (-feature_labels,
-gene_labels, -hit_labels, and -orf_labels). When set to T, labels are
shown for those label settings that are set to T. When set to auto,
labels are shown for those label settings that are T only when a
zoomed map is drawn. [T/F/auto]. Default is T.

-use_opacity - Whether BLAST hits should be drawn with partial opacity,
so that overlapping hits can be visualized. [T/F]. Default is F.

-show_sequence_features - Whether to draw features contained in the
supplied '-sequence' file, if it is a GenBank or EMBL
file. [T/F]. Default is T.

-draw_divider_rings - Whether to draw divider rings between feature
 rings. [T/F]. Default is F.

#######Data source options:
#######------------------------------

-genes - One or more files containing gene position information for
the genes in the genome. The file should be tab-delimited or
comma-delimited and should have the following column titles, in the
following order: 'seqname', 'source', 'feature', 'start', 'end',
'score', 'strand', 'frame'. The first line in the file must be the
column titles. For a given entry, 'seqname' should be the name of the
gene, 'feature' should be the type of gene (CDS, rRNA, tRNA, other) or
the single letter COG category (J for example). 'start' and 'end'
should be integers between 1 and the length of the sequence, and the
'start' value should be less than or equal to the 'end' regardless of
the 'strand' value. The 'strand' value should be '+' for the forward
strand and '-' for the reverse strand. All other values can be given
as '.' or left blank, since they are ignored. These column titles are
based on the specification of the GFF file format. If 'start' and
'end' values are not supplied, but a 'seqname' is given, this script
will attempt to get the 'start' and 'end' values from the sequence
file. [Files]. Optional. Multiple files can be supplied using the
genes option, as in the following example:

perl cgview_xml_builder.pl -sequence sample_input/R_denitrificans.gbk -output R_denitrificans.xml -tick_density 0.7 -genes file1.txt file2.txt

See http://www.sanger.ac.uk/Software/formats/GFF/ for more information
on the GFF format.

-analysis - One or more files containing gene expression information
for the genes in the genome. The file should be tab-delimited or
comma-delimited and should have the following column titles, in the
following order: 'seqname', 'source', 'feature', 'start', 'end',
'score', 'strand', 'frame'. The first line in the file must be the
column titles. For a given entry, only the 'start', 'end', 'strand',
and 'score' values are required. 'start' and 'end' should be integers
between 1 and the length of the sequence, and the 'start' value should
be less than or equal to the 'end' regardless of the 'strand'
value. The 'strand' value should be '+' for the forward strand and '-'
for the reverse strand. The 'score' value should be a real
number, positive or negative. The other values can be given as '.' or
left blank. These column titles are based on the specification of the
GFF file format. If 'start' and 'end' values are not supplied, but a
'seqname' is given, this script will attempt to get the 'start' and
'end' values from the sequence file. [Files]. Optional. Multiple files
can be supplied using the analysis option, as in the following example:

perl cgview_xml_builder.pl -sequence sample_input/R_denitrificans.gbk -output R_denitrificans.xml -tick_density 0.7 -analysis file1.txt file2.txt

See http://www.sanger.ac.uk/Software/formats/GFF/ for more information
on the GFF format.

-blast - One or more files of BLAST results to display. This option
is used to display BLAST results from the local_blast_client.pl and
remote_blast_client.pl scripts. These are available at:
http://www.ualberta.ca/~stothard/software.html. When using the above
scripts, the query should be split into multiple smaller sequences,
using one of the following scripts: get_orfs.pl, get_cds.pl, or
sequence_to_multi_fasta.pl. These are also available at the above
URL. The file containing the multiple sequences is then BLASTed using
local_blast_client.pl or remote_blast_client.pl. The BLAST results files
can be passed to cgview_xml_builder using this option. The percent
identity of each hit is plotted. [Files]. Optional. Multiple files can
be supplied using the blast option, as in the following example:

perl cgview_xml_builder.pl -sequence sample_input/R_denitrificans.gbk -output R_denitrificans.xml -tick_density 0.7 -blast file1.txt file2.txt

#######Other options:
#######------------------------------

-verbose - Whether program progress should be written to standard
output. [T/F]. Default is T. Optional.

-log - A log file for recording progress and error
messages. [File]. Default is to not write a log file.

Exit status:
------------

If the script encounters an error it exits with a status of 1. If no
error is encountered the script exits with a status of 0 upon
completing.

Written by Paul Stothard, University of Alberta

stothard@ualberta.ca"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, postfix="", subcmd="cgview_xml_builder"):
        if subcmd == "cgview_xml_builder":
            out = sample_io.id + "_cgview.xml"
            self.output_type = "xml"
            self.cmd = ["perl", "/usr/local/bin/cgview_xml_builder.pl", "-sequence", sample_io.files[0].name, "-output", out]\
                       + self.get_perl_params("cgview_xml_builder_params")

        elif subcmd == "cgview":
            out = sample_io.id + postfix + ".png"
            self.output_type = "png"
            self.cmd = ["cgview", "-i", sample_io.files[0].name, "-o", out] + self.get_opt_params("cgview_params")

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io):
        pass