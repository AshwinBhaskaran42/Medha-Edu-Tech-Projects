from datetime import date, timedelta

def register_member(member_id, name, contact, membership_type, branch_id, library_members,challenge_input):


    if membership_type == 'standard':
        expiry_duration = 180
    elif membership_type == 'premium':
        expiry_duration = 360

    membership_expiry= date.today() + timedelta(days= expiry_duration)

    library_members[member_id]={
        'name':name,
        'contact':contact,
        'membership_type':membership_type,
        'branch_id':branch_id,
        'membership_expiry':membership_expiry,
        'challenge_input':challenge_input, 
        'total_books_borrowed':0
    }
    print(f"Member: '{name}', registered with ID: {member_id} at branch: {branch_id}, with {membership_type} membership. ")
    print(f"Membership expiry: {membership_expiry}")

def register_members(library_members, library_branches):
    while True:
        # print(library_branches)
        print("\nAdding a new member.")
        branch_id= input("Enter branch id: ")
        if branch_id not in library_branches:
            print("Branch does not exist")
            continue

        member_id= input("Enter member ID: ")
        if member_id in library_members:
            print(f"Member ID:{member_id} already exists")
            continue
        name= input("Enter name: ")
        contact= input("Enter contact number: ")
        membership_type= input("Enter membership type (standard/premium): ").strip().lower()

        if membership_type not in ['standard', 'premium']:
            print("Membership type must be either Standard or Premium only.")
        
        print("Available Reading Challenges: 10, 20, 30, 40, 50 books. Enter 0 if not interested.")
        while True:
            challenge_input = int(input("Select your reading challenge goal (books): "))

            if challenge_input in [0,10, 20, 30, 40, 50]:
                break
            else:
                    print("Please choose from 0,10, 20, 30, 40, or 50.")
        
        register_member(member_id, name, contact, membership_type, branch_id, library_members,challenge_input)

        cont= input("Add another member? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
