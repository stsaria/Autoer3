import  sys
import SocketClient
version = 0.1
edition = "alpha"

def main():
    print("Autoer3-Client\nVersion : "+str(version)+"-"+edition)
    SocketClient.main()

if __name__ == "__main__":
    main()