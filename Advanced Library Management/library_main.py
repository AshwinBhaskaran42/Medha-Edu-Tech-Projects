import sys
sys.path.append('./modules')

from datetime import date, timedelta
from imports import *

library_branches = {}
library_members = {}
waitlist={}

add_library_branches(library_branches)
print(library_branches)
print("\n")
print(library_members)
add_books(library_branches)
print(library_branches)
print("\n")
print(library_members)
register_members(library_members, library_branches)
print(library_branches)
print("\n")
print(library_members)
issue_books(library_members, library_branches, waitlist)
print(library_branches)
print("\n")
print(library_members)
return_books(library_members, library_branches, waitlist)
print(library_branches)
print("\n")
print(library_members)

# print(library_branches)
# print(library_members)
