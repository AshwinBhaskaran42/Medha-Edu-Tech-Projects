import sys
sys.path.append('./modules')

from datetime import date, timedelta
from imports import *

library_branches = {}
library_members = {}
waitlist={}

lb=False # for add library branches
ab=False # for add books
ac=False # for add copies
rm=False # for register members
ib=False # for issue book


# === Main Menu ===
def library_main():
    global lb
    global ab
    global ac
    global rm
    global ib

    while True:
        print("\n====== LIBRARY MANAGEMENT MENU ======")
        print("1.  Add Library Branch")
        print("2.  Add Books to Branch")
        print("3.  Add copies to an existing book")
        print("4.  Register Member")
        print("5.  Issue Book to Member")
        print("6.  Return Book from Member")
        print("7.  View Member Reading Profile")
        print("8.  Track Reading Challenge")
        print("9.  Analyze Reading Patterns")
        print("10. Popular Books Report")
        print("11. Exit")
        choice = input("Enter your choice (1–10): ").strip()

        if choice == "1":
            add_library_branches(library_branches)
            lb=True
            # print(library_branches)

        elif choice == "2":
            if lb==True:
                add_books(library_branches)
                ab = True
            else:
                print("Please start with option 1.")
                continue
        
        elif choice == "3":
            if ab==True:
                add_copies(library_branches,library_members,waitlist)
                ac = True
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "4":
            if lb==True:
                register_members(library_members,library_branches)
                rm = True
            else:
                print("Please proceed with the prior option in given order, which are required for this option to work.")
                continue

        elif choice == "5":
            if ab==True and rm==True:
                issue_books(library_members, library_branches, waitlist)
                ib = True
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "6":
            if ib==True:
                return_books(library_members, library_branches, waitlist)
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "7":
            if rm==True:
                member_id = input("Enter Member ID: ").strip()
                view_member_profile(member_id, library_members, library_branches)
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "8":
            if rm==True:
                member_id = input("Enter Member ID: ").strip()
                track_reading_challenge(member_id, library_members)
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "9":
            if rm==True:
                member_id = input("Enter Member ID: ").strip()
                analyze_reading_patterns(member_id, library_members, library_branches)
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "10":
            if ab==True and rm==True:
                genre = input("Enter Genre (e.g., Fiction): ").strip()
                days = int(input("Enter number of past days (e.g., 30): ").strip())
                generate_popular_books_report(days, genre, library_members, library_branches)
            else:
                print("Please proceed with the prior options in given order, which are required for this option to work.")
                continue

        elif choice == "11":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    library_main()