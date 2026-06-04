import os

def dump_all_files(output_file="all_code_and_text.txt"):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(output_file, "w", encoding="utf-8", errors="ignore") as out:
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                # Skip the output file itself
                if file == output_file:
                    continue

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    relative_path = os.path.relpath(file_path, current_dir)

                    out.write("=" * 80 + "\n")
                    out.write(f"FILE NAME: {relative_path}\n")
                    out.write("=" * 80 + "\n")
                    out.write(content)
                    out.write("\n\n")

                except Exception as e:
                    print(f"Skipped {file_path}: {e}")

    print(f"Saved all file contents to: {output_file}")


if __name__ == "__main__":
    dump_all_files()