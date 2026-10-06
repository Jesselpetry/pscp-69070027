""" SurprisingVote """

def main():
    """SurprisingVote"""
    vote = float(input())
    highest_vote = float(input())
    lowest_vote = vote - (2 * highest_vote)
    if lowest_vote < 0:
        lowest_vote = 0

    if highest_vote - lowest_vote > 2:
        print("Surprising")
    else:
        print("Not surprising")

if __name__ == "__main__":
    main()
