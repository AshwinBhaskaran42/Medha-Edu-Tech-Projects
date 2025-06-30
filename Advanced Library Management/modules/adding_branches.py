def add_library_branch(branch_id, location, operating_hours, library_branches):

    library_branches[branch_id]={
        "location": location,
        "operating_hours": operating_hours
    }
    print(f"Branch {branch_id} at {location} added Successfully.")

def add_library_branches(library_branches):
    while True:
        print("Add a new Library Branch:")
        branch_id= input("Enter branch id: ").strip()
        if branch_id in library_branches:
            print(f"{branch_id} already exists!")
            continue
        location= input("Enter location: ").strip()
        operating_hours= input("Enter operating hours: ").strip()
    
        add_library_branch(branch_id, location, operating_hours, library_branches)

        cont= input("Add another branch? (yes/no): ").strip().lower()
        if cont !='yes':
            break
        