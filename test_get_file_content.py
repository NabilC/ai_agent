import os
from functions.get_file_content import get_file_content
from config import MAX_CHARS

def main():
    print(os.path.getsize("calculator/lorem.txt"))  # Should be > 10000
    print("Results for lorem ipsum text")
    result = get_file_content("calculator", "lorem.txt")
    # check for truncation message
    trunc_msg = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    if result.endswith(trunc_msg):
        print("Truncation message found - file was larger than limit.")
    else:
        print("No truncation (file fits within limit).")

    print("\n--- main.py ---")
    print(get_file_content("calculator", "main.py"))

    print("\n--- pkg/calculator.py ---")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n--- /bin/cat ---")
    print(get_file_content("calculator", "/bin/cat")) # (this should return an error string)

    print("\n--- pkg/does_not_exist.py ---")
    print(get_file_content("calculator", "pkg/does_not_exist.py")) # (this should return an error string)


if __name__ == "__main__":
    main()
