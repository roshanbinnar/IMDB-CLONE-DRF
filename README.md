# IMDB-CLONE-DRF

IMDB Clone API | Django REST Framework

Project Overview:

Developed a feature-rich REST API simulating core functionalities of the IMDB platform, enabling movie listing, ratings, and review management.

Key Features & Responsibilities:

•	User Management (user_app):

      o	Developed a custom User model with login and authentication functionality.
      o	Implemented user registration and login for secure access to authenticated actions.
      
•	Watchlist App:

    o	Stream Platform Management: Added and managed streaming services (e.g., Netflix, Hotstar).
    o	Watchlist Management: Implemented CRUD operations for movies and shows, linked to streaming platforms.
    
    o	Review & Rating System:
        
        o	Enabled authenticated users to post, update, or delete reviews and ratings.
        o	Prevented multiple reviews per user per movie.
        o	Automatically calculated and updated average movie ratings.
        o	Custom Permissions: Applied custom permissions to restrict edit/delete rights to review owners only.
        
•	Core Functionalities:

    o	Authentication & Authorization.
    o	Support for filtering, searching, and ordering of movies and streaming platforms.
    o	Implemented rate-limiting with custom throttling for review endpoints.
    o	Integrated pagination for scalable and efficient API responses.
