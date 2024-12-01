def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def main():
    content = read_file()

if __name__ == "__main__":
    result = main()
    print(result)
