Feature: View Notes

    Example: You make a note and view it
        Given the user makes a note
        And the user is on the note viewing page
        The user can view that note
        The user can view all notes


Feature: Share Note

    Example: You share a note
        Given the user makes a note
        And the user sends the share code
        A different user can view the note