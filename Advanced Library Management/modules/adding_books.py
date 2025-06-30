def add_book(isbn, title, author, genre, copies, book_type, branch_id, library_branches):

    books= library_branches[branch_id]["books"]

    books[isbn]={
        "title":title,
        "author":author,
        "genre":genre,
        "copies":copies,
        "book_type":book_type
    }
    
    print(f"Book '{title}' having ISBN:{isbn} successfully added to branch:{branch_id}")    

def add_books(library_branches):
    # if "books" not in library_branches[branch_id]:
    #     library_branches[branch_id]["books"]={}
        
    # books= library_branches[branch_id]["books"]
    
    while True:
        print("\nAdding new book: ")
        branch_id= input("Enter branch id: ")
        if branch_id not in library_branches:
            print("Branch does not exist.")
            continue

        if "books" not in library_branches[branch_id]:
            library_branches[branch_id]["books"]={}
        books= library_branches[branch_id]["books"]

        isbn = input("Enter book ISBN: ").strip()
        if isbn in books:
            print(f"Book with ISBN: {isbn} already exists in branch: {branch_id}.")
            continue
        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()
        genre = input("Enter genre: ").strip()
        copies = input("Enter number of copies: ").strip()
        book_type = input("Enter book type (physical/digital): ").strip().lower()

        if book_type not in ['physical','digital']:
            print("Book type must be either: physical or digital.")
            continue

        add_book(isbn, title, author, genre, int(copies), book_type, branch_id, library_branches)

        cont= input("Add another book? (yes/no): ").strip().lower()
        if cont !='yes':
            break