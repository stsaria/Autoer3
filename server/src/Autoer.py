import server, sys
version = 0.1
edition = "alpha"

def main(args : list):
    if args == 1:
        print("Autoer3-Server\nVersion : "+version+"-"+edition)
    else:
        if args[1] in "start":
            if len(args) >= 3:
                server.main(int(args[2]))
            else:
                server.main()

if __name__ == "__main__":
    main(sys.argv)