# Smart News Recommender

Smart News Recommender is a dynamic web application that delivers relevant news articles to users based on keyword-based search queries and category selection. The application integrates synonym expansion, keyword filtering, Redis caching, and a clean frontend interface to provide a fast and consistent user experience. It is fully containerized with Docker and deployed using Google Cloud Run.

## Project Overview

The application allows users to explore and search for current news topics through a simple and responsive interface. It fetches news from the NewsAPI.org service and processes the data to return focused results. To improve both performance and usability, it expands search terms using related synonyms and filters articles based on the presence of those terms in the title or description.

### Key Features

- Search for news by keyword or category
- Synonym expansion to include related terms per topic
- Keyword relevance filtering in article titles and descriptions
- Deduplication of similar articles
- FastAPI backend with async request handling
- Redis-based caching to reduce external API calls
- Modern frontend layout using Jinja2 templates and CSS
- Docker-based local development and containerized deployment
- Hosted publicly on Google Cloud Run

## Technologies Used

### Backend

- **FastAPI** – A high-performance, asynchronous Python web framework used to handle routing, templating, and API logic.
- **httpx** – An asynchronous HTTP client used to interact with the external News API.
- **Redis** – In-memory key-value store used for caching query results to improve performance and reduce redundant API calls.
- **dotenv** – Loads sensitive environment variables (like API keys) securely from a `.env` file.

### Frontend

- **HTML5 & CSS3** – Used for static layout and visual design.
- **Jinja2 Templates** – Enables dynamic content rendering based on server-side data.
- **Responsive Design** – Ensures compatibility across various device sizes.

### Deployment

- **Docker** – The app and Redis are containerized for consistent development and production environments.
- **Docker Compose** – Used to orchestrate both the FastAPI app and Redis locally.
- **Google Cloud Run** – The application is deployed as a containerized service to Google Cloud, allowing it to run continuously in a scalable, serverless environment.

## Search & Relevance Strategy

This project does not use machine learning or AI-based ranking. Instead, it determines article relevance using the following approach:

1. A predefined list of topic-based synonyms is maintained.
2. When a user enters a category or search term, all related synonyms are used to query the News API.
3. Articles are filtered based on whether the original search term appears in the title or description.
4. Duplicate titles are removed to ensure variety in the results.

This method is simple, fast, and effective for narrowing down results without requiring advanced algorithms.

## Caching Strategy

Redis is used as a caching layer to store the results of previous queries. The cache is indexed by search terms and expires automatically after a fixed time (e.g., 30–60 minutes). This improves response times for repeat queries and reduces the number of calls made to the external news provider.


## Deployment

The app is deployed using Google Cloud Run. To deploy:

1. Build the Docker image and push it to Google Container Registry.
2. Deploy the container to Cloud Run with environment variables set via the web console or `gcloud` CLI.
3. Connect to a Redis instance (if using a managed Redis service like Upstash or GCP Memorystore).


## Future Improvements

- Add AI-based summarization or ranking of articles
- Enable user profiles and saved searches
- Implement search suggestions and autocomplete
- Add pagination and filter controls on the UI
- Support multiple news providers via adapters

## License

This project is open-source and available under the MIT License.

## Author

Claudia Tannous  
University of Haifa  
claudetannous820@gmail.com
