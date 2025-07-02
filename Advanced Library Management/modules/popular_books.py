from datetime import date, timedelta

def generate_popular_books_report(time_period_days, genre, library_members, library_branches):
    today = date.today()
    start_date = today - timedelta(days=time_period_days)

    # Count how many times each book (by ISBN) was read
    book_read_counts = {}

    for member in library_members.values():
        read_books = member.get("books_read", [])
        for book in read_books:
            isbn = book["isbn"]
            branch_id = book["branch_id"]

            if isbn not in library_branches[branch_id]["books"]:
                continue

            book_info = library_branches[branch_id]["books"][isbn]

            # Check if genre matches
            if book_info["genre"].lower() != genre.lower():
                continue

            # Check if return date is within time period
            return_date = book.get("return_date")
            if return_date and return_date >= start_date:
                book_read_counts[isbn] = book_read_counts.get(isbn, 0) + 1

    # If no books found
    if not book_read_counts:
        print(f"\nNo books found in genre '{genre}' for the last {time_period_days} days.")
        return

    # One-loop sort into a new list, descending by count
    sorted_books = []
    for item in book_read_counts.items():  # item = (isbn, count)
        inserted = False
        for i in range(len(sorted_books)):
            if item[1] > sorted_books[i][1]:
                sorted_books.insert(i, item)
                inserted = True
                break
        if not inserted:
            sorted_books.append(item)

    # Display the report
    print(f"\nPopular Books in Genre '{genre}' (last {time_period_days} days):\n")

    for isbn, count in sorted_books:
        # Find title from any branch (assume ISBN is unique across branches)
        title = "Unknown Title"
        for branch in library_branches.values():
            if isbn in branch["books"]:
                title = branch["books"][isbn]["title"]
                break

        print(f"- {title} (ISBN: {isbn}) — Read {count} time(s)")
