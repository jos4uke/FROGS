#Copyright (C) 2021 INRA
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

__author__ = 'Plateforme bioinformatique EGFV'
__copyright__ = 'Copyright (C) 2021 INRAE'
__license__ = 'GNU General Public License'
__version__ = '1.0.0'
__email__ = ''
__status__ = 'alpha'

import os
import sys
import time
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
        print "\t[rAnomaly CMD]:\t" + cmd
        subprocess.check_call( cmd, shell=True )
    else:
        print "\t[rAnomaly CMD]:\t" + cmd + " > " + output
        subprocess.check_call( cmd + " > " + output, shell=True )


def dict_to_string(dictio):
    carac2 = ""
    for (k,v) in dictio.items():
       #  k = "--" + k
       # carac = k + " " + v
        carac2+=" --{key} {val} \ \n ".format(key=k, val=v)
    return(carac2)

##################################################################################################################################################
#
# MAIN
#
##################################################################################################################################################
if __name__ == "__main__":
    print "[SOFTWARE]:\trAnomaly"
    start_time = time.time()


# Parser
    parser = argparse.ArgumentParser(description='Launch rAnomaly workflow.')
    
# Global parameters
    group_global = parser.add_argument_group('Global')
    group_global.add_argument('--workingDirectory', type=str, help='Setting the working directory from the directory where the script is running')
    group_global.add_argument('--verbose', type=int, default=1, help='Verbose level (1: quiet, 3: verbal)')
    group_global.add_argument('--plot', action='store_true', default=False, help='Enabling creation or not of a plot (default is FALSE)')
    group_global.add_argument('--returnValue', action='store_true', default=True, help='Defining if the value is return or not (default is TRUE)')
    group_global_ns = parser.parse_args([])
    group_global_dict = vars(group_global_ns)     
    test = dict_to_string(group_global_dict)
    print(test)


# Dada2 parameters
    group_dada2 = parser.add_argument_group('Dada2')
    group_dada2.add_argument('--amplicon', type=str, required=True, help='Type of amplicon (16S or ITS)')
    group_dada2.add_argument('--fastqPath', type=str, required=True, help='Path to fastq files parent directory')
    group_dada2.add_argument('--compress', action='store_true', default=False, help='Reads files are compressed (.gz / default is FALSE)')
    group_dada2.add_argument('--paired', action='store_true', default=False, help='Boolean for Illumina Paired End Reads (default is FALSE)')
    group_dada2.add_argument('--torrent_single', action='store_true', default=False, help='Boolean to choose between Illumina Paired End SOP or Torrent Single End SOP (default is FALSE)')
    group_dada2.add_argument('--f_trunclen', type=str, default=None, help='Forward read tuncate length (only for paired end 16S / default is NULL")')
    group_dada2.add_argument('--r_trunclen', type=str, default=None, help='Reverse read tuncate length (only for paired end 16S / default is NULL")')
    group_dada2.add_argument('--f_primer', type=str, default=None, help='Forward primer sequence (only for ITS / default is NULL)')
    group_dada2.add_argument('--r_primer', type=str, default=None, help='Reverse primer sequence (only for ITS / default is NULL)')
    group_dada2.add_argument('--trim_l', type=str, default=None, help='Trim left size (default is NULL)')
    group_dada2.add_argument('--trim_r', type=str, default=None, help='Trim right size (default is NULL)')
    group_dada2.add_argument('--orient_torrent', type=str, default=None, help='Forward primer sequence to orient all reads to same strand (default is NULL)')
    group_dada2.add_argument('--dadapool', type=str, default="pseudo", help='Option for dada function (FALSE, TRUE or pseudo), default is pseudo')

# Taxonomy assignment parameters
    group_taxonomy = parser.add_argument_group('Taxonomy')
    group_taxonomy.add_argument('--idDb', type=str, required=True, help='ID of the database, could be a file path or a pair of file path separated by a comma')
    group_taxonomy.add_argument('--confidence', type=int, default=50, help='Bootstrap threshold 0...100 (default is 50)')
    group_taxonomy.add_argument('--ncpu', type=int, default=1, help='Number of cpus to use (default is 1)')
    
# Phyloseq parameters
    group_phyloseq = parser.add_argument_group('Phyloseq')
    group_phyloseq.add_argument('--metadata', type=str, required=True, help='Path to the metadata file')
    group_phyloseq.add_argument('--tree', action='store_true', default=True, help='Results of generate_tree_fun() (default is TRUE)')

# Decontamination parameters
    group_decontamination = parser.add_argument_group("Decontamination")
    group_decontamination.add_argument('--domain', type=str, required=True, default=None, help='16S region or ITS region (Bacteria or Fungi), default is NULL')
    group_decontamination.add_argument('--skip', action='store_true', default=True, help='Skip decontam step and process basic filters (depth per samples, prevalence, frequence / default is TRUE)')
    group_decontamination.add_argument('--number', type=int, default=100, help='Minimum number of reads per sample (default is 100)')
    group_decontamination.add_argument('--freq', type=int, default=0.00005, help='Minimum prevalence of an ASV in samples to be kept (default is 0.00005)')
    group_decontamination.add_argument('--prev', type=int, default=2, help='Minimum prevalence of an ASV in samples to be kept (default is 2)')
    group_decontamination.add_argument('--unassigned', action='store_true', default=True, help='Unassigned kingdom or phylum fitering (default is TRUE)')
    group_decontamination.add_argument('--krona', action='store_true', default=False, help='Export krona plot (default is FALSE)')
    group_decontamination.add_argument('--column', type=str, default="", help='Column name from sample_variables(data) for type of sample (control or sample). If informed, function filters control samples')
    group_decontamination.add_argument('--ctrl_identifier', type=str, default='control', help='Idendifier name for controls')
    group_decontamination.add_argument('--spl_identifier', type=str, default='sample', help='Idendifier name for samples')
    group_decontamination.add_argument('--batch', type=str, default=None, help='Batch column name for independent contaminant identification')
    group_decontamination.add_argument('--method', type=str, default='frequency', required=True, help='Method for contaminant identification (frequency, prevalence, combined, both, either / default is frequency)')
    group_decontamination.add_argument('--threshold', type=int, default=0.1, required=True, help='Threshold for DECONTAM prevalence filtering (default is 0.1)')
    group_decontamination.add_argument('--concentration', type=str, default=None, help='Column name for ADN concentration (default is NULL)')
    group_decontamination.add_argument('--manual_cont_rank', type=str, default='Genus', help='Rank of taxa to remove, inform ASV to remove ASV (default is Genus)')
    group_decontamination.add_argument('--manual_cont', type=str, default=None, help='Comma separated list of Genus to remove (eg. g__Enterococcus,g__Cellulosimicrobium,g__Serratia / default is NULL)')
    args = parser.parse_args()

'''
exec_cmd("rANOMALY_taxo_wrapper.R" + \
     global_options + \
     dada2_options + \
     taxonomy_options + \
     phyloseq_options)
'''

print("workingDirectory",args.workingDirectory)


end_time = time.time()
print "\t[rANOMALY EXEC_TIME]:\t" + str(end_time - start_time)











