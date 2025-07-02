def generate_recommendations(member_id,library_members, library_branches, recommendation_count=3):
    if member_id not in library_members:
        print(f"Member {member_id} not found.")
        return
    member = library_members[member_id]
    branch_id= member['branch_id']

    issued_books= member.get('books_issued', [])
    read_books= member.get('books_read', [])
    all_books= issued_books + read_books

    read_isbns= []
    read_genres= []

    for book in all_books:
        isbn= book["isbn"]
        if isbn not in read_isbns:
            read_isbns.append(isbn)
        if isbn in library_branches[branch_id]["books"]:
            genre= library_branches[branch_id]["books"][isbn]["genre"]
            if genre not in read_genres:
                read_genres.append(genre)
    
    recommendations= []
    for isbn, book in library_branches[branch_id]['books'].items():
        if book['genre'] in read_genres and isbn not in read_isbns and book['copies']>0:
            recommendations.append({
                'isbn':isbn,
                'title':book['title'],
                'genre':book['genre'],
                'copies':book['copies']
            })
        if len(recommendations)== recommendation_count:
            break
    
    if not recommendations:
        print("No recommendations to show in particular.")
        return
    
    print(f"Recommended books for member:{member_id}:")
    for book in recommendations:
        print(f"{book['title']} (Genre:{book['genre']}, ISBN:{book['isbn']}, Available in library)")

