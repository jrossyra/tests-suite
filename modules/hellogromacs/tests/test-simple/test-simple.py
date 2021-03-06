#!/usr/bin/env python

import sys
import os
import shutil
from ttools import JobBuilder, SessionMover

# First working directory
if "__file__" in globals():
    fwd = os.path.abspath(os.path.dirname(__file__))
else:
    fwd = os.getcwd()

session_mover = SessionMover(fwd)
config_file = "gmxsimple.yml"
input_file  = os.path.realpath("../small.tpr")

# Task here is like "MD task" of whatever
# is assigned to a single MD instance.
# On Summit, this maps to "resource set"
jobconfig = dict(
  allocation = 'bif112',
  minutes = 5,
  n_mpi_tasks = 1,
  n_nodes = 1,
  n_tasks = 1,
  threads_per_task = 7,
  mpi_per_task = 1,
  gpu_per_task = 1,
)


if __name__ == "__main__":
  #  # Moves us to a new, unique subdirectory
  # TODO needs to capture env and do file linking
  #  session_mover.use_current()  

    jb = JobBuilder()
    jb.load(config_file)
    jb.configure_workload(jobconfig)

    next_session_directory = session_mover.current
    os.mkdir(next_session_directory)
    shutil.copy(input_file, next_session_directory)
    os.chdir(next_session_directory)

    jb.launch_job()

    os.chdir(fwd)
  #  # Move logs that were left in first working
  #  # directory to the session's subdirectory
  #  session_mover.go_back(capture=True)
