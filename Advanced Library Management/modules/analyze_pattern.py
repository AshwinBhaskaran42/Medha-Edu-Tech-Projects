from datetime import date

def analyze_reading_patterns(member_id, library_members, library_branches):
    if member_id not in library_members:
        print(f"Member ID '{member_id}' not found.")
        return

    member = library_members[member_id]
    branch_id = member["branch_id"]
    read_books = member.get("books_read", [])
    issued_books = member.get("books_issued", [])

    if not read_books and not issued_books:
        print(f"No reading data available for member '{member_id}'.")
        return

    # Total number of books read or currently issued
    total_books_read = len(read_books) + len(issued_books)

    # Count how many times each genre appears
    genre_count = {}
    for book_list in [read_books, issued_books]:
        for book in book_list:
            isbn = book["isbn"]
            if isbn in library_branches[branch_id]["books"]:
                genre = library_branches[branch_id]["books"][isbn]["genre"]
                genre_count[genre] = genre_count.get(genre, 0) + 1

    # Find favorite (most-read) genre
    if genre_count:
        favorite_genre = max(genre_count, key=genre_count.get)
    else:
        favorite_genre = "N/A"

    # Calculate average reading duration from read_books
    total_days = 0
    valid_counts = 0
    for book in read_books:
        if "issue_date" in book and "return_date" in book:
            days = (book["return_date"] - book["issue_date"]).days
            total_days += days
            valid_counts += 1

    avg_reading_days = total_days // valid_counts if valid_counts else "N/A"

    # Find most recent book issued using a simple loop
    latest = None
    latest_date = date(1900, 1, 1)  # A very old default date

    for book in issued_books:
        if "issue_date" in book and book["issue_date"] > latest_date:
            latest = book
            latest_date = book["issue_date"]

    if latest:
        latest_isbn = latest["isbn"]
        latest_title = library_branches[branch_id]["books"].get(latest_isbn, {}).get("title", "Unknown")
    else:
        # Try fallback to latest returned book
        last_returned = None
        last_date = date(1900, 1, 1)
        for book in read_books:
            if "return_date" in book and book["return_date"] > last_date:
                last_returned = book
                last_date = book["return_date"]
        if last_returned:
            latest_isbn = last_returned["isbn"]
            latest_title = library_branches[branch_id]["books"].get(latest_isbn, {}).get("title", "Unknown")
        else:
            latest_title = "None"


    # Display the final summary
    print(f"Reading Summary for Member '{member_id}':")
    print(f"- Total books read: {total_books_read}")
    print(f"- Favorite genre: {favorite_genre}")
    print(f"- Average reading duration: {avg_reading_days} days")
    print(f"- Most recent book issued: {latest_title}")
