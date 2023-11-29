def file_writer(file_name, phrase):
    try:
        f = open(file_name, "w")
        f.write(phrase)
    except:
        print("error writing to file", file_name)
    f.close()