
import os
import shutil

# 1. File categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Programming": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".rb", ".php"],
}


# 2. Get file category
def get_category(file_extension):
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category

    return "Others"


# 3. Get unique file path
def get_unique_path(folder_path, filename):
    name, extension = os.path.splitext(filename)

    destination = os.path.join(folder_path, filename)
    counter = 1

    while os.path.exists(destination):
        new_filename = f"{name}_{counter}{extension}"
        destination = os.path.join(folder_path, new_filename)
        counter += 1

    return destination


# 4. Organize files
def organize_file(directory, preview=False):

    if not os.path.exists(directory):
        print("Error: This directory does not exist.")
        return

    if not os.path.isdir(directory):
        print("Error: The given path is not a directory.")
        return

    print(f"\nOrganizing files in: {directory}")

    stats = {
        "moved": 0,
        "failed": 0,
        "skipped": 0,
        "categories": {}
    }

    try:
        filenames = os.listdir(directory)

    except PermissionError:
        print("Error: You cannot access this directory.")
        return

    except OSError as error:
        print(f"Error while reading directory: {error}")
        return

    for filename in filenames:

        source_path = os.path.join(directory, filename)

        if not os.path.isfile(source_path):
            stats["skipped"] += 1
            continue

        file_extension = os.path.splitext(filename)[1].lower()

        category = get_category(file_extension)

        destination_folder = os.path.join(directory, category)

        destination_path = get_unique_path(
            destination_folder, filename
        )

        print(f"{filename} ---> {category}")

        if preview:
            stats["categories"][category] = (
                stats["categories"].get(category, 0) + 1
            )
            continue

        try:
            os.makedirs(destination_folder, exist_ok=True)

            shutil.move(source_path, destination_path)

            stats["moved"] += 1

            stats["categories"][category] = (
                stats["categories"].get(category, 0) + 1
            )

        except PermissionError:
            print(f"Error: No permission to move {filename}")
            stats["failed"] += 1

        except OSError as error:
            print(f"Error moving {filename}: {error}")
            stats["failed"] += 1

    # 5. Display final statistics
    print("\n========== Organizer Summary ==========")

    if preview:
        print("Preview mode: No files were moved.")
        print(f"Files that would be organized: {sum(stats['categories'].values())}")
    else:
        print(f"Successfully moved: {stats['moved']}")
        print(f"Failed: {stats['failed']}")

    print(f"Skipped: {stats['skipped']}")

    print("\nCategory Statistics:")

    for category, count in stats["categories"].items():
        print(f"{category}: {count}")


# 6. Main function
def main():

    print("Welcome to Automated File Organizer!")

    directory = input("Enter your folder path: ").strip().strip('"')

    choice = input(
        "Do you want Preview mode? (Yes/No): "
    ).strip().lower()

    if choice == "yes":
        organize_file(directory, preview=True)

    elif choice == "no":
        organize_file(directory, preview=False)

    else:
        print("Invalid choice! Please enter Yes or No.")


if __name__ == "__main__":
    main()
