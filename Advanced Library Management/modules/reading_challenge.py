def track_reading_challenge(member_id, library_members, challenge_name_suffix="Books Challenge 2025"):
    if member_id not in library_members:
        print(f"Member ID '{member_id}' not found.")
        return

    member = library_members[member_id]
    read_books = member.get("books_read", [])
    goal = member.get("challenge_input")

    if goal == 0:
        print("No reading challenge assigned to this member.")
        return

    total_read = len(read_books)
    percent = int((total_read / goal) * 100) if goal > 0 else 0

    print("\nReading Challenge Progress:")
    print(f'"{goal} Books reading challenge progress": {total_read}/{goal} ({percent}% complete)')

    if total_read >= goal:
        print("Congratulations! You've completed your reading challenge!")
