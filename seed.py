"""
Seed script — populates the database with:
- Admin account (Likhitha N M)
- 20 sample books across genres
Run: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import get_collection
from models.user import create_user, find_user_by_email
from models.book import create_book, get_all_books
from utils.auth_helpers import hash_password
from config import Config

def seed_admin():
    email = Config.ADMIN_EMAIL.lower()
    if find_user_by_email(email):
        print(f"✅ Admin already exists: {email}")
        return
    hashed = hash_password(Config.ADMIN_PASSWORD)
    create_user(Config.ADMIN_USERNAME, email, hashed, role='admin')
    print(f"✅ Admin created: {Config.ADMIN_USERNAME} / {email}")

def seed_books():
    if len(get_all_books()) > 0:
        print("✅ Books already seeded.")
        return

    books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Classic Fiction",
            "description": "A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan in 1920s America.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432472-L.jpg",
            "year": 1925,
            "isbn": "9780743273565"
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "Classic Fiction",
            "description": "A story of racial injustice and moral growth in the American South, seen through the eyes of young Scout Finch.",
            "cover_url": "https://covers.openlibrary.org/b/id/8228691-L.jpg",
            "year": 1960,
            "isbn": "9780061935466"
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "genre": "Dystopian",
            "description": "A chilling portrait of a totalitarian society where Big Brother watches every move and thoughtcrime is punishable by death.",
            "cover_url": "https://covers.openlibrary.org/b/id/8575741-L.jpg",
            "year": 1949,
            "isbn": "9780451524935"
        },
        {
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "genre": "Dystopian",
            "description": "A futuristic society where people are engineered and conditioned to fit their social roles, challenging individuality.",
            "cover_url": "https://covers.openlibrary.org/b/id/8091016-L.jpg",
            "year": 1932,
            "isbn": "9780060850524"
        },
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "genre": "Fantasy",
            "description": "Young Harry Potter discovers he is a wizard and begins his education at Hogwarts School of Witchcraft and Wizardry.",
            "cover_url": "https://covers.openlibrary.org/b/id/10523456-L.jpg",
            "year": 1997,
            "isbn": "9780590353427"
        },
        {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "genre": "Fantasy",
            "description": "An epic quest across Middle-earth to destroy the One Ring and defeat the dark lord Sauron.",
            "cover_url": "https://covers.openlibrary.org/b/id/9255566-L.jpg",
            "year": 1954,
            "isbn": "9780544003415"
        },
        {
            "title": "The Hitchhiker's Guide to the Galaxy",
            "author": "Douglas Adams",
            "genre": "Science Fiction",
            "description": "Earth is demolished to make way for a hyperspace bypass. Arthur Dent survives and hitchhikes across the universe.",
            "cover_url": "https://covers.openlibrary.org/b/id/8739161-L.jpg",
            "year": 1979,
            "isbn": "9780345391803"
        },
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "genre": "Science Fiction",
            "description": "On the desert planet Arrakis, young Paul Atreides becomes entangled in treachery, politics, and a messianic destiny.",
            "cover_url": "https://covers.openlibrary.org/b/id/9161210-L.jpg",
            "year": 1965,
            "isbn": "9780441013593"
        },
        {
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "genre": "Mystery Thriller",
            "description": "Symbologist Robert Langdon is drawn into a dangerous mystery involving secret religious societies and hidden codes.",
            "cover_url": "https://covers.openlibrary.org/b/id/8225261-L.jpg",
            "year": 2003,
            "isbn": "9780307474278"
        },
        {
            "title": "Gone Girl",
            "author": "Gillian Flynn",
            "genre": "Mystery Thriller",
            "description": "When Amy Dunne disappears on her fifth wedding anniversary, suspicion falls on her husband Nick in this twisted psychological thriller.",
            "cover_url": "https://covers.openlibrary.org/b/id/8233488-L.jpg",
            "year": 2012,
            "isbn": "9780307588371"
        },
        {
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "genre": "Philosophical Fiction",
            "description": "A young Andalusian shepherd travels to Egypt in search of worldly treasure and discovers the secrets of the universe.",
            "cover_url": "https://covers.openlibrary.org/b/id/8597432-L.jpg",
            "year": 1988,
            "isbn": "9780062315007"
        },
        {
            "title": "Sapiens: A Brief History of Humankind",
            "author": "Yuval Noah Harari",
            "genre": "Non-Fiction",
            "description": "A sweeping narrative of humanity's creation and evolution from the Stone Age through the twenty-first century.",
            "cover_url": "https://covers.openlibrary.org/b/id/9281823-L.jpg",
            "year": 2011,
            "isbn": "9780062316097"
        },
        {
            "title": "Educated",
            "author": "Tara Westover",
            "genre": "Memoir",
            "description": "A memoir about a woman who grows up in a survivalist family and eventually earns a PhD from Cambridge University.",
            "cover_url": "https://covers.openlibrary.org/b/id/9310929-L.jpg",
            "year": 2018,
            "isbn": "9780399590504"
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "genre": "Romance",
            "description": "Elizabeth Bennet navigates issues of marriage, morality, and misconception in 19th-century England.",
            "cover_url": "https://covers.openlibrary.org/b/id/8739234-L.jpg",
            "year": 1813,
            "isbn": "9780141439518"
        },
        {
            "title": "The Notebook",
            "author": "Nicholas Sparks",
            "genre": "Romance",
            "description": "A timeless story of two lovers separated by forces beyond their control but whose love ultimately transcends all obstacles.",
            "cover_url": "https://covers.openlibrary.org/b/id/8225178-L.jpg",
            "year": 1996,
            "isbn": "9781455582877"
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "genre": "Self-Help",
            "description": "A practical guide to building good habits and breaking bad ones through small, incremental changes.",
            "cover_url": "https://covers.openlibrary.org/b/id/10521773-L.jpg",
            "year": 2018,
            "isbn": "9780735211292"
        },
        {
            "title": "Think and Grow Rich",
            "author": "Napoleon Hill",
            "genre": "Self-Help",
            "description": "A classic in personal development, outlining principles of success through the power of thought and persistence.",
            "cover_url": "https://covers.openlibrary.org/b/id/8225261-L.jpg",
            "year": 1937,
            "isbn": "9781585424337"
        },
        {
            "title": "A Brief History of Time",
            "author": "Stephen Hawking",
            "genre": "Science",
            "description": "Hawking explains complex cosmological concepts like black holes, the Big Bang, and the nature of time to general readers.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432447-L.jpg",
            "year": 1988,
            "isbn": "9780553380163"
        },
        {
            "title": "The Power of Now",
            "author": "Eckhart Tolle",
            "genre": "Spirituality",
            "description": "A guide to spiritual enlightenment that encourages readers to live in the present moment and detach from the ego.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432471-L.jpg",
            "year": 1997,
            "isbn": "9781577314806"
        },
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "genre": "Coming of Age",
            "description": "Teenager Holden Caulfield narrates his experiences in New York City after being expelled from prep school.",
            "cover_url": "https://covers.openlibrary.org/b/id/8228689-L.jpg",
            "year": 1951,
            "isbn": "9780316769174"
        },
    ]

    for b in books:
        create_book(**b)
        print(f"📚 Added: {b['title']}")

    print(f"\n✅ {len(books)} books seeded successfully!")


def seed_more_books():
    """Adds 25 more books — skips any title already in the database."""
    from models.book import get_all_books
    existing_titles = {b['title'].lower() for b in get_all_books()}

    more_books = [
        {
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "genre": "Young Adult Fiction",
            "description": "In a dystopian future, teenager Katniss Everdeen volunteers to participate in the Hunger Games — a televised fight to the death — in place of her younger sister.",
            "cover_url": "https://covers.openlibrary.org/b/id/8228681-L.jpg",
            "year": 2008,
            "isbn": "9780439023481"
        },
        {
            "title": "The Fault in Our Stars",
            "author": "John Green",
            "genre": "Young Adult Fiction",
            "description": "Two teenagers with cancer meet at a support group and fall in love, embarking on a bittersweet journey that will change their lives forever.",
            "cover_url": "https://covers.openlibrary.org/b/id/7887036-L.jpg",
            "year": 2012,
            "isbn": "9780525478812"
        },
        {
            "title": "Animal Farm",
            "author": "George Orwell",
            "genre": "Political Satire",
            "description": "A satirical allegory where farm animals overthrow their human owner to establish an equal society, only to find power corrupts their leaders.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432438-L.jpg",
            "year": 1945,
            "isbn": "9780451526342"
        },
        {
            "title": "Sherlock Holmes: The Complete Stories",
            "author": "Arthur Conan Doyle",
            "genre": "Crime Thriller",
            "description": "The complete adventures of the world's greatest detective Sherlock Holmes and his loyal companion Dr. Watson across 60 mystery stories.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432112-L.jpg",
            "year": 1892,
            "isbn": "9781853260896"
        },
        {
            "title": "And Then There Were None",
            "author": "Agatha Christie",
            "genre": "Crime Thriller",
            "description": "Ten strangers are lured to an isolated island, each accused of murder. One by one they are killed, and the murderer is one of them.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432191-L.jpg",
            "year": 1939,
            "isbn": "9780062073488"
        },
        {
            "title": "The Girl with the Dragon Tattoo",
            "author": "Stieg Larsson",
            "genre": "Crime Thriller",
            "description": "Journalist Mikael Blomkvist and hacker Lisbeth Salander investigate a decades-old disappearance within a wealthy Swedish family.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432009-L.jpg",
            "year": 2005,
            "isbn": "9780307454546"
        },
        {
            "title": "The Kite Runner",
            "author": "Khaled Hosseini",
            "genre": "Historical Fiction",
            "description": "A powerful story of friendship, betrayal and redemption set against the turbulent history of Afghanistan from the 1970s to the early 2000s.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432001-L.jpg",
            "year": 2003,
            "isbn": "9781594631931"
        },
        {
            "title": "A Thousand Splendid Suns",
            "author": "Khaled Hosseini",
            "genre": "Historical Fiction",
            "description": "The lives of two Afghan women intertwine across three decades of devastating conflict, united by love, loss, and the resilience of the human spirit.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432002-L.jpg",
            "year": 2007,
            "isbn": "9781594483073"
        },
        {
            "title": "The Secret",
            "author": "Rhonda Byrne",
            "genre": "Self-Help",
            "description": "Based on the law of attraction, this book reveals how positive thinking and visualization can lead to health, wealth, and happiness.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432399-L.jpg",
            "year": 2006,
            "isbn": "9781582701707"
        },
        {
            "title": "Rich Dad Poor Dad",
            "author": "Robert T. Kiyosaki",
            "genre": "Self-Help",
            "description": "A personal finance classic contrasting the money mindsets of the author's two father figures, teaching financial literacy and investment.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432300-L.jpg",
            "year": 1997,
            "isbn": "9781612680194"
        },
        {
            "title": "Ikigai: The Japanese Secret to a Long and Happy Life",
            "author": "Héctor García & Francesc Miralles",
            "genre": "Self-Help",
            "description": "Explores the Japanese concept of ikigai — your reason for being — and how finding yours can bring fulfilment and longevity.",
            "cover_url": "https://covers.openlibrary.org/b/id/8897231-L.jpg",
            "year": 2016,
            "isbn": "9780143130727"
        },
        {
            "title": "Frankenstein",
            "author": "Mary Shelley",
            "genre": "Gothic Fiction",
            "description": "Scientist Victor Frankenstein creates a living creature from dead body parts, exploring themes of ambition, responsibility, and what it means to be human.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432445-L.jpg",
            "year": 1818,
            "isbn": "9780141439471"
        },
        {
            "title": "Dracula",
            "author": "Bram Stoker",
            "genre": "Gothic Fiction",
            "description": "English solicitor Jonathan Harker travels to Transylvania and encounters the terrifying Count Dracula in this foundational vampire horror novel.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432412-L.jpg",
            "year": 1897,
            "isbn": "9780141439846"
        },
        {
            "title": "The Midnight Library",
            "author": "Matt Haig",
            "genre": "Philosophical Fiction",
            "description": "Between life and death there is a library filled with infinite books. Each book offers a different version of your life if you had made different choices.",
            "cover_url": "https://covers.openlibrary.org/b/id/10872012-L.jpg",
            "year": 2020,
            "isbn": "9780525559474"
        },
        {
            "title": "Becoming",
            "author": "Michelle Obama",
            "genre": "Memoir",
            "description": "An intimate look at the life of former US First Lady Michelle Obama — from her childhood in Chicago to her years in the White House.",
            "cover_url": "https://covers.openlibrary.org/b/id/8988765-L.jpg",
            "year": 2018,
            "isbn": "9781524763138"
        },
        {
            "title": "Steve Jobs",
            "author": "Walter Isaacson",
            "genre": "Biography",
            "description": "The authorised biography of Apple co-founder Steve Jobs, drawn from exclusive interviews with Jobs, his family, friends, and rivals.",
            "cover_url": "https://covers.openlibrary.org/b/id/7978960-L.jpg",
            "year": 2011,
            "isbn": "9781451648539"
        },
        {
            "title": "Wings of Fire",
            "author": "A.P.J. Abdul Kalam",
            "genre": "Biography",
            "description": "The autobiography of India's missile scientist and former President, chronicling his rise from a small coastal town to guiding India's space and defense programs.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432521-L.jpg",
            "year": 1999,
            "isbn": "9788173711466"
        },
        {
            "title": "The God of Small Things",
            "author": "Arundhati Roy",
            "genre": "Literary Fiction",
            "description": "Set in Kerala, India, this Booker Prize-winning novel follows the lives of twins whose childhood is shattered by the intervention of love laws.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432561-L.jpg",
            "year": 1997,
            "isbn": "9780812979657"
        },
        {
            "title": "Five Point Someone",
            "author": "Chetan Bhagat",
            "genre": "Coming of Age",
            "description": "Three friends at IIT Delhi struggle with the pressure of engineering college, friendship, love, and finding what really matters in life.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432565-L.jpg",
            "year": 2004,
            "isbn": "9788129104595"
        },
        {
            "title": "The Psychology of Money",
            "author": "Morgan Housel",
            "genre": "Non-Fiction",
            "description": "Explores how people think about money in 19 short stories, revealing the strange ways we behave with wealth, greed, and fear.",
            "cover_url": "https://covers.openlibrary.org/b/id/10519773-L.jpg",
            "year": 2020,
            "isbn": "9780857197689"
        },
        {
            "title": "Man's Search for Meaning",
            "author": "Viktor E. Frankl",
            "genre": "Psychology",
            "description": "Holocaust survivor Frankl describes life in Nazi death camps and his psychotherapy method of finding a reason to live.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432488-L.jpg",
            "year": 1946,
            "isbn": "9780807014271"
        },
        {
            "title": "Thinking, Fast and Slow",
            "author": "Daniel Kahneman",
            "genre": "Psychology",
            "description": "Nobel laureate Kahneman explains the two systems of thinking — fast intuition and slow reasoning — and how they shape our decisions.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432499-L.jpg",
            "year": 2011,
            "isbn": "9780374533557"
        },
        {
            "title": "The Adventures of Tom Sawyer",
            "author": "Mark Twain",
            "genre": "Adventure Fiction",
            "description": "Tom Sawyer's childhood adventures along the Mississippi River, filled with mischief, treasure hunts, and the search for true friendship.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432300-L.jpg",
            "year": 1876,
            "isbn": "9780143039563"
        },
        {
            "title": "Around the World in 80 Days",
            "author": "Jules Verne",
            "genre": "Adventure Fiction",
            "description": "English gentleman Phileas Fogg bets he can circumnavigate the globe in just 80 days in this thrilling Victorian adventure.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432317-L.jpg",
            "year": 1872,
            "isbn": "9780140449068"
        },
        {
            "title": "The Subtle Art of Not Giving a F*ck",
            "author": "Mark Manson",
            "genre": "Self-Help",
            "description": "A counterintuitive approach to living a good life — arguing that accepting our limitations and failures leads to true happiness.",
            "cover_url": "https://covers.openlibrary.org/b/id/8432601-L.jpg",
            "year": 2016,
            "isbn": "9780062457714"
        },
    ]

    added = 0
    for b in more_books:
        if b['title'].lower() not in existing_titles:
            create_book(**b)
            print(f"📚 Added: {b['title']}")
            added += 1
        else:
            print(f"⏭️  Skipped (exists): {b['title']}")

    print(f"\n✅ {added} new books added ({len(more_books) - added} already existed).")


if __name__ == '__main__':
    print("🌱 Seeding database...\n")
    seed_admin()
    seed_books()
    seed_more_books()
    print("\n🎉 Database seeding complete!")
    print(f"\nAdmin Login:")
    print(f"  Email    : {Config.ADMIN_EMAIL}")
    print(f"  Password : {Config.ADMIN_PASSWORD}")

