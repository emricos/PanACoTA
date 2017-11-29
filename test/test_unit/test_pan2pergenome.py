#!/usr/bin/env python3
# coding: utf-8

"""
Unit tests for the pan_to_pergenome submodule in align module
"""
import os
import shutil

import pytest

import genomeAPCAT.align_module.pan_to_pergenome as p2p


ALPATH = os.path.join("test", "data", "align")
EXPPATH = os.path.join(ALPATH, "exp_files")
TESTPATH = os.path.join(ALPATH, "test_files")
ALL_PROTS = {"ESCO1": {"ESCO1_00001": '1',
                       "ESCO1_00002": '4'},
             "ESCO2": {"ESCO2_00001": '1',
                       "ESCO2_22": '2',
                       "ESCO2_456": '4',
                       "ESCO2_46": '3'},
             "ESCO3": {"ESCO3_1": '2',
                       "ESCO3_12": '1',
                       "ESCO3_4564": '3',
                       "ESCO3_00123": '4',
                       "ESCO3_8": '2'},
             "ESCO4": {"ESCO4_00001": '1',
                       "ESCO4_00002": '4',
                       "ESCO4_00003": '3',
                       "ESCO4_00004": '2',
                       "ESCO4_00006": '4'},
             "ESCO5": {"ESCO5_1": '1',
                       "ESCO5_2": '3',
                       "ESCO5_3": '2',
                       "ESCO5_4": '4',
                       "ESCO5_5": '2'},
             "ESCO6": {"ESCO6_1": '4',
                       "ESCO6_2": '3',
                       "ESCO6_3": '1'}}
FAM_GENOMES = {'1': ["ESCO1", "ESCO2", "ESCO3", "ESCO4", "ESCO5", "ESCO6"],
               '2': ["ESCO2", "ESCO3", "ESCO4", "ESCO5"],
               '3': ["ESCO2", "ESCO3", "ESCO4", "ESCO5", "ESCO6"],
               '4': ["ESCO1", "ESCO2", "ESCO3", "ESCO4", "ESCO5", "ESCO6"]}
SEVERAL = {'1': [],
           '2': ["ESCO3", "ESCO5"],
           '3': [],
           '4': ["ESCO4"]}
ALL_GENOMES = ["ESCO1", "ESCO2", "ESCO3", "ESCO4", "ESCO5", "ESCO6"]


def test_get_per_genome(caplog):
    """
    Test that when giving a persistent genome file and a list of genomes,
    it creates all expected files in output/Listdir
    """
    pers = os.path.join("test", "data", "persgenome", "exp_files", "exp_pers-floor-mixed.txt")
    list_gen = os.path.join(TESTPATH, "listfile.txt")
    dname = "TEST-all-gembase"
    outdir = "test_get_per_genome"
    all_genomes, aldir, listdir, fams = p2p.get_per_genome(pers, list_gen, dname, outdir)
    assert ("Reading PersGenome and constructing lists of missing genomes "
            "in each family") in caplog.text
    exp_al = os.path.join(outdir, "Align-TEST-all-gembase")
    exp_list = os.path.join(outdir, "List-TEST-all-gembase")
    assert exp_al == aldir
    assert os.path.isdir(aldir)
    assert exp_list == listdir
    assert os.path.isdir(listdir)
    exp_genomes = ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002", "GENO.1216.00003"]
    assert all_genomes == exp_genomes
    exp_fams = ['1', '3', '5', '8', '10', '11', '12']
    assert list(fams) == exp_fams
    shutil.rmtree(outdir)


def test_prot_per_strain():
    """
    Test parser of persistent genome file
    """
    pers = os.path.join("test", "data", "persgenome", "exp_files", "exp_pers-floor-mixed.txt")
    all_prots, fams_genomes, several = p2p.proteins_per_strain(pers)
    exp_several = {'1': ["GENO.1216.00002"],
                   '3': [],
                   '5': [],
                   '8': [],
                   '10': [],
                   '11': [],
                   '12': ["GENO.1216.00003"]}
    assert several == exp_several
    exp_fams = {'1': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002", "GENO.1216.00003"],
                '3': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002", "GENO.1216.00003"],
                '5': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002", "GENO.1216.00003"],
                '8': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002"],
                '10': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002"],
                '11': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002"],
                '12': ["GEN4.1111.00001", "GENO.0817.00001", "GENO.1216.00002", "GENO.1216.00003"]}
    assert fams_genomes == exp_fams
    exp_prots = {"GEN4.1111.00001": {"GEN4.1111.00001.b0001_00001": '1',
                                     "GEN4.1111.00001.b0001_00009": '3',
                                     "GEN4.1111.00001.i0001_00002": '5',
                                     "GEN4.1111.00001.i0001_00007": '8',
                                     "GEN4.1111.00001.i0001_00004": '10',
                                     "GEN4.1111.00001.i0001_00005": '11',
                                     "GEN4.1111.00001.i0001_00008": '12'
                                     },
                 "GENO.0817.00001": {"GENO.0817.00001.b0001_00002": '1',
                                     "GENO.0817.00001.b0002_00011": '3',
                                     "GENO.0817.00001.b0002_00003": '5',
                                     "GENO.0817.00001.i0002_00009": '8',
                                     "GENO.0817.00001.i0002_00004": '10',
                                     "GENO.0817.00001.i0002_00005": '11',
                                     "GENO.0817.00001.i0002_00010": '12'
                                     },
                 "GENO.1216.00002": {"GENO.1216.00002.b0001_00001": '1',
                                     "GENO.1216.00002.i0001_00002": '1',
                                     "GENO.1216.00002.b0002_00010": '3',
                                     "GENO.1216.00002.i0001_00003": '5',
                                     "GENO.1216.00002.b0001_00008": '8',
                                     "GENO.1216.00002.i0001_00005": '10',
                                     "GENO.1216.00002.i0001_00006": '11',
                                     "GENO.1216.00002.b0002_00009": '12'
                                     },
                 "GENO.1216.00003": {"GENO.1216.00003.i0001_00003": '1',
                                     "GENO.1216.00003.i0001_01010": '3',
                                     "GENO.1216.00003.i0080_00010": '5',
                                     "GENO.1216.00003.i0001_00004": '12',
                                     "GENO.1216.00003.i0001_01000": '12'
                                     }
                 }
    assert all_prots == exp_prots


def test_prot_per_strain_member_bis(caplog):
    """
    Test parser of persistent genome file when a same member is in 2 different families
    """
    pers = os.path.join(TESTPATH, "pers_genome_member-bis.txt")
    all_prots, fams_genomes, several = p2p.proteins_per_strain(pers)
    assert "problem: ESCO2_2 already exists, in family 5. Conflict with family 32" in caplog.text
    exp_several = {'1': [], '5': [], '12': [], '32': []}
    assert several == exp_several
    exp_fams = {'1': ["ESCO_1", "ESCO2", "ESCO3", "ESCO4"], '5': ["ESCO_1", "ESCO2", "ESCO4"],
                '12': ["ESCO_1", "ESCO2", "ESCO3"], '32': ["ESCO_1", "ESCO2", "ESCO3", "ESCO4"]}
    assert fams_genomes == exp_fams
    exp_prots = {"ESCO_1": {"ESCO_1_1": '1', "ESCO_1_2": '5', "ESCO_1_3": '12', "ESCO_1_4": '32'},
                 "ESCO2": {"ESCO2_1": '1', "ESCO2_2": '32', "ESCO2_3": '12'},
                 "ESCO3": {"ESCO3_1": '1', "ESCO3_3": '12', "ESCO3_4": '32'},
                 "ESCO4": {"ESCO4_1": '1', "ESCO4_3": '5', "ESCO4_4": '32'}}
    assert all_prots == exp_prots


def test_get_genomes():
    """
    Test parser of list of genomes
    """
    lstfile = os.path.join("test", "data", "annotate", "exp_files", "results_test_func-default",
                           "LSTINFO-list_genomes-func-test-default.lst")
    all_genomes = p2p.get_all_genomes(lstfile)
    assert all_genomes == ["ESCO.1015.00001", "ESCO.1116.00002", "GENO.1015.00001"]


def test_write_getentry():
    """
    Test that when giving a list of genomes with their persistent gene names,
    it creates all expected files.
    """
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    p2p.write_getentry_files(ALL_PROTS, SEVERAL, listdir, aldir, dname, ALL_GENOMES)
    # Check creation and content of all files
    genfiles = [os.path.join(listdir, "{}-getEntry_gen_ESCO{}.txt".format(dname, num)) for num in
                range(1, 7)]
    expgens = [os.path.join(EXPPATH, "exp_getentry-gen-ESCO{}.txt".format(num)) for num in
               range(1, 7)]
    for fexp, fout in zip(expgens, genfiles):
        check_list(fexp, fout)
    prtfiles = [os.path.join(listdir, "{}-getEntry_prt_ESCO{}.txt".format(dname, num)) for num in
                range(1, 7)]
    expprts = [os.path.join(EXPPATH, "exp_getentry-prt-ESCO{}.txt".format(num)) for num in
               range(1, 7)]
    for fexp, fout in zip(expprts, prtfiles):
        check_list(fexp, fout)
    shutil.rmtree(listdir)


def test_write_getentry_error(caplog):
    """
    Test that when giving a list of genomes with their persistent gene names,
    but for 2 genomes, there is no persistent gene, it exists, with an error message
    """
    all_prots = {"ESCO1": {"ESCO1_00001": '1',
                           "ESCO1_00002": '4'},
                 "ESCO2": {"ESCO2_00001": '1',
                           "ESCO2_22": '2',
                           "ESCO2_456": '4',
                           "ESCO2_46": '3'},
                 "ESCO3": {"ESCO3_1": '2',
                           "ESCO3_12": '1',
                           "ESCO3_4564": '3',
                           "ESCO3_00123": '4',
                           "ESCO3_8": '2'},
                 "ESCO6": {"ESCO6_1": '4',
                           "ESCO6_2": '3',
                           "ESCO6_3": '1'}}
    several = {'1': [],
               '2': ["ESCO3"],
               '3': [],
               '4': []}
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    with pytest.raises(SystemExit):
        p2p.write_getentry_files(all_prots, several, listdir, aldir, dname, ALL_GENOMES)
    assert ("There is not any protein for genome ESCO4 in any family! The program will close, "
            "please fix this problem to be able to run the alignments") in caplog.text
    assert ("There is not any protein for genome ESCO5 in any family! The program will close, "
            "please fix this problem to be able to run the alignments") in caplog.text
    # Check creation and content of all files
    genfiles = [os.path.join(listdir, "{}-getEntry_gen_ESCO{}.txt".format(dname, num)) for num in
                list(range(1, 4)) + [6]]
    expgens = [os.path.join(EXPPATH, "exp_getentry-gen-ESCO{}.txt".format(num)) for num in
               list(range(1, 4)) + [6]]
    for fexp, fout in zip(expgens, genfiles):
        check_list(fexp, fout)
    prtfiles = [os.path.join(listdir, "{}-getEntry_prt_ESCO{}.txt".format(dname, num)) for num in
                list(range(1, 4)) + [6]]
    expprts = [os.path.join(EXPPATH, "exp_getentry-prt-ESCO{}.txt".format(num)) for num in
               list(range(1, 4)) + [6]]
    for fexp, fout in zip(expprts, prtfiles):
        check_list(fexp, fout)
    shutil.rmtree(listdir)


def test_write_genome():
    """
    Test that given a genome, it writes the list of its proteins
    and genes in expected files.
    """
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    strain = "ESCO4"
    member4 = ALL_PROTS[strain]
    p2p.write_genome_file(listdir, aldir, dname, strain, member4, SEVERAL)

    # Check creation of files and content
    fileprt = os.path.join(listdir, "{}-getEntry_prt_ESCO4.txt".format(dname))
    expprt = os.path.join(EXPPATH, "exp_getentry-prt-ESCO4.txt")
    check_list(expprt, fileprt)
    filegen = os.path.join(listdir, "{}-getEntry_gen_ESCO4.txt".format(dname))
    expgen = os.path.join(EXPPATH, "exp_getentry-gen-ESCO4.txt")
    check_list(expgen, filegen)
    # Remove output directory
    shutil.rmtree(listdir)


def test_write_genome_prt_exists():
    """
    Test that when only prt file exists, it overwrites it and generates
    expected prt and gen files
    """
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    strain = "ESCO4"
    member4 = ALL_PROTS[strain]

    # Create prt file
    fileprt = os.path.join(listdir, "{}-getEntry_prt_ESCO4.txt".format(dname))
    with open(fileprt, "w") as prtf:
        prtf.write("Wrong prt file\n")
    p2p.write_genome_file(listdir, aldir, dname, strain, member4, SEVERAL)

    # Check creation of files and content
    expprt = os.path.join(EXPPATH, "exp_getentry-prt-ESCO4.txt")
    check_list(expprt, fileprt)
    filegen = os.path.join(listdir, "{}-getEntry_gen_ESCO4.txt".format(dname))
    expgen = os.path.join(EXPPATH, "exp_getentry-gen-ESCO4.txt")
    check_list(expgen, filegen)
    # Remove output directory
    shutil.rmtree(listdir)


def test_write_genome_gen_exists():
    """
    Test that when only gen file exists, it overwrites it and generates
    expected prt and gen files
    """
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    strain = "ESCO4"
    member4 = ALL_PROTS[strain]
    # Create prt file
    filegen = os.path.join(listdir, "{}-getEntry_gen_ESCO4.txt".format(dname))
    with open(filegen, "w") as genf:
        genf.write("Wrong gen file\n")
    p2p.write_genome_file(listdir, aldir, dname, strain, member4, SEVERAL)

    # Check creation of files and content
    fileprt = os.path.join(listdir, "{}-getEntry_prt_ESCO4.txt".format(dname))
    expprt = os.path.join(EXPPATH, "exp_getentry-prt-ESCO4.txt")
    check_list(expprt, fileprt)
    expgen = os.path.join(EXPPATH, "exp_getentry-gen-ESCO4.txt")
    check_list(expgen, filegen)
    # Remove output directory
    shutil.rmtree(listdir)


def test_write_genome_gen_prt_exist(caplog):
    """
    Test that when gen and prt files already exist, it does not do anything.
    Those files will be used for next steps.
    """
    listdir = "Listdir"
    aldir = "Aldir"
    # Create align folder
    os.makedirs(listdir)
    dname = "TEST6"
    strain = "ESCO4"
    member4 = ALL_PROTS[strain]
    # Create gen and prt files
    filegen = os.path.join(listdir, "{}-getEntry_gen_ESCO4.txt".format(dname))
    with open(filegen, "w") as genf:
        genf.write("Wrong gen file\n")
    fileprt = os.path.join(listdir, "{}-getEntry_prt_ESCO4.txt".format(dname))
    with open(fileprt, "w") as prtf:
        prtf.write("Wrong prt file\n")
    p2p.write_genome_file(listdir, aldir, dname, strain, member4, SEVERAL)

    # Check log
    assert ("For genome ESCO4, {} and {} already exist. The program will use them to extract "
            "proteins and genes. If you prefer to rewrite them, use option "
            "-F (or --force).".format(fileprt, filegen)) in caplog.text

    # Check content of prt and gen has not changed
    with open(fileprt, "r") as prtf:
        lines = prtf.readlines()
        assert lines == ["Wrong prt file\n"]
    with open(filegen, "r") as prtf:
        lines = prtf.readlines()
        assert lines == ["Wrong gen file\n"]

    # Remove output directory
    shutil.rmtree(listdir)


def check_list(expfile, outfile):
    """
    Check that the content of outfile is the same as in expfile

    Parameters
    ----------
    expfile : str
        path to expected file
    outfile : str
        path to output file
    """
    assert os.path.isfile(outfile)
    with open(expfile, "r") as expf, open(outfile, "r") as outf:
        lines_exp = []
        lines_out = []
        for lineexp in expf:
            lines_exp.append(lineexp.strip())
        for lineout in outf:
            lines_out.append(lineout.strip())
    assert len(lines_out) == len(lines_exp)
    assert set(lines_out) == set(lines_exp)


def test_write_missing():
    """
    Test that given families with genomes present, genomes with several numbers and
    list of all genomes, it returns, for each family, the genomes which will not
    be considered.
    """
    aldir = "."
    dname = "TEST6"
    p2p.write_missing_genomes(FAM_GENOMES, SEVERAL, ALL_GENOMES, aldir, dname)

    # Check content of output files
    exp1 = []
    check_missing("{}-current.{}.miss.lst".format(dname, 1), exp1)
    exp2 = ["ESCO1", "ESCO3", "ESCO5", "ESCO6"]
    check_missing("{}-current.{}.miss.lst".format(dname, 2), exp2)
    exp3 = ["ESCO1"]
    check_missing("{}-current.{}.miss.lst".format(dname, 3), exp3)
    exp4 = ["ESCO4"]
    check_missing("{}-current.{}.miss.lst".format(dname, 4), exp4)


def check_missing(outfile, exp):
    """
    Check that in the given output file, there is the given list of genomes.
    Then, remove outfile.

    Parameters
    ----------
    outfile : str
        output file
    exp : list
        list of lines that must be in outfile
    """
    assert os.path.isfile(outfile)
    missing = []
    with open(outfile, "r") as outf:
        for line in outf:
            missing.append(line.strip())
    assert len(missing) == len(exp)
    assert set(missing) == set(exp)
    os.remove(outfile)