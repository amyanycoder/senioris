def main():
    file = open("file.txt", "r")
    print(file.read())
    file.close()

    file = open("read.py", "r")
    print(file.read())
    file.close()


    file = open("cannytest.jpg", "rb")
    print(file.read())
    file.close()


if __name__ == "__main__":
    main()