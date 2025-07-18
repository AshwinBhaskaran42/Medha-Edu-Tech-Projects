# This file contains the following functions:
# add_to_waitlist
# calculate_fine
# return_book
# issue_book
# issue_books
# return_books
# add_copies

from datetime import date, timedelta

##########################################################################################################

def add_to_waitlist(member_id, isbn, waitlist):
    if isbn not in waitlist:
        waitlist[isbn]= []
    if member_id in waitlist[isbn]:
        print(f"Member '{member_id}' is already in waitlist for book with ISBN:{isbn} ")
    else:
        waitlist[isbn].append(member_id)
        print(f"Member '{member_id}' added to the waitlist for book ISBN:{isbn}.")
    ###### JUST PRITING TO SEE THE CONTENTS
    print(waitlist)

###########################################################################################################

def calculate_fine(issue_record, lost_damaged):
    due_date=issue_record["due_date"]
    today= date.today()

    fine=0
    if lost_damaged=='yes':
        fine=500

    if today < due_date:
        return fine
    elif today > due_date:
        late_days= (today - due_date).days
        fine = fine + late_days * 10
        return fine
    else:
        return 0

###########################################################################################################

def return_book(member_id, isbn, library_members, library_branches, waitlist, lost_damaged):
        member= library_members[member_id]
        branch_id= member['branch_id']
        fine=0
        today= date.today()
        books_issued = member.get('books_issued', [])
        
        
        for book in books_issued:
            if book['isbn']==isbn and book['branch_id']==branch_id:
                issue_date= book["issue_date"]
                due_date= book['due_date']
                fine= calculate_fine(book, lost_damaged)
                books_issued.remove(book)
                break
        
        # for book in books_issued:
        #     if isbn == book['isbn']:
        #         due_date= book.get('due_date')
        #         break

        # library_branches[branch_id]["books"]['isbn']["copies"] +=1
        if lost_damaged != 'yes':
            library_branches[branch_id]["books"][isbn]["copies"] +=1

        # print(f"Book with ISBN:{isbn} successfully returned by member with ID:{member_id}.")

        if lost_damaged == 'yes' and today < due_date:
            print(f"Book is lost/damaged. But due date has not been crossed.")
            print(f"Fine: ₹{fine}")

        elif lost_damaged == 'yes' and today > due_date:
            print(f"Book is lost/damaged and due date has been crossed.")
            print(f"Fine: ₹{fine}. {fine//10} days late.")

        elif lost_damaged !='yes' and fine > 0:
            print(f"Fine: ₹{fine}. Returned {fine//10} days late.")
        else:
            print("Book returned on time. No Fine imposed.")

        if isbn in waitlist and waitlist[isbn] and library_branches[branch_id]["books"][isbn]["copies"]>0:
            next_member_id = waitlist[isbn].pop(0)
            print(f"Book with ISBN:{isbn} will now be issued to waitlisted member with ID:{next_member_id}.")
            issue_book(next_member_id, isbn, library_members, library_branches)

        if 'books_read' not in library_members[member_id]:
            library_members[member_id]['books_read']=[]
        
        already_recorded = False
        for i in library_members[member_id]['books_read']:
            if i['isbn'] == isbn and i['branch_id']== branch_id:
                already_recorded= True
                break
        
        if not already_recorded:
            library_members[member_id]['books_read'].append({
                "isbn":isbn,
                "branch_id":branch_id,
                "issue_date":issue_date,
                "return_date":date.today()
            })


    
###########################################################################################################

def issue_book(member_id, isbn, library_members, library_branches):
    branch_id= library_members[member_id]['branch_id']
    book= library_branches[branch_id]["books"][isbn]
    book["copies"] -=1

    if "books_issued" not in library_members[member_id]:
        library_members[member_id]["books_issued"]= []

    if "books_issued" in library_members[member_id]:
        today = date.today()

        if library_members[member_id]["membership_type"] == "standard":
            due_duration= 15
        else:
            due_duration= 30

        due_date= today + timedelta(days= due_duration)
 
        library_members[member_id]["books_issued"].append({
            "isbn":isbn,
            "branch_id":branch_id,
            "issue_date": today,
            "due_date": due_date
        })
        print(f"Book {book['title']}, ISBN:{isbn} issued to member:{member_id} from branch:{branch_id}.")
        print(f"Issued on: {today}. Due by: {due_date}")
        library_members[member_id]["total_books_borrowed"] += 1
###########################################################################################################

def issue_books(library_members, library_branches, waitlist):
    while True:
        print("Issuing a book to member.")
        member_id= input("Enter member id: ")
        if member_id not in library_members:
            print(f"Member ID: {member_id} does not exist.")
            continue
        member= library_members[member_id]

        if date.today() > member['membership_expiry']:
            print(f"Membership of Member:{member_id} has expired on {member['membership_expiry']}.")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue

        has_overdue = False
        for issued_book in member.get('books_issued',[]):
            if date.today() > issued_book['due_date']:
                has_overdue= True
                break
        if has_overdue:
            print(f"Member:{member_id} has overdue books. Return them before borrowing more.")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue

        branch_id=member["branch_id"]

        branch_books= library_branches[branch_id].get('books', {})
        
        limit = 5 if member['membership_type']=='standard' else 10
        #if "books_issued" in library_members[member_id]:
        books_issued_len = len(member.get('books_issued',[]))

        isbn= input("Enter the ISBN number: ")
        if isbn in branch_books:
            book= branch_books[isbn]

        elif isbn not in branch_books:
            print(f"The book with ISBN:{isbn} is not available in this library.")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue

        #To prevent the member from being issued the book while already having a copy of it:
        already_issued = False
        if "books_issued" in library_members[member_id]:
            for i in library_members[member_id]["books_issued"]:
                if i["isbn"] == isbn:
                    already_issued = True
                    break
        if already_issued:
            print(f"Member {member_id} already has a copy of the book with ISBN:{isbn}!")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue

        elif books_issued_len >= limit:
            print(f"Member has reached their issue limit: {limit}.")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue
        
        elif isbn in waitlist and member_id in waitlist[isbn]:
            print(f"Member '{member_id}' is already in waitlist for book with ISBN:{isbn} ")
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue

        elif book["copies"]<=0:
            print(f"No copies of the book '{book['title']}' are currently availabe.\nMember will be added to the waitlist if their issue-limit is not exceeded.")
            add_to_waitlist(member_id, isbn, waitlist)
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue
        
        # if all good, then issue book:
        else:
            issue_book(member_id, isbn, library_members, library_branches)
            cont=input("\nIssue another book? (yes/no): ").strip().lower()
            if cont !='yes':
                break
            else:
                continue
###########################################################################################################

def return_books(library_members, library_branches, waitlist):
    while True:
        print("Returning a book.")
        member_id= input("Enter member ID: ").strip()
        if member_id not in library_members:
            print(f"Member '{member_id}' does not exist.")
            continue
        isbn = input("Enter Book's ISBN: ").strip()
        lost_damaged= input(f"Is the book damaged or lost (yes/no): ").strip()
        ####

        member = library_members[member_id]
        branch_id= member['branch_id']
        books_issued = member.get('books_issued', [])

        found = False
        for book in books_issued:
            if book['isbn'] == isbn and book['branch_id']==branch_id:
                return_book(member_id, isbn, library_members, library_branches, waitlist, lost_damaged)
                found= True
                break
        if not found:
            print(f"Member {member_id} has not borrowed book with ISBN:{isbn} from branch:{branch_id}.")

        cont = input("Return another book? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
        else:
            continue

###########################################################################################################

def add_copies(library_branches,library_members,waitlist):
    while True:
        branch_id = input("Enter branch id: ")
        if branch_id not in library_branches:
            print("Branch does not exist.")
            cont = input("Add copies to a book? (yes/no): ").strip().lower()
            if cont != 'yes':
                break
            else:
                continue
    
        isbn= input("Enter isbn number: ")
        if isbn not in library_branches[branch_id]['books']:
            print(f"Book with {isbn} does not exist in this branch.")
            cont = input("Add copies to a book? (yes/no): ").strip().lower()
            if cont != 'yes':
                break
            else:
                continue
        
        copies_to_add = int(input("Enter no. of copies to add: "))
        library_branches[branch_id]["books"][isbn]["copies"] += copies_to_add
        print(f"Successfully added {copies_to_add} copies to book with ISBN:{isbn} in branch:{branch_id}.")

        if isbn in waitlist and waitlist[isbn] and library_branches[branch_id]["books"][isbn]["copies"]>0:
            next_member_id = waitlist[isbn].pop(0)
            print(f"As copy/copies of book with ISBN:{isbn} has now become available, a copy will now be issued to waitlisted member with ID:{next_member_id}.")
            issue_book(next_member_id, isbn, library_members, library_branches)
            cont = input("Add copies to a book? (yes/no): ").strip().lower()
            if cont != 'yes':
                break
            else:
                continue


    

