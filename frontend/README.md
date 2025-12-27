# Workout Tracker Frontend

Next.js 15 frontend with TypeScript for workout tracking application.

## Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run development server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                  # Next.js 15 App Router
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   ├── globals.css      # Global styles
│   ├── log/             # Log creation/editing pages
│   └── history/         # Workout history pages
├── components/          # Reusable React components
├── lib/                 # Utilities
│   └── api.ts          # API client
├── types/              # TypeScript type definitions
│   └── index.ts        # Shared types
├── public/             # Static assets
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── next.config.ts      # Next.js config
├── tailwind.config.ts  # Tailwind CSS config
└── README.md          # This file
```

## Features

### Dashboard (Home)
- View recent workout logs
- Summary statistics
- Quick access to create new log

### Create/Edit Log
- Form for entering workout data
- Support for strength and running workouts
- Free-text reflection
- Body feedback (fatigue, pain/tightness)

### History
- List all workout logs
- Filter by date range
- View AI analysis

### AI Analysis
- Request Claude analysis for any log
- View human-friendly insights
- Explore structured machine context

## Technologies

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS
- **React 19**: Latest React features

## API Integration

The frontend communicates with the FastAPI backend via the API client in `lib/api.ts`.

See API documentation at `http://localhost:8000/docs` when backend is running.

## Development Tips

- Hot reload enabled in dev mode
- TypeScript strict mode for better type safety
- Tailwind CSS for rapid UI development
- All API calls are type-safe with TypeScript interfaces

## Notes

- This is a single-user MVP (no authentication)
- Data is stored in backend JSON files
- Designed for personal use and learning
- Extensible architecture for future AI features
