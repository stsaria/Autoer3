import configparser, sys
autoer_info = configparser.ConfigParser()
autoer_info.read('./data/autoerInfo.ini')

def main(args : list):
    print("Autoer3\nVersion : "+autoer_info['Autoer']['version']+"-"+autoer_info['Autoer']['edition'])

if __name__ == "__main__":
    main(sys.argv)