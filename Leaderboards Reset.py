#Opens the file
File = open("Assets/HighScore.txt", "w")

#Writes default values into the file
for line in range(3):
    File.write("0 AAA\n")

#Closes the file
File.close
