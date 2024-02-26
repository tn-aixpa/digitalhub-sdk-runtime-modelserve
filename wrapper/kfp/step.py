"""
Wrapper to execute an arbitrary function.
"""
import os
import argparse
from pathlib import Path

from digitalhub_core.utils.logger import LOGGER

import digitalhub as dhcore


def main():
    """
    Main function. Get run from backend and execute function.
    """

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='Step executor')

    parser.add_argument('--project', type=str, help='Project reference')
    parser.add_argument('--function', type=str, help='Function name')
    parser.add_argument('--action', type=str, help='Action type')
    parser.add_argument('--jsonprops', type=str, help='Project reference')
    parser.add_argument('-p', type=str, help='Parameter')
    parser.add_argument('-i', type=str, help='Input property')
    parser.add_argument('-o', type=str, help='Output property')
    args = parser.parse_args()

    LOGGER.info("Loading project " + args.project)
    # project = dhcore.get_project(args.project)
    
    LOGGER.info("Executing function " + args.function +' task ' + args.action)
    # function = project.get_function(args.function)
    # function.run(args.action)

    LOGGER.info("Done.")


if __name__ == "__main__":
    main()
