import math
import os
import subprocess
import sys


def ensure_dir_exists(dir_full_path: str):
    if not os.path.exists(dir_full_path):
        os.mkdir(dir_full_path)


def generate_output_dir(page_start: int, page_end: int) -> str:
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    results_dir = os.path.join(script_dir, "results")
    ensure_dir_exists(results_dir)
    page_dir = f"{page_start}_{page_end}"
    output_dir = os.path.join(results_dir, page_dir)
    ensure_dir_exists(output_dir)
    return output_dir


def run_command(*args) -> bool:
    result = subprocess.run(args,
                            stdout=sys.stdout,
                            stderr=sys.stderr,
                            text=True,
                            check=False,
                            shell=True)
    if result.returncode == 0:
        print("Command executed successfully!")
        return True
    return False


def run():
    total = 4387
    batch_size = 5
    total_batches = math.ceil(total / batch_size)
    # Iterate page by page, output page_start and page_end for every page.
    # For example: First page: page_start = 0, page_end = 99
    batch_count = 0
    for page_index in range(total_batches):
        batch_count += 1
        page_start = page_index * batch_size
        page_end = (page_index + 1) * batch_size - 1
        if page_end > total:
            page_end = total - 1  # Index should be < than total

        output_dir = generate_output_dir(page_start, page_end)

        command = "marker_single"
        command_args = [
            f"--output_dir={output_dir}",
            f"--page_range={page_start}-{page_end}",
            "--output_format=markdown",
            "us_hts_2025.pdf"]

        print(f"Processing pages: {page_start}-{page_end} (BatchSize: {batch_size} [{batch_count}/{total_batches}])")
        succeed = run_command(command, *command_args)
        if not succeed:
            break


if __name__ == "__main__":
    run()
