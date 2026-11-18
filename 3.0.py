import random

project_bases = [
    "Alpha", "Beta", "Gamma", "Delta", "Omega", "Nexus", "Vertex", "Zenith", 
    "Apex", "Matrix", "Vector", "Echo", "Mirage", "Titan", "Pioneer", "Orbit",
    "Stellar", "Core", "Flux", "Horizon", "Vanguard", "Synergy", "Beacon",
    "Atlas", "Pulse", "Quantum", "Nova", "Opa", "Solaris", "Hyperion", "Hydra"
]

platforms = [
    ("mobile app on React Native", ["Expo", "navigation", "validation", "React Hook Form", "Redux Toolkit"]),
    ("web platform on Next.js", ["SSR", "Tailwind CSS", "TypeScript", "Stripe integration", "Prisma ORM"]),
    ("backend API on Node.js (Express)", ["TypeScript", "PostgreSQL", "JWT auth", "Docker", "Swagger docs"]),
    ("analytics dashboard on React", ["Chart.js", "Material-UI", "WebSockets", "i18n", "Zustand"]),
    ("ML pipeline in Python", ["scikit-learn", "Pandas", "FastAPI", "pytest", "Docker container"]),
    ("cross-platform app on Flutter", ["Bloc", "Firebase", "SQLite", "Google Maps", "Riverpod"]),
    ("e-commerce backend on Django", ["PostgreSQL", "Celery", "Redis", "Django REST framework", "Stripe"]),
    ("microservice on Go (Golang)", ["gRPC", "Prometheus", "PostgreSQL", "Redis cache", "Goroutines"]),
    ("desktop app on Electron", ["React", "TypeScript", "SQLite", "IPC communication", "Tailwind"]),
    ("DevOps automation pipeline", ["GitHub Actions", "Kubernetes", "Terraform", "Docker", "Prometheus"])
]

extra_features = [
    "with automated testing and CI/CD integration",
    "with high-load performance optimization",
    "with advanced security audit and encryption",
    "with real-time data synchronization",
    "with comprehensive unit test coverage",
    "complying with enterprise standards",
    "optimized for low-latency cloud deployment",
    "featuring modular architecture and clean code"
]

generated_texts = set()
documents = []

i = 1
while i <= 1000:
    proj_name = f"{random.choice(project_bases)}_{i}"
    platform_name, features = random.choice(platforms)
    
    selected_features = random.sample(features, k=min(3, len(features)))
    features_str = ", ".join(selected_features)
    extra = random.choice(extra_features)
    
    text = f"Architect project {proj_name}: {platform_name} with {features_str} {extra}."
    
    if text in generated_texts:
        continue
        
    generated_texts.add(text)
    doc_id = f"doc_{i}"
    documents.append((doc_id, text))
    i += 1

# Запись в dataset.txt
with open("dataset.txt", "w", encoding="utf-8") as f:
    for doc_id, text in documents:
        f.write(f"ID: {doc_id}\nText: {text}\n" + "-" * 50 + "\n")

# Запись в dataset.md
with open("dataset.md", "w", encoding="utf-8") as f:
    f.write("# Unique Projects Dataset (1000 items)\n\n")
    for doc_id, text in documents:
        f.write(f"## `{doc_id}`\n\n{text}\n\n---\n\n")

print("Готово! Созданы два файла: dataset.txt и dataset.md (по 1000 уникальных записей в каждом).")