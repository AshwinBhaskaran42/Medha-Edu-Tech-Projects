from modules.reading_challenge import track_reading_challenge

from datetime import date

def view_member_profile(member_id, library_members, library_branches):
    if member_id not in library_members:
        print(f"Member ID '{member_id}' not found.")
        return

    member = library_members[member_id]
    name = member["name"]
    membership = member["membership_type"].capitalize()
    branch_id = member["branch_id"]

    read_books = member.get("books_read", [])
    issued_books = member.get("books_issued", [])

    # # Books read this year
    # year = date.today().year
    # books_read_this_year = 0
    # for book in read_books:
    #     if "return_date" in book:
    #         if book["return_date"].year == year:
    #             books_read_this_year += 1

    # Favorite genres
    genres = []
    for book in read_books:
        isbn = book["isbn"]
        if isbn in library_branches[branch_id]["books"]:
            genre = library_branches[branch_id]["books"][isbn]["genre"]
            if genre not in genres:
                genres.append(genre)

    # Average reading time
    total_days = 0
    count = 0
    for book in read_books:
        if "issue_date" in book and "return_date" in book:
            days = (book["return_date"] - book["issue_date"]).days
            total_days += days
            count += 1

    if count > 0:
        avg_days = total_days // count
    else:
        avg_days = "N/A"

    # Current status
    if member["membership_type"] == "standard":
        limit = 5
    else:
        limit = 10

    overdue = 0
    fine = 0
    for book in issued_books:
        if "due_date" in book:
            if date.today() > book["due_date"]:
                overdue += 1
                fine += (date.today() - book["due_date"]).days * 10

    # Output
    print("\n=== MEMBER READING PROFILE ===")
    print("Member:", name)
    print("Membership:", membership)
    print("Books Borrowed This Year:", member.get('total_books_borrowed',0))
    print("Favorite Genres:", ", ".join(genres) if genres else "N/A")
    print("Average Reading Time:", avg_days, "days per book")
    print("Current Status:")
    print("- Books Currently Issued:", str(len(issued_books)) + "/" + str(limit))
    print("- Overdue Books:", overdue)
    print("- Pending Fines: ₹" + str(fine))
    track_reading_challenge(member_id, library_members)
