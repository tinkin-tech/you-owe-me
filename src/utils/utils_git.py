import subprocess


def get_commit_by_date(directory_path, date):
    return (
        subprocess.check_output(
            f"cd '{directory_path}' && git rev-list -1 --before {date} HEAD",
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )


def checkout_by_commit_or_branch(directory_path, identifier):
    subprocess.run(
        f"cd '{directory_path}' && git checkout {identifier} --quiet --force",
        shell=True,
        stdout=subprocess.DEVNULL,
        check=True,
    )


def get_current_branch(directory_path):
    return (
        subprocess.check_output(
            f"cd '{directory_path}' && git rev-parse --abbrev-ref HEAD ",
            shell=True,
        )
        .decode("utf-8")
        .strip()
    )
