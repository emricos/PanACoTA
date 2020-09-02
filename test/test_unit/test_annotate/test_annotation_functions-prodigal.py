#!/usr/bin/env python3
# coding: utf-8

"""
Unit tests for annotate/annotation_functions.py
"""

import pytest
import os
import logging
import shutil

import test.test_unit.utilities_for_tests as tutil
import PanACoTA.utils as utils
import PanACoTA.annotate_module.annotation_functions as afunc


# Define variables used by several tests
DBDIR = os.path.join("test", "data", "annotate")
GEN_PATH = os.path.join(DBDIR, "genomes")
TMP_PATH = os.path.join(DBDIR, "tmp_files")
EXP_DIR = os.path.join(DBDIR, 'exp_files')
TEST_DIR = os.path.join(DBDIR, 'test_files')
GENEPATH = os.path.join(DBDIR, "generated_by_unit-tests")
LOGFILE_BASE = os.path.join(GENEPATH, "logfile.log")
LOGFILES = [LOGFILE_BASE + ext for ext in [".log", ".log.debug", ".log.details", ".log.err"]]


@pytest.fixture(autouse=True)
def setup_teardown_module():
    """
    Remove log files at the end of this test module

    Before each test:
    - init logger
    - create directory to put generated files

    After:
    - remove all log files
    - remove directory with generated results
    """
    os.mkdir(GENEPATH)
    print("setup")

    yield
    for f in LOGFILES:
        if os.path.exists(f):
            os.remove(f)
    shutil.rmtree(GENEPATH)
    print("teardown")


# Create a logger with sublogger inside
def my_logger(name):
    """
    logger given to function called by a subprocess
    """
    import multiprocessing
    m = multiprocessing.Manager()
    q = m.Queue()
    qh = logging.handlers.QueueHandler(q)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers = []
    logging.addLevelName(utils.detail_lvl(), "DETAIL")
    root.addHandler(qh)
    return q, logging.getLogger(name)


def test_check_prodigal_nofaa():
    """
    Check that check_prodigal returns false when a faa file is missing, and an error message
    """
    logger = my_logger("test_check_prodigal_nofaa")
    ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prokkaRes")
    ori_name = "prokka_out_for_test"
    out_dir = os.path.join(GENEPATH, "out_test_nofaa")
    name = "prodigal_out_for_test-missfaa"
    os.makedirs(out_dir)
    shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
                    os.path.join(out_dir, name + ".tbl"))
    shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
                    os.path.join(out_dir, name + ".ffn"))
    shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
                    os.path.join(out_dir, name + ".gff"))
    logf = os.path.join(GENEPATH, "prodigal.log")
    gpath = "path/to/nogenome/original_name.fna"
    nbcont = 7
    assert not afunc.check_prodigal(gpath, name, out_dir, logger[1])
    msg = "prodigal_out_for_test-missfaa original_name.fna: no or several .faa file(s)"
    q = logger[0]
    assert q.qsize() == 2
    assert q.get().message == msg
    assert q.get().message == "no faa"


# def test_check_prodigal_sevfaa():
#     """
#     Check that check_prodigal returns false when there is more than 1 faa file,
#     and an error message
#     """
#     logger = my_logger("test_check_prodigal_sevfaa")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "out_test_nofaa")
#     name = "prodigal_out_for_test-missfaa"
#     os.makedirs(out_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + "2.faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = "prodigal_out_for_test-missfaa original_name.fna: several .faa files"
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_noffn():
#     """
#     Check that check_prodigal returns false when a ffn file is missing, and an error message
#     """
#     logger = my_logger("test_check_prodigal_noffn")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "out_test_noffn")
#     name = "prodigal_out_for_test-missffn"
#     os.makedirs(out_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = "prodigal_out_for_test-missffn original_name.fna: no .ffn file"
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_sevffn():
#     """
#     Check that check_prodigal returns false when there is more than 1 ffn file,
#     and an error message
#     """
#     logger = my_logger("test_check_prodigal_sevffn")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "out_test_noffn")
#     name = "prodigal_out_for_test-missffn"
#     os.makedirs(out_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + "2.ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = "prodigal_out_for_test-missffn original_name.fna: several .ffn files"
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_nogff():
#     """
#     Check that check_prodigal returns false when a ffn file is missing, and an error message
#     """
#     logger = my_logger("test_check_prodigal_nogff")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "out_test_noffn")
#     name = "prodigal_out_for_test-missgff"
#     os.makedirs(out_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = "prodigal_out_for_test-missgff original_name.fna: no .gff file"
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_sevgff():
#     """
#     Check that check_prodigal returns false when there is more than 1 ffn file,
#     and an error message
#     """
#     logger = my_logger("test_check_prodigal_sevgff")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "out_test_noffn")
#     name = "prodigal_out_for_test-sevgff"
#     os.makedirs(out_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + "2.gff"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = "prodigal_out_for_test-sevgff original_name.fna: several .gff files"
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_wrong_cont():
#     """
#     Check that check_prodigal returns an error message when the number of contigs in tbl
#     file is not as expected
#     """
#     logger = my_logger("test_check_prodigal_wrong_cont")
#     outdir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     name = "prodigal_out_for_test"
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 10
#     assert not afunc.check_prodigal(outdir, logf, name, gpath, nbcont, logger[1])
#     msg = ("prodigal_out_for_test original_name.fna: no matching number of contigs; "
#            "nbcontig=10; in tbl =7")
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_wrong_tbl_cds():
#     """
#     Check that check_prodigal returns an error message when the number of CDS in tbl
#     file is different from the number of headers in faa file
#     """
#     logger = my_logger("test_check_prodigal_wrong_tbl_cds")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "res_checkprodigalWrongTbl")
#     os.makedirs(out_dir)
#     name = "prodigal_out_for_test-wrongCDS"
#     tblfile = os.path.join(TEST_DIR, name + ".tbl")
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))

#     shutil.copyfile(tblfile, os.path.join(out_dir, name + ".tbl"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg1 = ("prodigal_out_for_test-wrongCDS original_name.fna: "
#             "no matching number of proteins between tbl and faa; "
#             "faa=13; in tbl =12")
#     msg2 = ("prodigal_out_for_test-wrongCDS original_name.fna: "
#             "no matching number of genes between tbl and ffn; "
#             "ffn=17; in tbl =14genes 2CRISPR")
#     q = logger[0]
#     assert q.qsize() == 2
#     assert q.get().message == msg1
#     assert q.get().message == msg2


# def test_check_prodigal_wrong_tbl_crispr():
#     """
#     Check that check_prodigal returns an error message when the number of headers in ffn
#     file is different from the number of CDS + CRISPR in tbl file (1CRISPR in tbl, 2 in ffn)
#     """
#     logger = my_logger("test_check_prodigal_wrong_tbl_crispr")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "res_checkprodigalWrongCRISPR")
#     os.makedirs(out_dir)
#     name = "prodigal_out_for_test-wrongtblCRISP"
#     tblfile = os.path.join(TEST_DIR, name + ".tbl")
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(out_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     shutil.copyfile(tblfile, os.path.join(out_dir, name + ".tbl"))
#     logf = "prodigal.log"
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert not afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])
#     msg = ("prodigal_out_for_test-wrongtblCRISP original_name.fna: "
#            "no matching number of genes between tbl and ffn; "
#            "ffn=17; in tbl =15genes 1CRISPR")
#     q = logger[0]
#     assert q.qsize() == 1
#     assert q.get().message == msg


# def test_check_prodigal_tbl_crispr_newversion():
#     """
#     Check that check_prodigal does not return an error message when the number of headers in ffn
#     file is equal to the number of CDS in tbl file (1CRISPR in tbl, 0 in ffn), but
#     does not contain the CRISPRs found in tbl
#     As the new version of prodigal (1.12) does not put crisprs in .ffn
#     """
#     logger = my_logger("test_check_prodigal_tbl_crispr_newversion")
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     out_dir = os.path.join(GENEPATH, "res_checkprodigalWrongCRISPRnewversion")
#     os.makedirs(out_dir)
#     name = "prodigal_out_for_test-wrongtblCRISPnewversion"
#     ffnfile = os.path.join(TEST_DIR, name + ".ffn")
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".tbl"),
#                     os.path.join(out_dir, name + ".tbl"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(out_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(out_dir, name + ".gff"))
#     shutil.copyfile(ffnfile, os.path.join(out_dir, name + ".ffn"))
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert afunc.check_prodigal(out_dir, logf, name, gpath, nbcont, logger[1])


# def test_check_prodigal_ok():
#     """
#     Check that everything is ok with prodigal results (tbl, faa and ffn files exist,
#     and number of CDS, CRISPR and genes correspond between them)
#     """
#     logger = my_logger("test_check_prodigal_ok")
#     outdir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     name = "prodigal_out_for_test"
#     logf = os.path.join(GENEPATH, "prodigal.log")
#     gpath = "path/to/nogenome/original_name.fna"
#     nbcont = 7
#     assert afunc.check_prodigal(outdir, logf, name, gpath, nbcont, logger[1])


# def test_run_prodigal_out_exists_ok():
#     """
#     Test that when the output directory already exists, and files inside are OK,
#     run_prodigal returns True, with a warning message indicating that prodigal did not rerun.
#     """
#     logger = my_logger("test_run_prodigal_out_exists_ok")
#     utils.init_logger(LOGFILE_BASE, 0, 'prodigal_out_exists_ok')
#     gpath = "path/to/nogenome/original_name.fna"
#     cores_prodigal = 1
#     name = "prodigal_out_for_test"
#     force = False
#     nbcont = 7
#     arguments = (gpath, TEST_DIR, cores_prodigal, name, force, nbcont, None, logger[0])
#     assert afunc.run_prodigal(arguments)

#     q = logger[0]
#     assert q.qsize() == 4
#     # start annotating :
#     assert q.get().message.startswith("Start annotating")
#     # # warning prodigal results folder exists:
#     assert q.get().message.startswith("prodigal results folder test/data/annotate/test_files/"
#                                       "original_name.fna-prodigalRes already exists.")
#     # Results in result folder are ok
#     assert q.get().message.startswith("prodigal did not run again, formatting step used already "
#                                       "generated results of prodigal in "
#                                       "test/data/annotate/test_files/original_name.fna-prodigalRes.")
#     # End annotation:
#     assert q.get().message.startswith("End annotating")


# def test_run_prodigal_out_exists_error():
#     """
#     Test that when the output directory already exists, and 1 file is missing,
#     run_prodigal returns False, and writes the warning message saying that prodigal did not
#     rerun, + the warning message for the missing file(s).
#     """
#     logger = my_logger("test_run_prodigal_out_exists_error")
#     utils.init_logger(LOGFILE_BASE, 0, 'prodigal_out_error')
#     ori_prok_dir = os.path.join(TEST_DIR, "original_name.fna-prodigalRes")
#     ori_name = "prodigal_out_for_test"
#     new_prok_dir = os.path.join(GENEPATH, "original_name-error-prodigalRes")
#     name = "prodigal_out_for_test-wrongCDS"
#     os.makedirs(new_prok_dir)
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".ffn"),
#                     os.path.join(new_prok_dir, name + ".ffn"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".faa"),
#                     os.path.join(new_prok_dir, name + ".faa"))
#     shutil.copyfile(os.path.join(ori_prok_dir, ori_name + ".gff"),
#                     os.path.join(new_prok_dir, name + ".gff"))
#     gpath = "path/to/nogenome/original_name-error"
#     cores_prodigal = 1
#     force = False
#     nbcont = 7
#     arguments = (gpath, GENEPATH, cores_prodigal, name, force, nbcont, None, logger[0])
#     assert not afunc.run_prodigal(arguments)
#     q = logger[0]
#     # assert q.qsize() == 4
#     # start annotating :
#     assert q.get().message.startswith("Start annotating")
#     # warning prodigal results folder exists:
#     assert q.get().message == ("prodigal results folder test/data/annotate/generated_by_unit-tests/"
#                                "original_name-error-prodigalRes already exists.")
#     # error, no tbl file
#     msg = "prodigal_out_for_test-wrongCDS original_name-error: no .tbl file"
#     assert q.get().message == msg
#     # warning, files in outdir are not as expected
#     assert q.get().message.startswith("Problems in the files contained in your already existing "
#                                       "output dir ")


# def test_run_prodigal_out_exists_force():
#     """
#     Test that when the output directory already exists with wrong files, but force is on,
#     prodigal is rerun and outputs the right files
#     """
#     logger = my_logger("test_run_prodigal_out_exists_force")
#     utils.init_logger(LOGFILE_BASE, 0, 'force')
#     gpath = os.path.join(GEN_PATH, "H299_H561.fasta")
#     out_prokdir = os.path.join(GENEPATH, "H299_H561.fasta-prodigalRes")
#     name = "test_runprodigal_H299"
#     # Put empty tbl, faa, ffn files in prodigal output dir, to check that they are overridden
#     os.makedirs(out_prokdir)
#     open(os.path.join(out_prokdir, name + ".tbl"), "w").close()
#     open(os.path.join(out_prokdir, name + ".faa"), "w").close()
#     open(os.path.join(out_prokdir, name + ".ffn"), "w").close()
#     cores_prodigal = 2
#     force = True
#     nbcont = 3
#     arguments = (gpath, GENEPATH, cores_prodigal, name, force, nbcont, None, logger[0])
#     assert afunc.run_prodigal(arguments)
#     # As we used 'force', tbl, faa and ffn files, which were empty, must have been replaced
#     # by the prodigal output
#     exp_dir = os.path.join(EXP_DIR, "H299_H561.fasta-short-contig.fna-prodigalRes",
#                            "test_runprodigal_H299")
#     out_tbl = os.path.join(out_prokdir, name + ".tbl")
#     out_faa = os.path.join(out_prokdir, name + ".faa")
#     out_ffn = os.path.join(out_prokdir, name + ".ffn")
#     assert os.path.isfile(out_tbl)
#     # For tbl file, check that, at least, the 3 contigs were considered,
#     # and that the number of CDS is as expected.
#     # Before, we checked that the output
#     # was exactly as expected. But it changes with the different versions of prodigal, so
#     # we cannot compare the whole file.
#     with open(out_tbl, "r") as outt:
#         lines = [line.strip() for line in outt.readlines()]
#         assert ">Feature H561_S27" in lines
#         assert ">Feature H561_S28" in lines
#         assert ">Feature H561_S29" in lines
#         CDS = 0
#         for line in lines:
#             if "CDS" in line:
#                 CDS += 1
#         assert CDS == 16
#     # Check that faa and ffn files are as expected
#     assert os.path.isfile(out_faa)
#     tutil.compare_order_content(exp_dir + ".faa", out_faa)
#     assert os.path.isfile(out_ffn)
#     tutil.compare_order_content(exp_dir + ".ffn", out_ffn)
#     q = logger[0]
#     # assert q.qsize() == 3
#     assert q.get() .message.startswith("Start annotating test_runprodigal_H299 from test/data/"
#                                        "annotate/genomes/H299_H561.fasta with prodigal")
#     assert q.get() .message == ("prodigal results folder already exists, but removed because "
#                                 "--force option used")
#     assert q.get().message == ("prodigal command: prodigal "
#                                "--outdir test/data/annotate/generated_by_unit-tests/"
#                                "H299_H561.fasta-prodigalRes --cpus 2 --prefix test_runprodigal_H299 "
#                                "test/data/annotate/genomes/H299_H561.fasta")
#     assert q.get() .message.startswith("End annotating test_runprodigal_H299 "
#                                        "from test/data/annotate/genomes/H299_H561.fasta")


# def test_run_prodigal_out_doesnt_exist():
#     """
#     Test that when the output directory does not exist, it creates it, and runs prodigal
#     with all expected outfiles
#     """
#     logger = my_logger("test_run_prodigal_out_doesnt_exist")
#     utils.init_logger(LOGFILE_BASE, 0, 'test_run_prodigal_out_doesnt_exist')
#     gpath = os.path.join(GEN_PATH, "H299_H561.fasta")
#     out_dir = os.path.join(GENEPATH, "H299_H561.fasta-prodigalRes")
#     cores_prodigal = 2
#     name = "test_runprodigal_H299"
#     force = False
#     nbcont = 3
#     arguments = (gpath, GENEPATH, cores_prodigal, name, force, nbcont, None, logger[0])
#     assert afunc.run_prodigal(arguments)
#     # Check content of tbl, ffn and faa files
#     exp_dir = os.path.join(EXP_DIR, "H299_H561.fasta-short-contig.fna-prodigalRes",
#                            "test_runprodigal_H299")
#     out_tbl = os.path.join(out_dir, name + ".tbl")
#     out_faa = os.path.join(out_dir, name + ".faa")
#     out_ffn = os.path.join(out_dir, name + ".ffn")
#     out_gff = os.path.join(out_dir, name + ".gff")
#     assert os.path.isfile(out_tbl)
#     # For tbl file, check that, at least, the 3 contigs were considered,
#     # and that the number of CDS is as expected.
#     # Before, we checked that the output
#     # was exactly as expected. But it changes with the different versions of prodigal, so
#     # we cannot compare the whole file.
#     with open(out_tbl, "r") as outt:
#         lines = [line.strip() for line in outt.readlines()]
#         assert ">Feature H561_S27" in lines
#         assert ">Feature H561_S28" in lines
#         assert ">Feature H561_S29" in lines
#         CDS = 0
#         for line in lines:
#             if "CDS" in line:
#                 CDS += 1
#         assert CDS == 16
#     assert os.path.isfile(out_faa)
#     with open(exp_dir + ".faa", "r") as expf, open(out_faa, "r") as outf:
#         for line_exp, line_out in zip(expf, outf):
#             assert line_exp == line_out
#     # Check that faa and ffn files are as expected
#     assert os.path.isfile(out_faa)
#     tutil.compare_order_content(exp_dir + ".faa", out_faa)
#     assert os.path.isfile(out_ffn)
#     tutil.compare_order_content(exp_dir + ".ffn", out_ffn)
#     q = logger[0]
#     assert q.qsize() == 3
#     assert q.get().message.startswith("Start annotating")
#     assert q.get().message == ("prodigal command: prodigal "
#                                "--outdir test/data/annotate/generated_by_unit-tests/"
#                                "H299_H561.fasta-prodigalRes --cpus 2 --prefix test_runprodigal_H299 "
#                                "test/data/annotate/genomes/H299_H561.fasta")
#     assert q.get().message.startswith("End annotating")


# def test_run_prodigal_out_problem_running():
#     """
#     Check that when a problem occurs while trying to run prodigal, run_prodigal returns False,
#     and the error message indicating to read in the log why it couldn't run
#     """
#     logger = my_logger("test_run_prodigal_out_problem_running")
#     utils.init_logger(LOGFILE_BASE, 0, 'test_run_prodigal_out_problem_running')
#     gpath = os.path.join(GEN_PATH, "H299 H561.fasta")
#     cores_prodigal = 2
#     name = "test_runprodigal_H299-error"
#     force = False
#     nbcont = 3
#     logf = os.path.join(GENEPATH, "H299 H561.fasta-prodigal.log")
#     arguments = (gpath, GENEPATH, cores_prodigal, name, force, nbcont, None, logger[0])
#     assert not afunc.run_prodigal(arguments)
#     q = logger[0]
#     assert q.qsize() == 3
#     assert q.get().message.startswith("Start annotating")
#     assert q.get().message == ("prodigal command: prodigal "
#                                "--outdir test/data/annotate/generated_by_unit-tests/"
#                                "H299 H561.fasta-prodigalRes --cpus 2 "
#                                "--prefix test_runprodigal_H299-error "
#                                "test/data/annotate/genomes/H299 H561.fasta")
#     assert q.get().message == ("Error while trying to run prodigal on test_runprodigal_H299-error "
#                                "from test/data/annotate/genomes/H299 H561.fasta")