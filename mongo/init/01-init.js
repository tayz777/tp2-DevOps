db = db.getSiblingDB('blog_db');

db.createCollection('posts', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'content', 'author'],
      properties: {
        title: {
          bsonType: 'string',
          description: 'Titre de l\'article – obligatoire'
        },
        content: {
          bsonType: 'string',
          description: 'Contenu de l\'article – obligatoire'
        },
        author: {
          bsonType: 'string',
          description: 'Auteur de l\'article – obligatoire'
        }
      }
    }
  }
});

db.posts.insertMany([
  {
    title: 'Introduction à Docker',
    content: 'Docker est une plateforme de conteneurisation qui simplifie le déploiement des applications.',
    author: 'Zayd El AJLI'
  },
  {
    title: 'MongoDB et les bases NoSQL',
    content: 'Les bases NoSQL offrent flexibilité et scalabilité pour les données non structurées.',
    author: 'Glenden AHO'
  },
  {
    title: 'FastAPI : un framework moderne',
    content: 'FastAPI permet de construire des API REST performantes avec Python 3.9+.',
    author: 'Frederic Sturm'
  },
  {
    title: 'Docker Compose en pratique',
    content: 'Docker Compose orchestre plusieurs conteneurs via un seul fichier YAML.',
    author: 'Sacha MOREAU'
  },
  {
    title: 'Bonnes pratiques DevOps',
    content: 'Le DevOps réunit développement et opérations pour des livraisons continues et fiables.',
    author: 'Zayd El AJLI'
  }
]);
