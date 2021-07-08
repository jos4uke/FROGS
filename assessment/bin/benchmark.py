opyright (C) 2021 INRAE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = 'Plateforme bioinformatique Toulouse - Sigenae Jouy en Josas'
__copyright__ = 'Copyright (C) 2021 INRAE'
__license__ = 'GNU General Public License'
__version__ = '1.1.1'
__email__ = ''
__status__ = 'prod'


import os
import argparse
import subprocess

##################################################################################################################################################
#
# FUNCTIONS
#
##################################################################################################################################################
def exec_cmd( cmd, output=None ):
    """
    @summary: Execute command line and check status.
    @param cmd: [str] Command line.
    @param output: [str] Path to the file where the stdout will be written.
    """
    if output is None:
        print cmd
        subprocess.check_call( cmd, shell=True )
    else:
        print cmd + " > " + output
        subprocess.check_call( cmd + " > " + output, shell=True )


def untar(tarfile, outdir):
    """
    @summary: Extract files from tar.
    @param tarfile: [str] Path to the tar file.
    @param outdir: [str] Path to the output directory.
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    exec_cmd(
        "tar zxvf" \
        + " " + tarfile \
        + " -C " + outdir
    )
    exec_cmd( "gzip -f -d " + os.path.join(outdir, "*.fastq.gz") )


def clusters_assessment(in_biom, in_fasta, origin, reads_dir, output, sample_separator):
    """
    @summary: Launch clusters metrics processing.
    @param in_biom: [str] Path to the BIOM file processed.
    @param in_fasta: [str] Path to the sequence file corresponding to the BIOM file.
    @param origin: [str] Path to the sequence file provided to the simulation workflow.
    @param reads_dir: [str] Path to the directory with one sequence file by sample (reads produced by simulation).
    @param output: [str] Path to the report.
    @param sample_separator: [str] Separator between sample name and the rest of the filename.
    """
    exec_cmd(
        "clustersAssessment.py " \
        + " --biom " + in_biom \
        + " --fasta " + in_fasta \
        + " --origin " + origin \
        + " --reads-dir " + reads_dir \
        + " --sample-sep '" + sample_separator + "'",
        output
    )


def affiliations_assessment(fasta_databank, in_biom, in_fasta, dataset_in_dir, duplicated_sequences, output, sample_separator, taxonomy_key, is_multi_affi):
    """
    @summary: Launch affiliations metrics processing.
    @param fasta_databank: [str] Path to the databank used in affiliation.
    @param in_biom: [str] Path to the BIOM file processed.
    @param in_fasta: [str] Path to the sequence file corresponding to the BIOM file.
    @param dataset_in_dir: [str] Path to the directory with count by initial sequence in simulation.
    @param duplicated_sequences: [str] Path to the file with by line the list of IDs of initial sequences with the same sequence.
    @param output: [str] Path to the report.
    @param sample_separator: [str] Separator between sample name and the rest of the filename.
    @param taxonomy_key: [str] The metadata tag used for store taxonomy in the BIOM file.
    @param is_multi_affi: [bool] True if the taxonomy is produced by FROGS multi-affiliations.
    """


def frogs(fasta_databank, reads_directory, out_biom, out_fasta, min_length, max_length, nb_cpus):
    """
    @summary: Launch FROGS pipeline.
    @param fasta_databank: [str] Path to the databank used in affiliation.
    @param reads_directory: [str] Path to the directory with one sequence file by sample (reads produced by simulation).
    @param out_biom: [str] Path to the outputed BIOM file.
    @param out_fasta: [str] Path to the outputed sequences file.
    @param min_length: [int] Amplicon minimum length.
    @param max_length: [int] Amplicon maximum length.
    @param nb_cpus: [int] Number of used CPUs.
    """
    exec_cmd(
        os.sep.join([args.frogs_directory, "assessment", "bin", "frogs.py"]) \
        + " --min-length " + str(min_length) \
        + " --max-length " + str(max_length) \
        + " --already-contiged " \
        + " --without-primers " \
        + " --samples-files " + os.path.join(reads_directory, "*.fastq") \
        + " --affiliation-databank " + fasta_databank \
        + " --output-biom " + out_biom \
        + " --output-fasta " + out_fasta \
        + " --nb-cpus " + str(nb_cpus)
    )


def rAnomaly(amplicon, f_trunclen, r_trunclen, trim_l, trim_r, verbose, fastqPath, paired, compress, idDb, metadata, domain):
    exec_cmd(
        python $wrapper \
     --amplicon 16S \
     --f_trunclen 240 --r_trunclen 240 \
     --trim_l 15 --trim_r 0 --verbose 3 \
     --fastqPath "$reads_dir" \
     --paired True \
     --compress True \
     --idDb "$id_db" \
     --metadata "$mdata" \
     --domain "Bacteria"
   )    


def frogs_affiliation(fasta_databank, in_biom, in_fasta, output_biom, nb_cpus):
    """
    @summary: launch FROGS affiliation on BIOM file.
    @param fasta_databank: [str] Path to the databank used in affiliation.
    @param in_biom: [str] Path to the BIOM file.
    @param in_fasta: [str] Path to the sequences file corresponding to the BIOM file.
    @param out_biom: [str] Path to the outputed BIOM file.
    @param nb_cpus: [int] Number of used CPUs.
    """
    exec_cmd( "affiliation_OTU.py" + \
        " --reference " + fasta_databank + \
        " --input-fasta " + in_fasta + \
        " --input-biom " + in_biom + \
        " --output-biom " + output_biom + \
        " --summary " + output_biom + ".affiliationOTU_summary.html" + \
        " --log-file " + output_biom + ".affiliationOTU_log.txt" + \
        " --nb-cpus " + str(nb_cpus) + \
        " --java-mem 20" )


##################################################################################################################################################
#
# MAIN
#
##################################################################################################################################################
if __name__ == "__main__":
    # Manage parameters
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
Launch assessment on simulated datasets.
Used datasets for this assessment must be stored in following structure:
  <nb>sp/dataset_<nb>/<primers>/dataset.fasta
                                <distribLaw>/dataset.tar.gz
                                             sample<nb>-100sp-Powerlaw_ranks.txt'''
    )
    parser.add_argument( '--nb-sp', type=int, nargs='+', default=[20, 100, 200, 500, 1000], help='Numbers of species used in assessment. Example: with "--nb-sp 20 100" only the sub-folders 20sp and 100sp are used in assessment. [Default: 20, 100, 200, 500, 1000]' )
    parser.add_argument( '--datasets', type=int, nargs='+', default=[1, 2, 3, 4, 5], help='IDs of datasets used in assessment. Example: with "--datasets 1 5" only the sub-folders dataset_1 and dataset_5 are used in assessment. [Default: 1, 2, 3, 4, 5]' )
    parser.add_argument( '--primers', type=str, nargs='+', default=["V4V4", "V3V4"], help='Primers used in assessment. Example: with "--primers V4V4" only the sub-folder V4V4 is used in assessment. [Default: V4V4, V3V4]' )
    parser.add_argument( '--distribution-laws', type=str, nargs='+', default=["powerlaw", "uniform"], help='Distribution laws used in assessment. Example: with "--distribution-laws powerlaw" only the sub-folder powerlaw is used in assessment. [Default: powerlaw, uniform].' )
    parser.add_argument( '--pipelines', type=str, nargs='+', default=["frogs", "rAnomaly"], help='launched pipelines. Example: with "--pipelines frogs" only the frogs is launched. [Default: frogs, rAnomaly].' )
    parser.add_argument( '-p', '--nb-cpus', type=int, default=1, help='The maximum number of CPUs used. [Default: 1]' )
    parser.add_argument( '-v', '--version', action='version', version=__version__)
    # Inputs
    group_input = parser.add_argument_group('Inputs')
    group_input.add_argument( '--datasets-directory', required=True, help='Path to the datasets directory. See general description for a structure example.' )
    group_input.add_argument( '--frogs-directory', required=True, help='Path to the FROGS install directory.' )
    group_input.add_argument( '--affiliation-databank-fasta', required=True, help='Path to the affiliation databank (format: fasta). The description of sequences must be the taxonomy.' )
    group_input.add_argument( '--affiliation-databank-udb', help='Path to the affiliation databank for uparse (format: udb). In uparse pipeline the affiliation is processed with FROGS affiliation tool and if this option is provided the affiliation is also processed with Utax.' )
    group_input.add_argument( '--affiliation-databank-tax', help='Path to the affiliation databank taxonomy for mothur (format: mothur tax). In mothur pipeline the affiliation is processed with FROGS affiliation tool and if this option is provided the affiliation is also processed with mothur classify.' )
    # Outputs
    group_output = parser.add_argument_group('Outputs')
    group_output.add_argument( '--output-directory', required=True, help='Path to the output directory.' )
    args = parser.parse_args()

# Add in path
    add_path = ["assessment/bin", "libexec", "app"]
    add_path_str = args.frogs_directory + os.sep + (os.pathsep + args.frogs_directory + os.sep).join(add_path)
    os.putenv('PATH', add_path_str + os.pathsep + os.getenv('PATH'))

    # Process
    for current_primers in args.primers:
        min_length = primers_param[current_primers]["min_length"]
        max_length = primers_param[current_primers]["max_length"]
        pcr_start = primers_param[current_primers]["pcr_start"]
        pcr_end = primers_param[current_primers]["pcr_end"]
        kept_start = primers_param[current_primers]["kept_start"]
        kept_end = primers_param[current_primers]["kept_end"]
        for current_nb_sp in args.nb_sp:
            for dataset_idx in args.datasets:
                for current_distribution in args.distribution_laws:
                    dataset_out_dir = os.sep.join([args.output_directory, str(current_nb_sp) + "sp", "dataset_" + str(dataset_idx), current_primers, current_distribution])
                    dataset_in_dir = os.sep.join([args.datasets_directory, str(current_nb_sp) + "sp", "dataset_" + str(dataset_idx), current_primers, current_distribution])
                    dataset_fasta = os.path.join(os.path.dirname(dataset_in_dir), "dataset.fasta")

                    # Create dir
                    if not os.path.exists(dataset_out_dir):
                        os.makedirs(dataset_out_dir)

                    # Untar unzip dataset
                    reads_directory = os.path.join(dataset_out_dir, "reads")
                    untar( os.path.join(dataset_in_dir, "dataset.tar.gz"), reads_directory )

                    # Uniq
                    duplicated_sequences = os.path.join(dataset_out_dir, "duplicated_sequences.txt")
                    exec_cmd(
                        os.sep.join([args.frogs_directory, "assessment", "bin", "duplicatedSequences.py"]) \
                        + " --input " + os.path.join(os.path.dirname(dataset_in_dir), "dataset.fasta") \
                        + " --output " + duplicated_sequences
                    )

                    # FROGS
                    if "frogs" in args.pipelines:
                        #    Set files and directory
                        frogs_out_dir = os.path.join(dataset_out_dir, "frogs")
                        if not os.path.exists(frogs_out_dir):
                            os.makedirs(frogs_out_dir)
                        frogs_biom = os.path.join(frogs_out_dir, "frogs.biom")
                        frogs_fasta = os.path.join(frogs_out_dir, "frogs.fasta")
                        frogs_assess_affi = os.path.join(frogs_out_dir, "frogs_affiResults.txt")
                        frogs_assess_clst = os.path.join(frogs_out_dir, "frogs_OTUResults.txt")
                        #    Execution and assessment
                        frogs(args.affiliation_databank_fasta, reads_directory, frogs_biom, frogs_fasta, min_length, max_length, args.nb_cpus)
                        affiliations_assessment(args.affiliation_databank_fasta, frogs_biom, frogs_fasta, dataset_in_dir, duplicated_sequences, frogs_assess_affi, "_", "blast_taxonomy", True)
                        clusters_assessment(frogs_biom, frogs_fasta, dataset_fasta, reads_directory, frogs_assess_clst, "_")


                    #rAnomaly
                    if "rAnomaly" in args.pipelines:
                        #    Set files and directory
                        frogs_out_dir = os.path.join(dataset_out_dir, "rAnomaly")
                        if not os.path.exists(frogs_out_dir):
                            os.makedirs(frogs_out_dir)
                        frogs_biom = os.path.join(frogs_out_dir, "rAnomaly.biom")
                        frogs_fasta = os.path.join(frogs_out_dir, "rAnomaly.fasta")
                        frogs_assess_affi = os.path.join(frogs_out_dir, "rAnomaly_affiResults.txt")
                        frogs_assess_clst = os.path.join(frogs_out_dir, "rAnomaly_OTUResults.txt")
                        #    Execution and assessment
                        rAnomaly(args.amplicon, args.f_trunclen, args.r_trunclen, args.trim_l, args.trim_r, args.verbose, args.fastqPath, args.paired, args.compress, args.idDb, args.metadata, args.domain)

~

































