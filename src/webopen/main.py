import webbrowser
import argparse

def main():
    def open_link(website):
        webbrowser.open(f"http://{website}")
        
    parser=argparse.ArgumentParser(description="Open a weblink.")
    parser.add_argument("-link",dest="link_name",help="The name of the link to open")
    args=parser.parse_args()
    open_link(args.link_name)

if __name__ == "__main__":
    main()