import revenue_tracker.interface as interface


def main():

    print("\n", "-"*40, 'REVENUE TRACKER', "-"*40, "\n")

    choice = None
     
    while choice != -1:
        choice = interface.menu()

if __name__ == "__main__":
    main()
