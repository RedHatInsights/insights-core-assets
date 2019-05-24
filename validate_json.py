import git, json, re
import argparse


def validate_specs(specs, sec, filenm):
    """Validates commands, files and glob sections making sure a spec is not it the incorrect section"""
    sections = {'commands': {'bad_spec_name': ['file', 'glob']},
                'files': {'bad_spec_name': ['command', 'glob']},
                'globs': {'bad_spec_name': ['command', 'file']}}

    error = False

    if sec not in sections.keys():
        return

    s = sections[sec]
    for sp in specs:
        if sec[:-1] not in sp.keys():
            bsn = False
            for b in s['bad_spec_name']:
                if b in sp.keys():
                    error = True
                    bsn = True
                    print("ERROR: A {0} spec ({1}) was found in the '{1}' section of ({2}), validation failed"
                          .format(b, sp['symbolic_name'], filenm))
                elif not bsn:
                    print("ERROR: Missing {0} tag in the 'commands' section of ({2}), validation failed"
                          .format(sec[:-1], sec, sp['symbolic_name'], filenm))
        if 'pattern' not in sp.keys():
            error = True
            print("ERROR: Missing 'pattern' tag in the 'commands' section of ({}), validation failed"
                  .format(sp['symbolic_name'], filenm))
        elif not isinstance(sp['pattern'], list):
            error = True
            print("ERROR: The 'pattern' tag in the 'commands' section of ({}) is not type 'list', validation failed"
                  .format(sp['symbolic_name'], filenm))
        if 'symbolic_name' not in sp.keys():
            error = True
            print("ERROR: Missing 'symbolic_name' tag in the 'commands' section of ({}), validation failed"
                  .format(sp['symbolic_name'], filenm))
    return error


def validate_reserved(sec, file):
    """Validates that nothing has changed in sections other than commands, files or globs"""

    other_sections = ['meta_specs', 'pre_commands', 'version', 'specs']
    error = False

    if sec in other_sections:
        error = True
        print("ERROR: Changes found in ({0}) reserved section of {1} file, validation failed"
              .format(sec, file))

    return error


def validate_regex(specs, sec):
    """Validates regex strings in file specs are valid"""

    error = False

    if sec == 'files':
        for spec in specs:
            try:
                re.compile(spec['file'])
            except re.error:
                error = True
                print("ERROR: Invalid regex ({0}) found in ({1}) section, symbolic_name ({2}), validation failed"
                      .format(spec['file'], sec, spec['symbolic_name']))

    return error

def get_args():
    """ Gets runtime argumants"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--branch", help="Branch to validate if running locally")

    return parser.parse_args()


def main(args):
    """Gets branch information, does diffs and calls validation functions."""

    files = ['uploader.json', 'uploader.v2.json']

    start_val = "Validating contents of '{}' files".format("','".join(f for f in files))
    print("\n{}".format(start_val))
    print("-" * len(start_val))

    repo = git.Repo('.')

    if args.branch:
        master_branch = repo.commit("master")
        repo.git.checkout(args.branch)
    else:
        branch = repo.heads[0].name
        repo.git.checkout('origin/master', b="test")
        repo.git.checkout(branch)
        master_branch = repo.commit("test")
        repo.git.checkout(branch)

    sp_stat = False
    res_stat = False
    regex_stat = False
    for file in files:
        diff_index = master_branch.diff(None, file)
        for diff in diff_index.iter_change_type(change_type='M'):
            if diff.a_blob and diff.b_blob:
                master = json.loads(diff.a_blob.data_stream.read().decode('utf-8'))
                branch = json.loads(diff.b_blob.data_stream.read().decode('utf-8'))

                for sec in master.keys():
                    if master[sec] == branch[sec]:
                        branch.pop(sec, None)
                    else:
                        sp_stat = validate_specs(branch[sec], sec, file)
                        res_stat = validate_reserved(sec, file)
                        regex_stat = validate_regex(branch[sec], sec)
    if sp_stat or res_stat or regex_stat:
        print("\nUploader json validation has failed due to previously stated errors "
              "please see the following git diff.\n")
        for file in files:
            df = repo.git.diff(master_branch, '--', file)
            print(df)

    fin_val = "Validation for contents of '{}' files complete".format("','".join(f for f in files))
    print("\n\n{}".format(fin_val))
    print("-" * len(fin_val))

    if sp_stat or res_stat or regex_stat:
        exit(1)


if __name__ == "__main__":
    args = get_args()
    main(args)
