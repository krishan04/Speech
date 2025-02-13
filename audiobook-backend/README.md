📂 audiobook-backend
 ├── 📂 src/main/java/com/audiobook
 │    ├── 📂 controllers     # API Controllers (handles requests)
 │    ├── 📂 services        # Business Logic (novel storage, progress tracking)
 │    ├── 📂 repositories    # Database Queries (Spring Data JPA)
 │    ├── 📂 models          # Database Entity Models (Novels, Users, Progress)
 │    ├── 📂 config          # Application Configurations
 │    ├── 📄 AudiobookApplication.java  # Main Spring Boot Application
 ├── 📂 src/main/resources
 │    ├── application.properties   # Database & Storage Configs
 ├── 📂 uploads         # Stores novel files (TXT, PDF) & audio files (MP3)
 ├── 📄 pom.xml         # Maven Dependencies
 ├── 📄 README.md       # Documentation




 Module	Method	Endpoint	Description
Novel Upload	POST	/novels/upload	Upload a TXT/PDF file
Retrieve Novel	GET	/novels/{id}	Fetch novel metadata
Delete Novel	DELETE	/novels/{id}	Remove a novel
Track Progress	POST	/progress/save	Save user’s last listened position
Get Progress	GET	/progress/{userId}/{novelId}	Retrieve user progress
Generate Audio	POST	/tts/generate	Send novel text & get AI-generated MP3
Stream Audio	GET	/audio/{novelId}	Stream/download generated MP3