#Author: Modester Mwangi and Bello Moussa

""" This programme records everything the user does in the
system by taking the users inputs and reads the file"""

def write_to_file(user_inputs):
    file = open("user's_info.txt", "a")

    #writing the file
    file.write(user_inputs + "\n")

def main():
    user_in_puts = input("Fill in your personal details: player name, full name, email, age city? ")
    len(user_in_puts)

    write_to_file(user_in_puts)

    user_info = input("give a brief of the motive if you playing this game")

    write_to_file(user_info)


if __name__ == "__main__":
    main()
